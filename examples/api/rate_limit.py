"""Rate limiting brick."""
import time
from collections import defaultdict


_requests = defaultdict(list)


def rate_limit(client_id, max_requests=10, window_seconds=60):
    """
    Check if request is within rate limit.

    Args:
        client_id: Unique client identifier
        max_requests: Max requests per window
        window_seconds: Time window in seconds

    Returns:
        dict: {allowed: bool, remaining: int, reset_at: float}
    """
    now = time.time()
    cutoff = now - window_seconds

    # Remove old requests
    _requests[client_id] = [t for t in _requests[client_id] if t > cutoff]

    count = len(_requests[client_id])
    allowed = count < max_requests

    if allowed:
        _requests[client_id].append(now)
        remaining = max_requests - count - 1
    else:
        remaining = 0

    reset_at = _requests[client_id][0] + window_seconds if _requests[client_id] else now

    return {"allowed": allowed, "remaining": remaining, "reset_at": reset_at}


def test_rate_limit():
    """Test rate limiting."""
    result = rate_limit("test_client", max_requests=2, window_seconds=60)
    assert result["allowed"] is True
    assert result["remaining"] == 1
