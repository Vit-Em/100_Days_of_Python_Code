"""
Central tracing utility for the Flashcard Application.
- Toggle via environment variable IC_ENABLED=1
- Timestamped output
- No-op when disabled or icecream missing
Usage:
    from .tracing import tracer
    tracer.ic({"event": "something", "details": 123})
"""
import os
from datetime import datetime

try:
    from icecream import ic as _ic
except Exception:  # icecream not installed
    _ic = None

class _Tracer:
    def __init__(self) -> None:
        self.enabled = os.getenv("IC_ENABLED") == "1"
        if _ic is not None and not self.enabled:
            try:
                _ic.disable()
            except Exception:
                pass

    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def ic(self, *args):
        if not self.enabled or _ic is None:
            return args[0] if args else None
        ts = self._timestamp()
        if len(args) == 1:
            return _ic({"ts": ts, "data": args[0]})
        return _ic({"ts": ts, "data": args})

tracer = _Tracer()
