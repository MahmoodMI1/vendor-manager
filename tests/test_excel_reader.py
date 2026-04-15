import pytest
from datetime import date, datetime
from src.excel_reader import (
    read_schedule,
    read_directory,
    get_visits_for_date,
    lookup_vendor_email,
)


SCHEDULE_PATH = "test_data/sample_schedule.xlsx"
DIRECTORY_PATH = "test_data/sample_directory.xlsx"


def test_read_schedule_returns_rows():
    rows = read_schedule(SCHEDULE_PATH)
    assert len(rows) >= 3


def test_read_schedule_has_required_keys():
    rows = read_schedule(SCHEDULE_PATH)
    for row in rows:
        assert "vendor_name" in row
        assert "visit_date" in row


def test_read_schedule_dates_are_date_objects():
    rows = read_schedule(SCHEDULE_PATH)
    for row in rows:
        assert isinstance(row["visit_date"], date)


def test_get_visits_for_date_filters_correctly():
    rows = read_schedule(SCHEDULE_PATH)
    matches = get_visits_for_date(rows, date(2026, 4, 16))
    names = [r["vendor_name"] for r in matches]
    assert "Acme Corp" in names
    assert "Beta Inc" in names
    assert "Smith LLC" not in names


def test_get_visits_for_date_no_matches():
    rows = read_schedule(SCHEDULE_PATH)
    matches = get_visits_for_date(rows, date(2099, 1, 1))
    assert matches == []


def test_read_directory_returns_rows():
    rows = read_directory(DIRECTORY_PATH)
    assert len(rows) >= 3


def test_lookup_vendor_email_exact_match():
    directory = read_directory(DIRECTORY_PATH)
    email = lookup_vendor_email("Acme Corp", directory)
    assert email == "contact@acme.com"


def test_lookup_vendor_email_case_insensitive():
    directory = read_directory(DIRECTORY_PATH)
    email = lookup_vendor_email("Smith LLC", directory)
    assert email == "info@smithllc.com"


def test_lookup_vendor_email_not_found():
    directory = read_directory(DIRECTORY_PATH)
    email = lookup_vendor_email("Nonexistent Vendor", directory)
    assert email is None


def test_lookup_vendor_email_duplicate_takes_first():
    directory = read_directory(DIRECTORY_PATH)
    email = lookup_vendor_email("Beta Inc", directory)
    assert email == "hello@betainc.com"


def test_read_schedule_skips_empty_rows(tmp_path):
    """Schedule with empty rows should not crash or return None entries."""
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Vendor Name", "Visit Date"])
    ws.append(["Acme Corp", datetime(2026, 4, 16)])
    ws.append([None, None])
    ws.append(["", datetime(2026, 4, 16)])
    ws.append(["Beta Inc", None])
    ws.append(["Valid Co", datetime(2026, 4, 16)])

    path = str(tmp_path / "sparse.xlsx")
    wb.save(path)

    rows = read_schedule(path)
    names = [r["vendor_name"] for r in rows]
    assert "Acme Corp" in names
    assert "Valid Co" in names
    assert len(rows) == 2