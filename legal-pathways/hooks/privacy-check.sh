#!/usr/bin/env bash
# Privacy & Privilege Classification Hook
# 3-tier classification system for content sensitivity
# Runs before Write, Edit, WebFetch, and MCP tool invocations

set -euo pipefail

# Read tool input from stdin (JSON with tool_name and tool_input)
INPUT=$(cat)

# Extract content to classify from the tool input
CONTENT=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    # Combine all string values for classification
    parts = []
    if isinstance(tool_input, dict):
        for v in tool_input.values():
            if isinstance(v, str):
                parts.append(v)
    elif isinstance(tool_input, str):
        parts.append(tool_input)
    print(' '.join(parts))
except:
    print('')
" 2>/dev/null || echo "")

# Classification function
classify_content() {
    local content="$1"
    
    # TIER 1: PRIVILEGED — attorney-client privilege indicators
    local privileged_patterns=(
        "legal opinion"
        "advice letter"
        "privileged"
        "confidential communication"
        "work product"
        "attorney-client"
        "lawyer-client"
        "solicitor-client"
        "律師與客戶通信"
        "法律意見"
        "特權通信"
        "attorney work product"
        "prepared at the direction of counsel"
    )
    
    for pattern in "${privileged_patterns[@]}"; do
        if echo "$content" | grep -qi "$pattern" 2>/dev/null; then
            echo '{"decision": "block", "reason": "Content contains attorney-client privilege indicators. Must use local processing only. Do not transmit to external services.", "classification": "privileged"}'
            return 0
        fi
    done
    
    # TIER 2: CONFIDENTIAL — sensitive but not privileged
    local confidential_patterns=(
        "confidential"
        "internal only"
        "not for distribution"
        "do not share"
        "restricted"
        "機密"
        "內部使用"
        "不得外傳"
        "限閱"
    )
    
    for pattern in "${confidential_patterns[@]}"; do
        if echo "$content" | grep -qi "$pattern" 2>/dev/null; then
            echo '{"decision": "warn", "reason": "Content classified as CONFIDENTIAL. Proceeding with anonymization note — ensure no PII or client-identifying information is transmitted.", "classification": "confidential"}'
            return 0
        fi
    done
    
    # TIER 3: PUBLIC — everything else
    echo '{"decision": "allow", "reason": "Content does not contain privilege or confidentiality indicators.", "classification": "public"}'
    return 0
}

# Run classification
if [ -n "$CONTENT" ]; then
    classify_content "$CONTENT"
else
    # No content to classify — allow by default
    echo '{"decision": "allow", "reason": "No content to classify.", "classification": "public"}'
fi
