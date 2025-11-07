"""CSV parsing brick."""
import csv
from io import StringIO


def csv_parse(csv_string, has_header=True):
    """
    Parse CSV string into list of dicts or lists.

    Args:
        csv_string: CSV data as string
        has_header: Whether first row is header

    Returns:
        dict: {data: list, error: str|None}
    """
    try:
        reader = csv.reader(StringIO(csv_string))
        rows = list(reader)

        if not rows:
            return {"data": [], "error": None}

        if has_header:
            headers = rows[0]
            data = [dict(zip(headers, row)) for row in rows[1:]]
        else:
            data = rows

        return {"data": data, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}


def test_csv_parse():
    """Test CSV parsing."""
    csv = "name,age\nAlice,30\nBob,25"
    result = csv_parse(csv)
    assert result["error"] is None
    assert len(result["data"]) == 2
    assert result["data"][0]["name"] == "Alice"


def test_csv_parse_no_header():
    """Test CSV without header."""
    csv = "Alice,30\nBob,25"
    result = csv_parse(csv, has_header=False)
    assert len(result["data"]) == 2
    assert result["data"][0] == ["Alice", "30"]
