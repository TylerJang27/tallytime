
def _coalesce(val, default):
    try:
        if val is None or len(val) == 0:
            return default
        return val
    except Exception:
        return default
