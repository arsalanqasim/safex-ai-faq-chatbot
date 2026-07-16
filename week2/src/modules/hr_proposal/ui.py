import math
from datetime import date

import streamlit as st

from src.modules.registry import MODULE_REGISTRY
from src.modules.hr_proposal.engine import (
    HrProposalEngine,
    HrProposalError,
    LEAVE_TYPES,
)

DEPARTMENTS = ["Engineering", "AI/ML", "Sales", "Marketing", "Finance", "HR", "Operations"]

STATUS_DOT = {"Pending": "var(--warning)", "Approved": "var(--success)", "Rejected": "var(--error)"}
AVATAR_COLORS = ["var(--accent)", "var(--success)", "var(--warning)", "var(--error)", "#A371F7", "#3FB0AC"]

# --- Inline monochrome line icons (Feather-style, stroke=currentColor) -------
_I_USERS = ('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
            '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>')
_I_TREND = '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'
_I_CLOCK = '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
_I_CHECK = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
_I_USERPLUS = ('<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/>'
               '<line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/>')
_I_EDIT = ('<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
           '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>')
_I_TICKET = ('<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/>'
             '<line x1="13" y1="5" x2="13" y2="19"/>')

# ---------------------------------------------------------------------------
# All native-widget styling is scoped under `.st-key-hrp-root` (added by the
# keyed root container) so it never leaks into the sidebar or sibling modules
# in the shared hub. Injected-HTML blocks use unique `.hrp-*` class names.
# ---------------------------------------------------------------------------
_CSS = """
<style>
@keyframes hrp-in{from{opacity:0;transform:translateY(7px);}to{opacity:1;transform:none;}}
@keyframes hrp-grow{from{transform:scaleX(0);}to{transform:scaleX(1);}}

/* ---- module badge (matches KPI accent language) ---- */
.hrp-badge{display:inline-flex;align-items:center;gap:7px;padding:5px 15px;border-radius:999px;
  background:var(--accent-soft);border:1px solid var(--accent-soft);color:var(--accent);
  font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;}

/* ---- KPI tiles (semantic per-tile accent via --k) ---- */
.hrp-kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:8px 0 26px;}
.hrp-kpi{--k:var(--accent);position:relative;overflow:hidden;display:flex;gap:13px;align-items:center;
  background:linear-gradient(135deg,color-mix(in srgb,var(--k) 14%,transparent),transparent 62%),var(--card-bg);
  border:1px solid var(--card-border);border-radius:14px;padding:15px 16px 14px 20px;
  animation:hrp-in .35s ease both;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease;}
.hrp-kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-card);}
.hrp-kpi-accent{position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--k);}
.hrp-kpi.is-zero{background:var(--card-bg);}
.hrp-kpi.is-zero .hrp-kpi-accent{background:var(--border-strong);}
.hrp-kpi.is-zero .hrp-kpi-val,.hrp-kpi.is-zero .hrp-kpi-ic{color:var(--text-muted);}
.hrp-kpi.is-zero .hrp-ring-txt{fill:var(--text-muted);}
.hrp-kpi-ic{width:38px;height:38px;border-radius:10px;background:color-mix(in srgb,var(--k) 12%,transparent);
  border:1px solid color-mix(in srgb,var(--k) 22%,transparent);display:flex;align-items:center;
  justify-content:center;color:var(--k);flex-shrink:0;}
.hrp-kpi-val{font-size:24px;font-weight:650;color:var(--text-primary);line-height:1.1;letter-spacing:-.5px;}
.hrp-kpi-lbl{font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:var(--text-muted);margin-top:3px;}
.hrp-kpi-trend{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text-secondary);margin-top:9px;}
.hrp-kpi-trend svg{color:var(--k);flex-shrink:0;}
.hrp-kpi.is-zero .hrp-kpi-trend svg{color:var(--text-muted);}

/* ---- progress ring ---- */
.hrp-ring{flex-shrink:0;}
.hrp-ring-txt{fill:var(--text-primary);font-weight:650;}

/* ---- avatar ---- */
.hrp-avatar{border-radius:50%;display:flex;align-items:center;justify-content:center;
  color:#fff;font-weight:700;flex-shrink:0;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12);}

/* ---- section headers ---- */
.hrp-sec{display:flex;align-items:center;gap:9px;margin:24px 0 14px;font-size:14px;font-weight:650;color:var(--text-primary);letter-spacing:.2px;}
.hrp-sec svg{color:var(--accent);}

/* ---- record cards ---- */
.hrp-card{background:var(--card-bg);border:1px solid var(--card-border);border-radius:14px;
  padding:16px 18px;margin-bottom:12px;animation:hrp-in .35s ease both;
  transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease;}
.hrp-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-card);border-color:var(--border-strong);}
.hrp-emp{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;}
.hrp-emp-left{display:flex;align-items:center;gap:13px;min-width:0;}
.hrp-name{font-size:15px;font-weight:600;color:var(--text-primary);display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.hrp-id{font-size:11px;color:var(--text-muted);font-family:ui-monospace,Menlo,monospace;margin-top:3px;}
.hrp-role{font-size:12px;color:var(--text-secondary);margin-top:4px;}
.hrp-meta{font-size:12.5px;color:var(--text-secondary);text-align:right;line-height:1.6;}
.hrp-ring-wrap{display:flex;flex-direction:column;align-items:center;gap:5px;flex-shrink:0;}
.hrp-ring-cap{font-size:11px;color:var(--text-muted);}
.hrp-chip{border:1px solid var(--border-soft);color:var(--text-secondary);background:var(--bg-app-2);
  padding:2px 10px;border-radius:6px;font-size:11px;font-weight:600;white-space:nowrap;}
.hrp-status{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:var(--text-secondary);}
.hrp-dot{width:7px;height:7px;border-radius:50%;display:inline-block;}
.hrp-reason{font-size:12.5px;color:var(--text-secondary);margin-top:10px;}
.hrp-reason b{color:var(--text-muted);font-weight:600;}

/* ---- phase group headers in checklist ---- */
.hrp-phase{display:flex;align-items:center;gap:8px;margin:14px 0 6px;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:.6px;color:var(--text-secondary);}
.hrp-phase:first-child{margin-top:2px;}
.hrp-phase-dot{width:9px;height:9px;border-radius:50%;border:2px solid var(--accent);}
.hrp-phase-dot.done{background:var(--accent);}
.hrp-phase-count{color:var(--text-muted);font-weight:600;letter-spacing:0;}

/* ---- empty state ---- */
.hrp-empty{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;
  padding:34px 20px;border:1px dashed var(--border-strong);border-radius:14px;background:var(--card-bg);}
.hrp-empty svg{color:var(--text-muted);}
.hrp-empty-title{font-size:14px;font-weight:600;color:var(--text-secondary);}
.hrp-empty-sub{font-size:12.5px;color:var(--text-muted);max-width:340px;}

/* ============ SCOPED native-widget overrides (this module only) ============ */

/* Tabs (react-aria based in Streamlit 1.59): accent underline + soft highlight */
.st-key-hrp-root [role="tablist"]{gap:4px;border-bottom:1px solid var(--border-soft);margin:2px 0 10px;}
.st-key-hrp-root [data-testid="stTab"]{border-radius:8px 8px 0 0;padding:8px 16px;margin-bottom:-1px;transition:background .15s ease;}
.st-key-hrp-root [data-testid="stTab"] p{color:var(--text-secondary);font-weight:600;transition:color .15s ease;}
.st-key-hrp-root [data-testid="stTab"]:hover{background:var(--bg-app-2);}
.st-key-hrp-root [data-testid="stTab"]:hover p{color:var(--text-primary);}
.st-key-hrp-root [data-testid="stTab"][aria-selected="true"]{background:var(--accent-soft);}
.st-key-hrp-root [data-testid="stTab"][aria-selected="true"] p{color:var(--accent);}
.st-key-hrp-root .react-aria-SelectionIndicator{background:var(--accent) !important;height:3px !important;}

/* Cards: consistent radius/border/pad on Streamlit's bordered containers */
.st-key-hrp-root [data-testid="stVerticalBlockBorderWrapper"]{border:1px solid var(--card-border) !important;
  border-radius:14px !important;background:var(--card-bg);padding:4px 6px;transition:border-color .15s ease;}
.st-key-hrp-root [data-testid="stVerticalBlockBorderWrapper"]:focus-within{border-color:var(--accent) !important;}

/* Expander (Module details / checklists): match the card/tile language */
.st-key-hrp-root [data-testid="stExpander"]{border:1px solid var(--card-border) !important;border-radius:12px !important;background:var(--card-bg);overflow:hidden;}
.st-key-hrp-root [data-testid="stExpander"] summary:hover{color:var(--accent);}

/* Form-field labels: small, uppercase, muted */
.st-key-hrp-root [data-testid="stWidgetLabel"] p,
.st-key-hrp-root [data-testid="stWidgetLabel"] label{font-size:11px !important;font-weight:600 !important;
  text-transform:uppercase;letter-spacing:.5px;color:var(--text-muted) !important;}
/* ...but keep checklist task text readable (normal case, not shouty) */
.st-key-hrp-root [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
.st-key-hrp-root [data-testid="stCheckbox"] label{font-size:13px !important;font-weight:400 !important;
  text-transform:none !important;letter-spacing:normal !important;color:var(--text-primary) !important;}

/* Inputs: accent border on hover/focus */
.st-key-hrp-root [data-baseweb="input"],
.st-key-hrp-root [data-baseweb="select"] > div,
.st-key-hrp-root [data-baseweb="textarea"]{transition:border-color .15s ease;}
.st-key-hrp-root [data-baseweb="input"]:hover,
.st-key-hrp-root [data-baseweb="select"] > div:hover,
.st-key-hrp-root [data-baseweb="textarea"]:hover,
.st-key-hrp-root [data-baseweb="input"]:focus-within,
.st-key-hrp-root [data-baseweb="textarea"]:focus-within{border-color:var(--accent) !important;}

/* Primary buttons: force the module accent (not Streamlit's default red) */
.st-key-hrp-root [data-testid="stBaseButton-primary"],
.st-key-hrp-root [data-testid="stBaseButton-primaryFormSubmit"]{
  background-color:var(--accent) !important;border-color:var(--accent) !important;color:#fff !important;}
.st-key-hrp-root [data-testid="stBaseButton-primary"]:hover,
.st-key-hrp-root [data-testid="stBaseButton-primaryFormSubmit"]:hover{
  background-color:var(--accent-hover) !important;border-color:var(--accent-hover) !important;}
</style>
"""


def _svg(paths: str, size: int = 18) -> str:
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


def _ring(pct: float, size: int = 46, stroke: int = 5, color: str = "var(--accent)") -> str:
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - max(0.0, min(1.0, pct)))
    c = size / 2
    return (f'<svg class="hrp-ring" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{c}" cy="{c}" r="{r:.1f}" fill="none" stroke="var(--bg-app-2)" stroke-width="{stroke}"/>'
            f'<circle cx="{c}" cy="{c}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
            f'transform="rotate(-90 {c} {c})"/>'
            f'<text x="50%" y="50%" dy="0.35em" text-anchor="middle" class="hrp-ring-txt" '
            f'style="font-size:{size * 0.29:.0f}px">{pct * 100:.0f}%</text></svg>')


def _avatar(name: str, size: int = 42) -> str:
    parts = [p for p in name.strip().split() if p]
    initials = (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper() if parts else "?"
    color = AVATAR_COLORS[sum(ord(ch) for ch in name) % len(AVATAR_COLORS)]
    return (f'<div class="hrp-avatar" style="width:{size}px;height:{size}px;background:{color};'
            f'font-size:{size * 0.38:.0f}px">{initials}</div>')


def _section(icon: str, text: str) -> None:
    st.markdown(f'<div class="hrp-sec">{_svg(icon, 16)}<span>{text}</span></div>', unsafe_allow_html=True)


def _status(status: str) -> str:
    return (f'<span class="hrp-status"><span class="hrp-dot" '
            f'style="background:{STATUS_DOT.get(status, "var(--text-muted)")}"></span>{status}</span>')


def _empty(icon: str, title: str, sub: str) -> None:
    st.markdown(f'<div class="hrp-empty">{_svg(icon, 30)}<div class="hrp-empty-title">{title}</div>'
                f'<div class="hrp-empty-sub">{sub}</div></div>', unsafe_allow_html=True)


def _kpi(label: str, trend: str, accent: str, muted: bool,
         icon: str = "", ring_pct: float | None = None, value: str = "") -> str:
    cls = "hrp-kpi is-zero" if muted else "hrp-kpi"
    if ring_pct is not None:
        lead = _ring(ring_pct, size=46, color=("var(--text-muted)" if muted else accent))
        body = f'<div><div class="hrp-kpi-lbl">{label}</div><div class="hrp-kpi-trend">{_svg(_I_TREND, 13)}{trend}</div></div>'
    else:
        lead = f'<div class="hrp-kpi-ic">{_svg(icon)}</div>'
        body = (f'<div><div class="hrp-kpi-val">{value}</div><div class="hrp-kpi-lbl">{label}</div>'
                f'<div class="hrp-kpi-trend">{_svg(_I_TREND, 13)}{trend}</div></div>')
    return (f'<div class="{cls}" style="--k:{accent}"><span class="hrp-kpi-accent"></span>{lead}{body}</div>')


def _phase_of(offset_days: int) -> str:
    if offset_days <= 0:
        return "Day 1"
    if offset_days <= 7:
        return "First Week"
    return "First Month"


@st.cache_resource
def _get_engine() -> HrProposalEngine:
    return HrProposalEngine()


def render_ui():
    """Renders the Streamlit frontend tab for HR Automation Proposal."""
    metadata = MODULE_REGISTRY["week2"]["hr_proposal"]
    engine = _get_engine()

    st.markdown(_CSS, unsafe_allow_html=True)

    # Keyed root container -> `.st-key-hrp-root` wrapper scopes all CSS below.
    with st.container(key="hrp-root"):
        st.markdown(f'''
        <div class="hero-wrap">
            <div class="hrp-badge">Business Automation Suite</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Assigned to: <strong>{metadata["developer"]}</strong> ({metadata["role"]})
            </div>
        </div>
        ''', unsafe_allow_html=True)

        with st.expander("Module details"):
            st.markdown(
                f"**Developer:** {metadata['email']}  \n"
                f"**Difficulty:** {metadata['difficulty']}  \n"
                f"**Stack:** {', '.join(metadata['tech'])}  \n\n"
                f"{metadata['description']}"
            )

        cases = engine.get_onboarding_cases()
        n_cases = len(cases)
        pending_count = len(engine.list_leave_requests(status="Pending"))
        approved_count = len(engine.list_leave_requests(status="Approved"))
        avg_progress = (
            sum(engine.onboarding_progress(eid) for eid in cases["employee_id"]) / n_cases
            if n_cases else 0.0
        )

        st.markdown(
            '<div class="hrp-kpi-grid">'
            + _kpi("New Hires", f"{n_cases} in pipeline", "var(--accent)", n_cases == 0,
                   icon=_I_USERS, value=str(n_cases))
            + _kpi("Avg. Progress", f"across {n_cases} hire(s)", "var(--accent)", n_cases == 0,
                   ring_pct=avg_progress)
            + _kpi("Pending Leave", f"{pending_count} to review", "var(--warning)", pending_count == 0,
                   icon=_I_CLOCK, value=str(pending_count))
            + _kpi("Approved Leave", f"{approved_count} granted this week", "var(--success)", approved_count == 0,
                   icon=_I_CHECK, value=str(approved_count))
            + '</div>',
            unsafe_allow_html=True,
        )

        onboarding_tab, leave_tab = st.tabs(["Onboarding Pipeline", "Leave Requests"])

        with onboarding_tab:
            _render_onboarding_tab(engine, cases)

        with leave_tab:
            _render_leave_tab(engine)


def _render_onboarding_tab(engine: HrProposalEngine, cases):
    _section(_I_USERPLUS, "Register a New Hire")
    st.caption("Generates a standard onboarding checklist with due dates based on the start date.")

    with st.container(border=True):
        with st.form("onboarding_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name")
                email = st.text_input("Company Email")
                department = st.selectbox("Department", DEPARTMENTS)
            with col2:
                role = st.text_input("Job Role / Title")
                start_date = st.date_input("Start Date", value=date.today())

            submitted = st.form_submit_button("Create Onboarding Case", type="primary")

        if submitted:
            try:
                result = engine.create_onboarding_case(full_name, email, department, role, start_date)
                st.success(f"Onboarding case created for **{full_name}** ({result['employee']['employee_id']}).")
                st.rerun()
            except HrProposalError as exc:
                st.error(str(exc))

    _section(_I_USERS, "Active Onboarding Cases")

    if cases.empty:
        _empty(_I_USERS, "No onboarding cases yet",
               "Register your first hire above to generate their onboarding checklist automatically.")
        return

    today = date.today()
    for _, case in cases.iterrows():
        employee_id = case["employee_id"]
        tasks = engine.get_onboarding_tasks(employee_id)
        progress = engine.onboarding_progress(employee_id)
        completed_count = int((tasks["completed"] == "True").sum())

        st.markdown(f'''
        <div class="hrp-card">
            <div class="hrp-emp">
                <div class="hrp-emp-left">
                    {_avatar(case["full_name"])}
                    <div>
                        <div class="hrp-name">{case["full_name"]} <span class="hrp-chip">{case["department"]}</span></div>
                        <div class="hrp-id">{employee_id}</div>
                        <div class="hrp-role">{case["role"]} &middot; Start date {case["start_date"]}</div>
                    </div>
                </div>
                <div class="hrp-ring-wrap">
                    {_ring(progress, size=52, stroke=5)}
                    <div class="hrp-ring-cap">{completed_count}/{len(tasks)} tasks</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        with st.expander(f"Checklist — {case['full_name']} ({completed_count}/{len(tasks)})"):
            start = date.fromisoformat(case["start_date"])
            last_phase = None
            for _, task in tasks.iterrows():
                due = date.fromisoformat(task["due_date"])
                phase = _phase_of((due - start).days)
                if phase != last_phase:
                    phase_tasks = tasks[tasks["due_date"].apply(
                        lambda d: _phase_of((date.fromisoformat(d) - start).days) == phase)]
                    phase_done = int((phase_tasks["completed"] == "True").sum())
                    dot_cls = "hrp-phase-dot done" if phase_done == len(phase_tasks) else "hrp-phase-dot"
                    st.markdown(
                        f'<div class="hrp-phase"><span class="{dot_cls}"></span>{phase}'
                        f'<span class="hrp-phase-count">{phase_done}/{len(phase_tasks)}</span></div>',
                        unsafe_allow_html=True,
                    )
                    last_phase = phase

                is_done = task["completed"] == "True"
                overdue_tag = " · :red[overdue]" if (not is_done and due < today) else ""
                checked = st.checkbox(
                    f"{task['task']}  \n:gray[due {task['due_date']}]{overdue_tag}",
                    value=is_done,
                    key=f"task_{task['task_id']}",
                )
                if checked != is_done:
                    engine.set_task_completed(task["task_id"], checked)
                    st.rerun()


def _render_leave_tab(engine: HrProposalEngine):
    _section(_I_EDIT, "Submit a Leave Request")

    with st.container(border=True):
        with st.form("leave_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                employee_name = st.text_input("Employee Name")
                employee_email = st.text_input("Employee Email")
                leave_type = st.selectbox("Leave Type", LEAVE_TYPES)
            with col2:
                start_date = st.date_input("Start Date", value=date.today(), key="leave_start")
                end_date = st.date_input("End Date", value=date.today(), key="leave_end")

            reason = st.text_area("Reason for Leave")
            submitted = st.form_submit_button("Submit Leave Request", type="primary")

        if submitted:
            try:
                ticket = engine.submit_leave_request(
                    employee_name, employee_email, leave_type, start_date, end_date, reason
                )
                st.success(
                    f"Ticket **{ticket['ticket_id']}** filed for {ticket['leave_days']} day(s), "
                    f"status: {ticket['status']}."
                )
                st.rerun()
            except HrProposalError as exc:
                st.error(str(exc))

    _section(_I_TICKET, "Leave Tickets")

    status_filter = st.segmented_control(
        "Filter by status", ["All", "Pending", "Approved", "Rejected"], default="All"
    )
    requests = engine.list_leave_requests(status=None if status_filter in (None, "All") else status_filter)

    if requests.empty:
        _empty(_I_TICKET, "No leave tickets", "Submit a leave request above to open a new ticket.")
        return

    for _, ticket in requests.iloc[::-1].iterrows():
        status = ticket["status"]
        notes_html = (
            f'<div class="hrp-reason"><b>Reviewer notes:</b> {ticket["reviewer_notes"]}</div>'
            if ticket["reviewer_notes"] else ""
        )
        st.markdown(f'''
        <div class="hrp-card">
            <div class="hrp-emp">
                <div class="hrp-emp-left">
                    {_avatar(ticket["employee_name"])}
                    <div>
                        <div class="hrp-name">{ticket["employee_name"]} <span class="hrp-chip">{ticket["leave_type"]}</span></div>
                        <div class="hrp-id">{ticket["ticket_id"]}</div>
                    </div>
                </div>
                <div class="hrp-meta">{_status(status)}<br>{ticket["start_date"]} &rarr; {ticket["end_date"]} &middot; {ticket["leave_days"]} day(s)</div>
            </div>
            <div class="hrp-reason"><b>Reason:</b> {ticket["reason"] or "—"}</div>
            {notes_html}
        </div>
        ''', unsafe_allow_html=True)

        if status == "Pending":
            with st.container(border=True):
                notes = st.text_input("Reviewer notes (optional)", key=f"notes_{ticket['ticket_id']}")
                approve_col, reject_col = st.columns(2)
                with approve_col:
                    if st.button("Approve", key=f"approve_{ticket['ticket_id']}", type="primary", use_container_width=True):
                        engine.update_leave_status(ticket["ticket_id"], "Approved", notes)
                        st.rerun()
                with reject_col:
                    if st.button("Reject", key=f"reject_{ticket['ticket_id']}", use_container_width=True):
                        engine.update_leave_status(ticket["ticket_id"], "Rejected", notes)
                        st.rerun()
