"""Tests for cache_get brick."""
import time
from cache_get import cache_get


def test_cache_get():
    """Test cache retrieval functionality."""
    cache = {}

    # Test cache miss
    result = cache_get(cache, 'missing_key', default='default')
    assert result['found'] is False
    assert result['value'] == 'default'
    assert result['expired'] is False

    # Test simple cache hit
    cache['simple'] = 'value1'
    result = cache_get(cache, 'simple')
    assert result['found'] is True
    assert result['value'] == 'value1'
    assert result['expired'] is False

    # Test cache hit with metadata (no expiration)
    cache['meta'] = {'value': 'value2', 'expires_at': None}
    result = cache_get(cache, 'meta')
    assert result['found'] is True
    assert result['value'] == 'value2'
    assert result['expired'] is False

    # Test cache hit with valid TTL
    future = time.time() + 3600
    cache['valid'] = {'value': 'value3', 'expires_at': future}
    result = cache_get(cache, 'valid')
    assert result['found'] is True
    assert result['value'] == 'value3'
    assert result['expired'] is False

    # Test expired entry
    past = time.time() - 1
    cache['expired'] = {'value': 'value4', 'expires_at': past}
    result = cache_get(cache, 'expired', default='expired_default')
    assert result['found'] is True
    assert result['expired'] is True
    assert result['value'] == 'expired_default'

    # Test invalid cache type
    result = cache_get('not-a-dict', 'key', default='error')
    assert result['found'] is False
    assert result['value'] == 'error'

    print("All cache_get tests passed!")


if __name__ == '__main__':
    test_cache_get()
