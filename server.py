import json
import os
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_DATA_PATH = Path(__file__).parent / "data" / "harri.json"
_db: dict = json.loads(_DATA_PATH.read_text())


def _match(record: dict, field: str, value: str) -> bool:
    """Case-insensitive substring match on a field."""
    return value.lower() in str(record.get(field, "")).lower()


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="harri-mock",
    version="1.0.0",
    instructions=(
        "Mock Harri workforce management platform. Query employees, schedules, "
        "open shifts, time-off requests, compliance alerts, and labor data."
    ),
)

# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------

@mcp.tool()
def get_employees(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    role: Optional[str] = Field(default=None, description="Filter by role (partial match), e.g. Shift Lead"),
    status: Optional[str] = Field(default=None, description="Filter by status: active | onboarding"),
    minor: Optional[bool] = Field(default=None, description="If true, return only minors; if false, return only non-minors"),
) -> list[dict]:
    """List employees. Optionally filter by location, role, status, or minor flag."""
    results = _db["employees"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if role:
        results = [r for r in results if _match(r, "role", role)]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    if minor is not None:
        results = [r for r in results if r.get("minor") == minor]
    return results


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

@mcp.tool()
def get_schedule(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    employee_id: Optional[str] = Field(default=None, description="Filter by employee ID, e.g. EMP11"),
    date: Optional[str] = Field(default=None, description="Filter by shift date, e.g. 2026-07-13"),
    status: Optional[str] = Field(default=None, description="Filter by status: published | draft"),
) -> list[dict]:
    """List schedule entries. Optionally filter by location, employee, date, or status."""
    results = _db["schedule"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if employee_id:
        results = [r for r in results if r["employee_id"].upper() == employee_id.upper()]
    if date:
        results = [r for r in results if r["date"] == date]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    return results


# ---------------------------------------------------------------------------
# Open Shifts
# ---------------------------------------------------------------------------

@mcp.tool()
def get_open_shifts(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    date: Optional[str] = Field(default=None, description="Filter by shift date, e.g. 2026-07-14"),
) -> list[dict]:
    """List open (unfilled) shifts. Optionally filter by location or date."""
    results = _db["open_shifts"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if date:
        results = [r for r in results if r["date"] == date]
    return results


# ---------------------------------------------------------------------------
# Time-Off Requests
# ---------------------------------------------------------------------------

@mcp.tool()
def get_time_off_requests(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    employee_id: Optional[str] = Field(default=None, description="Filter by employee ID, e.g. EMP24"),
    status: Optional[str] = Field(default=None, description="Filter by status: approved | pending | denied"),
) -> list[dict]:
    """List time-off requests. Optionally filter by location, employee, or status."""
    results = _db["time_off_requests"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if employee_id:
        results = [r for r in results if r["employee_id"].upper() == employee_id.upper()]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    return results


# ---------------------------------------------------------------------------
# Compliance Alerts
# ---------------------------------------------------------------------------

@mcp.tool()
def get_compliance_alerts(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L004"),
    severity: Optional[str] = Field(default=None, description="Filter by severity: high | medium | low"),
    type: Optional[str] = Field(default=None, description="Filter by alert type, e.g. minor_work_permit_expiry"),
) -> list[dict]:
    """List compliance alerts. Optionally filter by location, severity, or alert type."""
    results = _db["compliance_alerts"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if severity:
        results = [r for r in results if _match(r, "severity", severity)]
    if type:
        results = [r for r in results if _match(r, "type", type)]
    return results


# ---------------------------------------------------------------------------
# Labor Summary
# ---------------------------------------------------------------------------

@mcp.tool()
def get_labor_summary(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match), e.g. 2026-06-08/2026-07-15"),
) -> list[dict]:
    """Return labor summary records (hours, cost, cost %). Optionally filter by location or period."""
    results = _db["labor_summary"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Onboarding
# ---------------------------------------------------------------------------

@mcp.tool()
def get_onboarding(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    status: Optional[str] = Field(default=None, description="Filter by onboarding status, e.g. in_progress"),
) -> list[dict]:
    """List onboarding records. Optionally filter by location or status."""
    results = _db["onboarding"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    return results


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

@mcp.tool()
def get_availability(
    employee_id: Optional[str] = Field(default=None, description="Filter by employee ID, e.g. EMP01"),
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L004"),
) -> list[dict]:
    """List employee availability records. Optionally filter by employee or location."""
    results = _db["availability"]
    if employee_id:
        results = [r for r in results if r["employee_id"].upper() == employee_id.upper()]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    return results


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

@mcp.tool()
def get_locations(
    id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L003"),
    name: Optional[str] = Field(default=None, description="Filter by location name (partial match), e.g. Daybreak"),
) -> list[dict]:
    """List locations. Optionally filter by ID or name."""
    results = _db["locations"]
    if id:
        results = [r for r in results if r["id"].upper() == id.upper()]
    if name:
        results = [r for r in results if _match(r, "name", name)]
    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
