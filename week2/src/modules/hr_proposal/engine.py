# HR Automation Proposal - Engine
# Developer: Muhammad Faozan Mujtaba (Group Member)
# For SafeX Solutions Business Automation Research
#
# Implements two prototype workflows for a corporate HR team:
#   1. Onboarding pipeline  - generates a standard checklist of tasks for
#      every new hire and tracks completion progress.
#   2. Leave-request ticketing - lets employees submit leave requests,
#      detects overlaps with their own approved/pending leave, and lets an
#      HR reviewer approve/reject each ticket.
#
# Data is persisted as CSV files so the prototype has no external service
# dependency. Each engine instance can be pointed at its own data
# directory, which is what makes the class easy to unit test.

from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

DEFAULT_DATA_DIR = Path(__file__).parent / "data"

ONBOARDING_EMPLOYEES_FILE = "onboarding_employees.csv"
ONBOARDING_TASKS_FILE = "onboarding_tasks.csv"
LEAVE_REQUESTS_FILE = "leave_requests.csv"

# (task description, days after start date it is due)
ONBOARDING_CHECKLIST_TEMPLATE = [
    ("Send welcome email & offer letter confirmation", 0),
    ("Create company email and IT accounts", 0),
    ("Provision laptop / hardware", 1),
    ("Collect signed HR paperwork (NDA, tax forms)", 2),
    ("Enroll in payroll and benefits", 3),
    ("Schedule orientation / company overview session", 3),
    ("Assign onboarding buddy and team introductions", 5),
    ("Grant access to internal tools and repositories", 5),
    ("30-day check-in with manager", 30),
]

LEAVE_TYPES = ["Annual", "Sick", "Casual", "Unpaid"]
LEAVE_STATUSES = ["Pending", "Approved", "Rejected"]

EMPLOYEES_COLUMNS = ["employee_id", "full_name", "email", "department", "role", "start_date", "created_at"]
TASKS_COLUMNS = ["task_id", "employee_id", "task", "due_date", "completed"]
LEAVE_COLUMNS = [
    "ticket_id", "employee_name", "employee_email", "leave_type",
    "start_date", "end_date", "leave_days", "reason", "status",
    "reviewer_notes", "created_at", "updated_at",
]


class HrProposalError(ValueError):
    """Raised for invalid HR automation inputs (bad dates, unknown ids, etc.)."""


class HrProposalEngine:
    """
    Onboarding pipeline and leave-request ticketing system.

    All state is stored as CSV files under `data_dir` so the prototype can
    run without a database. Pass a temp directory in tests to avoid
    touching the module's real data files.
    """

    def __init__(self, data_dir: Path | str = DEFAULT_DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal CSV helpers
    # ------------------------------------------------------------------
    def _path(self, filename: str) -> Path:
        return self.data_dir / filename

    def _read(self, filename: str, columns: list[str]) -> pd.DataFrame:
        path = self._path(filename)
        if not path.exists():
            return pd.DataFrame(columns=columns)
        return pd.read_csv(path, dtype=str).fillna("")

    def _write(self, filename: str, df: pd.DataFrame) -> None:
        df.to_csv(self._path(filename), index=False)

    # ------------------------------------------------------------------
    # Onboarding pipeline
    # ------------------------------------------------------------------
    def create_onboarding_case(
        self,
        full_name: str,
        email: str,
        department: str,
        role: str,
        start_date: date,
    ) -> dict:
        """Register a new hire and generate their onboarding task checklist."""
        if not full_name.strip():
            raise HrProposalError("Full name is required.")
        if "@" not in email:
            raise HrProposalError("A valid email address is required.")

        employees = self._read(ONBOARDING_EMPLOYEES_FILE, EMPLOYEES_COLUMNS)
        employee_id = f"EMP-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now().isoformat(timespec="seconds")

        new_employee = {
            "employee_id": employee_id,
            "full_name": full_name.strip(),
            "email": email.strip(),
            "department": department,
            "role": role.strip(),
            "start_date": start_date.isoformat(),
            "created_at": now,
        }
        employees = pd.concat([employees, pd.DataFrame([new_employee])], ignore_index=True)
        self._write(ONBOARDING_EMPLOYEES_FILE, employees)

        tasks = self._read(ONBOARDING_TASKS_FILE, TASKS_COLUMNS)
        new_tasks = []
        for task, offset in ONBOARDING_CHECKLIST_TEMPLATE:
            new_tasks.append({
                "task_id": f"TSK-{uuid.uuid4().hex[:8].upper()}",
                "employee_id": employee_id,
                "task": task,
                "due_date": (start_date + timedelta(days=offset)).isoformat(),
                "completed": "False",
            })
        tasks = pd.concat([tasks, pd.DataFrame(new_tasks)], ignore_index=True)
        self._write(ONBOARDING_TASKS_FILE, tasks)

        return {"employee": new_employee, "tasks": new_tasks}

    def get_onboarding_cases(self) -> pd.DataFrame:
        return self._read(ONBOARDING_EMPLOYEES_FILE, EMPLOYEES_COLUMNS)

    def get_onboarding_tasks(self, employee_id: str | None = None) -> pd.DataFrame:
        tasks = self._read(ONBOARDING_TASKS_FILE, TASKS_COLUMNS)
        if employee_id is not None:
            tasks = tasks[tasks["employee_id"] == employee_id]
        return tasks

    def set_task_completed(self, task_id: str, completed: bool) -> None:
        tasks = self._read(ONBOARDING_TASKS_FILE, TASKS_COLUMNS)
        if task_id not in tasks["task_id"].values:
            raise HrProposalError(f"Unknown task_id: {task_id}")
        tasks.loc[tasks["task_id"] == task_id, "completed"] = str(completed)
        self._write(ONBOARDING_TASKS_FILE, tasks)

    def onboarding_progress(self, employee_id: str) -> float:
        """Fraction (0-1) of onboarding tasks completed for one employee."""
        tasks = self.get_onboarding_tasks(employee_id)
        if tasks.empty:
            return 0.0
        completed = (tasks["completed"] == "True").sum()
        return completed / len(tasks)

    # ------------------------------------------------------------------
    # Leave-request ticketing
    # ------------------------------------------------------------------
    def submit_leave_request(
        self,
        employee_name: str,
        employee_email: str,
        leave_type: str,
        start_date: date,
        end_date: date,
        reason: str,
    ) -> dict:
        """Validate and file a new leave-request ticket."""
        if not employee_name.strip():
            raise HrProposalError("Employee name is required.")
        if leave_type not in LEAVE_TYPES:
            raise HrProposalError(f"Leave type must be one of {LEAVE_TYPES}.")
        if end_date < start_date:
            raise HrProposalError("End date cannot be before start date.")

        leave_days = (end_date - start_date).days + 1

        requests = self._read(LEAVE_REQUESTS_FILE, LEAVE_COLUMNS)
        overlap = self._find_overlap(requests, employee_name, start_date, end_date)
        if overlap is not None:
            raise HrProposalError(
                f"Overlaps with existing {overlap['status']} ticket {overlap['ticket_id']} "
                f"({overlap['start_date']} to {overlap['end_date']})."
            )

        now = datetime.now().isoformat(timespec="seconds")
        ticket = {
            "ticket_id": f"LR-{uuid.uuid4().hex[:8].upper()}",
            "employee_name": employee_name.strip(),
            "employee_email": employee_email.strip(),
            "leave_type": leave_type,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "leave_days": str(leave_days),
            "reason": reason.strip(),
            "status": "Pending",
            "reviewer_notes": "",
            "created_at": now,
            "updated_at": now,
        }
        requests = pd.concat([requests, pd.DataFrame([ticket])], ignore_index=True)
        self._write(LEAVE_REQUESTS_FILE, requests)
        return ticket

    @staticmethod
    def _find_overlap(
        requests: pd.DataFrame, employee_name: str, start_date: date, end_date: date
    ) -> dict | None:
        """Return the first active (Pending/Approved) ticket for this employee
        whose date range overlaps [start_date, end_date], if any."""
        active = requests[
            (requests["employee_name"] == employee_name.strip())
            & (requests["status"].isin(["Pending", "Approved"]))
        ]
        for _, row in active.iterrows():
            existing_start = date.fromisoformat(row["start_date"])
            existing_end = date.fromisoformat(row["end_date"])
            if start_date <= existing_end and existing_start <= end_date:
                return row.to_dict()
        return None

    def list_leave_requests(
        self, status: str | None = None, employee_name: str | None = None
    ) -> pd.DataFrame:
        requests = self._read(LEAVE_REQUESTS_FILE, LEAVE_COLUMNS)
        if status is not None:
            requests = requests[requests["status"] == status]
        if employee_name is not None:
            requests = requests[requests["employee_name"] == employee_name]
        return requests

    def update_leave_status(self, ticket_id: str, status: str, reviewer_notes: str = "") -> dict:
        if status not in LEAVE_STATUSES:
            raise HrProposalError(f"Status must be one of {LEAVE_STATUSES}.")

        requests = self._read(LEAVE_REQUESTS_FILE, LEAVE_COLUMNS)
        if ticket_id not in requests["ticket_id"].values:
            raise HrProposalError(f"Unknown ticket_id: {ticket_id}")

        mask = requests["ticket_id"] == ticket_id
        requests.loc[mask, "status"] = status
        requests.loc[mask, "reviewer_notes"] = reviewer_notes
        requests.loc[mask, "updated_at"] = datetime.now().isoformat(timespec="seconds")
        self._write(LEAVE_REQUESTS_FILE, requests)
        return requests.loc[mask].iloc[0].to_dict()
