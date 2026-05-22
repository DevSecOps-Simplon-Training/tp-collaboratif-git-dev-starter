import sys
import types
from unittest.mock import patch, mock_open

# Intercepter l'open() de config.json avant l'import de app
config_json = '{"api": {"host": "localhost", "port": 5000, "route": "/api/logs", "log_file": "server.log"}}'

import builtins
_real_open = builtins.open

def _patched_open(path, *args, **kwargs):
    if str(path).endswith('config.json'):
        from io import StringIO
        import json
        return mock_open(read_data=config_json)()
    return _real_open(path, *args, **kwargs)

builtins.open = _patched_open

import app  # noqa: E402 — import après patch

builtins.open = _real_open  # restaurer pour les tests
