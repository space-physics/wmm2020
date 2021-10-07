"""Get the path of this directory. Ugh."""
# Find the source directory that holds WMM.COF
try:  # Doesn't exists on all Python Versions
    import importlib.resources
    SDIR = importlib.resources.files('wmm2020')
except (NameError, Exception):
    try:  # Not really good for executables.
        from pathlib import Path
        SDIR = Path(__file__).parent
    except (ImportError, Exception):
        try:  # Compatibility support
            import importlib_resources
            SDIR = importlib_resources.files('wmm2020')
        except (ImportError, Exception):
            try:  # Compatibility support
                import resource_man
                SDIR = resource_man.files('wmm2020')
            except (ImportError, Exception):
                SDIR = Path()


__all__ = ['SDIR']
