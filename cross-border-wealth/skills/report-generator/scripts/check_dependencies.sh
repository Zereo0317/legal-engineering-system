#!/usr/bin/env bash
set -euo pipefail

# check_dependencies.sh
# Detects available output format dependencies for report generation.
# Returns JSON indicating which formats are supported.

result='{"html": true'

# Check python3
if command -v python3 &>/dev/null; then
  result="${result}, \"python3\": true"
else
  result="${result}, \"python3\": false"
fi

# Check python-docx
if python3 -c "import docx" 2>/dev/null; then
  result="${result}, \"python_docx\": true, \"docx\": true"
else
  result="${result}, \"python_docx\": false, \"docx\": false, \"docx_install\": \"pip install python-docx\""
fi

# Check python-pptx
if python3 -c "import pptx" 2>/dev/null; then
  result="${result}, \"python_pptx\": true, \"pptx\": true"
else
  result="${result}, \"python_pptx\": false, \"pptx\": false, \"pptx_install\": \"pip install python-pptx\""
fi

# Check wkhtmltopdf
if command -v wkhtmltopdf &>/dev/null; then
  result="${result}, \"wkhtmltopdf\": true, \"pdf\": true"
else
  result="${result}, \"wkhtmltopdf\": false, \"pdf\": false, \"pdf_install\": \"apt install wkhtmltopdf / brew install wkhtmltopdf\""
fi

result="${result}}"
echo "$result"
