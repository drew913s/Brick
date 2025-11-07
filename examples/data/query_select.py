"""Safe SELECT query with parameterization to prevent SQL injection.

Args:
    conn: DB connection, table: str, columns: list[str], where: dict, limit: int

Returns:
    dict: {'rows': list[dict], 'count': int, 'error': str|None}
"""
import re

def query_select(conn, table, columns, where=None, limit=None):
    """Execute safe parameterized SELECT query."""
    try:
        # Validate table name (alphanumeric + underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', table):
            return {'rows': None, 'count': 0, 'error': 'Invalid table name'}

        # Validate column names
        for col in columns:
            if not re.match(r'^[a-zA-Z0-9_]+$', col):
                return {'rows': None, 'count': 0, 'error': f'Invalid column: {col}'}

        # Build parameterized query
        query = f"SELECT {', '.join(columns)} FROM {table}"
        params = []

        # Add WHERE clause with parameterization
        if where:
            conditions = []
            for key, value in where.items():
                if not re.match(r'^[a-zA-Z0-9_]+$', key):
                    return {'rows': None, 'count': 0, 'error': f'Invalid key: {key}'}
                conditions.append(f"{key} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(conditions)

        # Add LIMIT clause
        if limit:
            query += f" LIMIT {int(limit)}"

        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return {'rows': rows, 'count': len(rows), 'error': None}

    except Exception as e:
        return {'rows': None, 'count': 0, 'error': str(e)}
