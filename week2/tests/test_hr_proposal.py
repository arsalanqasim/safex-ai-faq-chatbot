# ==============================================================================
# HR Automation Proposal - Unit Tests
# ==============================================================================
from datetime import date, timedelta

import pytest

from src.modules.hr_proposal.engine import (
    HrProposalEngine,
    HrProposalError,
    ONBOARDING_CHECKLIST_TEMPLATE,
)


@pytest.fixture
def engine(tmp_path):
    return HrProposalEngine(data_dir=tmp_path)


# ------------------------------------------------------------------
# Onboarding pipeline
# ------------------------------------------------------------------
def test_create_onboarding_case_generates_full_checklist(engine):
    result = engine.create_onboarding_case(
        "Jane Doe", "jane@safex.com", "Engineering", "Backend Intern", date(2026, 1, 5)
    )
    assert result["employee"]["employee_id"].startswith("EMP-")
    assert len(result["tasks"]) == len(ONBOARDING_CHECKLIST_TEMPLATE)

    cases = engine.get_onboarding_cases()
    assert len(cases) == 1
    assert cases.iloc[0]["full_name"] == "Jane Doe"


def test_create_onboarding_case_rejects_bad_email(engine):
    with pytest.raises(HrProposalError):
        engine.create_onboarding_case("Jane Doe", "not-an-email", "Engineering", "Intern", date.today())


def test_create_onboarding_case_rejects_empty_name(engine):
    with pytest.raises(HrProposalError):
        engine.create_onboarding_case("   ", "jane@safex.com", "Engineering", "Intern", date.today())


def test_onboarding_progress_tracks_task_completion(engine):
    result = engine.create_onboarding_case(
        "John Smith", "john@safex.com", "Sales", "Account Exec", date.today()
    )
    employee_id = result["employee"]["employee_id"]
    assert engine.onboarding_progress(employee_id) == 0.0

    tasks = engine.get_onboarding_tasks(employee_id)
    first_task_id = tasks.iloc[0]["task_id"]
    engine.set_task_completed(first_task_id, True)

    expected = 1 / len(ONBOARDING_CHECKLIST_TEMPLATE)
    assert engine.onboarding_progress(employee_id) == pytest.approx(expected)


def test_set_task_completed_unknown_task_raises(engine):
    with pytest.raises(HrProposalError):
        engine.set_task_completed("TSK-DOESNOTEXIST", True)


# ------------------------------------------------------------------
# Leave-request ticketing
# ------------------------------------------------------------------
def test_submit_leave_request_computes_days_and_defaults_to_pending(engine):
    ticket = engine.submit_leave_request(
        "Jane Doe", "jane@safex.com", "Annual",
        date(2026, 2, 1), date(2026, 2, 3), "Family trip",
    )
    assert ticket["leave_days"] == "3"
    assert ticket["status"] == "Pending"
    assert ticket["ticket_id"].startswith("LR-")


def test_submit_leave_request_rejects_end_before_start(engine):
    with pytest.raises(HrProposalError):
        engine.submit_leave_request(
            "Jane Doe", "jane@safex.com", "Annual",
            date(2026, 2, 3), date(2026, 2, 1), "Oops",
        )


def test_submit_leave_request_rejects_invalid_leave_type(engine):
    with pytest.raises(HrProposalError):
        engine.submit_leave_request(
            "Jane Doe", "jane@safex.com", "Sabbatical",
            date.today(), date.today(), "Not a real type",
        )


def test_submit_leave_request_detects_overlap_with_pending_ticket(engine):
    engine.submit_leave_request(
        "Jane Doe", "jane@safex.com", "Annual",
        date(2026, 3, 1), date(2026, 3, 5), "Trip",
    )
    with pytest.raises(HrProposalError):
        engine.submit_leave_request(
            "Jane Doe", "jane@safex.com", "Sick",
            date(2026, 3, 4), date(2026, 3, 6), "Overlapping",
        )


def test_submit_leave_request_allows_overlap_after_rejection(engine):
    first = engine.submit_leave_request(
        "Jane Doe", "jane@safex.com", "Annual",
        date(2026, 3, 1), date(2026, 3, 5), "Trip",
    )
    engine.update_leave_status(first["ticket_id"], "Rejected")

    second = engine.submit_leave_request(
        "Jane Doe", "jane@safex.com", "Sick",
        date(2026, 3, 4), date(2026, 3, 6), "No longer overlapping since rejected",
    )
    assert second["status"] == "Pending"


def test_update_leave_status_approves_ticket(engine):
    ticket = engine.submit_leave_request(
        "John Smith", "john@safex.com", "Casual",
        date.today(), date.today() + timedelta(days=1), "Personal",
    )
    updated = engine.update_leave_status(ticket["ticket_id"], "Approved", "Looks good")
    assert updated["status"] == "Approved"
    assert updated["reviewer_notes"] == "Looks good"


def test_update_leave_status_unknown_ticket_raises(engine):
    with pytest.raises(HrProposalError):
        engine.update_leave_status("LR-DOESNOTEXIST", "Approved")


def test_update_leave_status_invalid_status_raises(engine):
    ticket = engine.submit_leave_request(
        "John Smith", "john@safex.com", "Casual",
        date.today(), date.today(), "Personal",
    )
    with pytest.raises(HrProposalError):
        engine.update_leave_status(ticket["ticket_id"], "Cancelled")


def test_list_leave_requests_filters_by_status_and_employee(engine):
    engine.submit_leave_request(
        "Jane Doe", "jane@safex.com", "Annual", date(2026, 4, 1), date(2026, 4, 2), "A"
    )
    engine.submit_leave_request(
        "John Smith", "john@safex.com", "Sick", date(2026, 4, 3), date(2026, 4, 3), "B"
    )

    assert len(engine.list_leave_requests(status="Pending")) == 2
    assert len(engine.list_leave_requests(employee_name="Jane Doe")) == 1
    assert len(engine.list_leave_requests(status="Approved")) == 0
