"""Safe INSERT query with parameterization to prevent SQL injection.

Args:
    conn: Database connection object
    table: str - Table name
    data: dict - Column-value pairs to insert

Returns:
    dict: {'row_id': int|None, 'rows_affected': int, 'error': str|None}
"""
import re


def query_insert(conn, table, data):
    """Execute safe parameterized INSERT query."""
    try:
        # Validate table name (alphanumeric + underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', table):
            return {'row_id': None, 'rows_affected': 0, 'error': 'Invalid table name'}

        if not data or not isinstance(data, dict):
            return {'row_id': None, 'rows_affected': 0, 'error': 'Data must be non-empty dict'}

        # Validate column names
        for col in data.keys():
            if not re.match(r'^[a-zA-Z0-9_]+$', col):
                return {'row_id': None, 'rows_affected': 0, 'error': f'Invalid column: {col}'}

        # Build parameterized INSERT query
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        params = list(data.values())

        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        return {
            'row_id': cursor.lastrowid,
            'rows_affected': cursor.rowcount,
            'error': None
        }

    except Exception as e:
        return {'row_id': None, 'rows_affected': 0, 'error': str(e)}


# Tests
def test_query_insert():
    """Test INSERT query with parameterization."""
    import sqlite3
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db = f.name

    conn = sqlite3.connect(db)
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')

    # Test valid insert
    result = query_insert(conn, 'users', {'name': 'Alice', 'email': 'alice@example.com'})
    assert result['error'] is None
    assert result['row_id'] is not None
    assert result['rows_affected'] == 1

    # Test invalid table name (SQL injection prevention)
    result = query_insert(conn, 'users; DROP TABLE users--', {'name': 'Bob'})
    assert result['error'] == 'Invalid table name'

    # Test invalid column name
    result = query_insert(conn, 'users', {'name; DROP--': 'Bob'})
    assert 'Invalid column' in result['error']

    conn.close()
    os.unlink(db)
