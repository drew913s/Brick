"""Tests for query_select brick."""
import sqlite3
from query_select import query_select


def test_query_select():
    """Test safe SELECT query functionality."""
    # Setup test database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER, name TEXT, email TEXT)')
    cursor.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@test.com')")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@test.com')")
    conn.commit()

    # Test basic select
    result = query_select(conn, 'users', ['id', 'name'])
    assert result['error'] is None
    assert result['count'] == 2
    assert result['rows'][0]['name'] == 'Alice'

    # Test with WHERE clause
    result = query_select(conn, 'users', ['name', 'email'], {'id': 1})
    assert result['error'] is None
    assert result['count'] == 1
    assert result['rows'][0]['email'] == 'alice@test.com'

    # Test with LIMIT
    result = query_select(conn, 'users', ['name'], limit=1)
    assert result['count'] == 1

    # Test SQL injection prevention (table name)
    result = query_select(conn, 'users; DROP TABLE users;', ['name'])
    assert result['error'] is not None
    assert 'Invalid table name' in result['error']

    # Test SQL injection prevention (column name)
    result = query_select(conn, 'users', ["name' OR '1'='1"])
    assert result['error'] is not None
    assert 'Invalid column' in result['error']

    # Test SQL injection prevention (WHERE clause)
    result = query_select(conn, 'users', ['name'], {"id' OR '1'='1": 1})
    assert result['error'] is not None

    conn.close()
    print("All query_select tests passed!")


if __name__ == '__main__':
    test_query_select()
