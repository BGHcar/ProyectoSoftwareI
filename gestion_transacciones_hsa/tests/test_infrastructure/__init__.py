# tests/test_infrastructure/__init__.py
import os
import sys

# Añadir el directorio raíz al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)