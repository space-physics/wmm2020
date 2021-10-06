try:
    from .with_extension import wmm, transect, wmm_point
except (ImportError, Exception):
    from .base import wmm, transect, wmm_point
