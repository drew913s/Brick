"""Tests for query_insert brick."""
import sqlite3
from query_insert import query_insert


def test_query_insert():
    """Test safe INSERT query functionality."""
    # Setup test database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
    conn.commit()

    # Test basic insert
    result = query_insert(conn, 'users', {'name': 'Alice', 'email': 'alice@test.com'})
    assert result['error'] is None
    assert result['rows_affected'] == 1
    assert result['row_id'] is not None

    # Verify data was inserted
    cursor.execute('SELECT name, email FROM users WHERE id = ?', (result['row_id'],))
    row = cursor.fetchone()
    assert row[0] == 'Alice'
    assert row[1] == 'alice@test.com'

    # Test SQL injection prevention (table name)
    result = query_insert(conn, 'users; DROP TABLE users;', {'name': 'Bob'})
    assert result['error'] is not None
    assert 'Invalid table name' in result['error']

    # Test SQL injection prevention (column name)
    result = query_insert(conn, 'users', {"name' OR '1'='1": 'Bob'})
    assert result['error'] is not None
    assert 'Invalid column' in result['error']

    # Test empty data
    result = query_insert(conn, 'users', {})
    assert result['error'] is not None

    conn.close()
    print("All query_insert tests passed!")


if __name__ == '__main__':
    test_query_insert()
