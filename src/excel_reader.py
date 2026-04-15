import openpyxl
from datetime import date, datetime


def _normalize_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromordinal(datetime(1899, 12, 30).toordinal() + int(value)).date()
        except (ValueError, OverflowError):
            return None
    return None


def read_schedule(path: str) -> list[dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = []

    header_skipped = False
    for row in ws.iter_rows(values_only=True):
        if not header_skipped:
            header_skipped = True
            continue

        name = row[0]
        raw_date = row[1]

        if not name or not str(name).strip():
            continue

        parsed_date = _normalize_date(raw_date)
        if parsed_date is None:
            continue

        rows.append({
            "vendor_name": str(name).strip(),
            "visit_date": parsed_date,
        })

    wb.close()
    return rows


def read_directory(path: str) -> list[dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = []

    header_skipped = False
    for row in ws.iter_rows(values_only=True):
        if not header_skipped:
            header_skipped = True
            continue

        name = row[0]
        email = row[1]

        if not name or not str(name).strip():
            continue
        if not email or not str(email).strip():
            continue

        rows.append({
            "vendor_name": str(name).strip(),
            "email": str(email).strip(),
        })

    wb.close()
    return rows


def get_visits_for_date(schedule: list[dict], target: date) -> list[dict]:
    return [row for row in schedule if row["visit_date"] == target]


def lookup_vendor_email(vendor_name: str, directory: list[dict]) -> str | None:
    target = vendor_name.lower()
    for entry in directory:
        if entry["vendor_name"].lower() == target:
            return entry["email"]
    return None