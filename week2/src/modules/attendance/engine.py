# Attendance Automation Prototype - Engine Stub
# Assigned Developer: MUHAMMAD WASIM (Group Member)
# For SafeX Solutions Business Automation Research

from datetime import date
from typing import Optional


class AttendanceEngine:
    """
    Attendance Automation Engine.
    Tracks daily attendance per employee and generates summary reports.
    """

    VALID_STATUSES = {"present", "absent", "leave", "late"}

    def __init__(self):
        # records[employee_id] = { "YYYY-MM-DD": "present" | "absent" | ... }
        self.records: dict[str, dict[str, str]] = {}

    def mark_attendance(
        self,
        employee_id: str,
        status: str,
        record_date: Optional[date] = None
    ) -> dict:
        """Mark attendance for one employee on a given date (defaults to today)."""
        status = status.lower().strip()
        if status not in self.VALID_STATUSES:
            return {
                "status": "error",
                "message": f"Invalid status '{status}'. Must be one of {sorted(self.VALID_STATUSES)}"
            }

        record_date = record_date or date.today()
        date_key = record_date.isoformat()

        self.records.setdefault(employee_id, {})[date_key] = status

        return {
            "status": "success",
            "employee_id": employee_id,
            "date": date_key,
            "marked_as": status
        }

    def get_employee_history(self, employee_id: str) -> dict:
        """Return full attendance history for one employee."""
        return self.records.get(employee_id, {})

    def get_summary(self, employee_id: str) -> dict:
        """Return counts of each status for one employee."""
        history = self.records.get(employee_id, {})
        summary = {status: 0 for status in self.VALID_STATUSES}
        for status in history.values():
            summary[status] += 1
        summary["total_days_recorded"] = len(history)
        return summary

    def get_daily_report(self, record_date: date) -> dict:
        """Return attendance status of every employee for a specific date."""
        date_key = record_date.isoformat()
        report = {
            emp_id: day_records.get(date_key, "not_recorded")
            for emp_id, day_records in self.records.items()
        }
        return {"date": date_key, "report": report}

    def delete_record(self, employee_id: str, record_date: date) -> dict:
        """Remove a specific attendance record."""
        date_key = record_date.isoformat()
        if employee_id in self.records and date_key in self.records[employee_id]:
            del self.records[employee_id][date_key]
            return {"status": "success", "message": f"Deleted record for {employee_id} on {date_key}"}
        return {"status": "error", "message": "Record not found"}


# --- Example usage ---
if __name__ == "__main__":
    engine = AttendanceEngine()
    engine.mark_attendance("EMP001", "present")
    engine.mark_attendance("EMP002", "absent")
    engine.mark_attendance("EMP001", "late", record_date=date(2026, 7, 20))

    print(engine.get_summary("EMP001"))
    print(engine.get_daily_report(date.today()))
