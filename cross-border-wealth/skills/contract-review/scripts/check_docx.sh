#!/usr/bin/env bash
set -euo pipefail
python3 -c "import docx" 2>/dev/null && echo '{"available": true}' || echo '{"available": false, "install": "pip install python-docx"}'
