"""Simple cache retrieval with TTL support.

Args:
    cache: dict - Cache storage dictionary
    key: str - Cache key
    default: any - Default value if key not found or expired

Returns:
    dict: {'value': any, 'found': bool, 'expired': bool}
"""
import time


def cache_get(cache, key, default=None):
    """Retrieve value from cache with TTL check."""
    try:
        if not isinstance(cache, dict):
            return {'value': default, 'found': False, 'expired': False}

        if key not in cache:
            return {'value': default, 'found': False, 'expired': False}

        entry = cache[key]

        # Check if entry has TTL
        if isinstance(entry, dict) and 'value' in entry:
            # Entry with metadata
            value = entry['value']
            expires_at = entry.get('expires_at')

            # Check expiration
            if expires_at is not None:
                if time.time() > expires_at:
                    # Expired
                    return {'value': default, 'found': True, 'expired': True}

            return {'value': value, 'found': True, 'expired': False}
        else:
            # Simple value without metadata
            return {'value': entry, 'found': True, 'expired': False}

    except Exception as e:
        return {'value': default, 'found': False, 'expired': False}
