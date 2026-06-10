# Skill Evaluation Framework

This document defines how to write, run, and score evaluations for Legal Engineering plugin skills.

## Overview

Evals verify that skills produce correct, complete, and well-structured outputs for known inputs. They catch regressions when skills are modified and validate new skills before merge.

## Eval File Format

Evals are stored as JSON files in `scripts/evals/` with the naming convention `{skill-name}.eval.json`.

### Schema

```json
{
  "$schema": "./eval-schema.json",
  "skill": "adversarial-analysis",
  "plugin": "cross-border-wealth",
  "version": "1.0.0",
  "evals": [
    {
      "id": "eval-001",
      "name": "Basic treaty shopping position test",
      "description": "Tests that adversarial-analysis correctly identifies arguments for and against a treaty shopping position",
      "input": {
        "prompt": "Stress-test this position: A Taiwan-resident individual routes dividends through a Netherlands BV to claim the NL-TW treaty rate of 10% instead of the domestic 21% withholding. The BV has one employee, a local director, and conducts treasury management.",
        "context": {
          "jurisdictions": ["TW", "NL"],
          "structure_type": "holding_company",
          "treaty": "NL-TW DTA"
        }
      },
      "assertions": [
        {
          "type": "contains",
          "target": "output",
          "value": "ADV-",
          "description": "Output must contain advocate argument IDs"
        },
        {
          "type": "contains",
          "target": "output",
          "value": "OPP-",
          "description": "Output must contain adversary argument IDs"
        },
        {
          "type": "regex",
          "target": "output",
          "pattern": "(Position upheld|Position upheld as stated).*?\\d+%",
          "description": "Must contain probability assessment with percentage"
        },
        {
          "type": "regex",
          "target": "output",
          "pattern": "(PPT|Principal Purpose Test|treaty shopping|beneficial owner)",
          "description": "Must reference relevant anti-avoidance doctrine"
        },
        {
          "type": "json_schema",
          "target": "structured_output",
          "schema": {
            "type": "object",
            "required": ["advocate_arguments", "adversary_arguments", "probability_assessment"],
            "properties": {
              "advocate_arguments": {
                "type": "array",
                "minItems": 2,
                "items": {
                  "type": "object",
                  "required": ["id", "argument", "strength"],
                  "properties": {
                    "id": { "type": "string", "pattern": "^ADV-\\d{3}$" },
                    "argument": { "type": "string" },
                    "strength": { "type": "number", "minimum": 1, "maximum": 10 }
                  }
                }
              },
              "adversary_arguments": {
                "type": "array",
                "minItems": 2,
                "items": {
                  "type": "object",
                  "required": ["id", "argument", "severity"],
                  "properties": {
                    "id": { "type": "string", "pattern": "^OPP-\\d{3}$" },
                    "argument": { "type": "string" },
                    "severity": { "type": "number", "minimum": 1, "maximum": 10 }
                  }
                }
              },
              "probability_assessment": {
                "type": "object",
                "required": ["upheld", "partial_denial", "full_denial"],
                "properties": {
                  "upheld": { "type": "number", "minimum": 0, "maximum": 100 },
                  "partial_denial": { "type": "number", "minimum": 0, "maximum": 100 },
                  "full_denial": { "type": "number", "minimum": 0, "maximum": 100 }
                }
              }
            }
          },
          "description": "Structured output must conform to adversarial-analysis schema"
        },
        {
          "type": "citation_valid",
          "target": "output",
          "jurisdiction": "TW",
          "description": "Any Taiwan citations must use correct format"
        },
        {
          "type": "citation_valid",
          "target": "output",
          "jurisdiction": "NL",
          "description": "Any Netherlands citations must use correct format"
        }
      ],
      "scoring": {
        "pass_threshold": 0.8,
        "weights": {
          "contains": 1.0,
          "regex": 1.0,
          "json_schema": 2.0,
          "citation_valid": 1.5
        }
      },
      "metadata": {
        "difficulty": "medium",
        "tags": ["treaty", "substance", "cross-border"],
        "author": "legal-engineering",
        "created": "2024-01-01"
      }
    }
  ]
}
```

## Assertion Types

### `contains`
Checks that the output contains a specific string (case-insensitive by default).

```json
{
  "type": "contains",
  "target": "output",
  "value": "ADV-001",
  "case_sensitive": false,
  "description": "Must reference first advocate argument"
}
```

**Parameters:**
- `value` (string, required): The substring to search for
- `case_sensitive` (boolean, optional, default: false): Whether match is case-sensitive
- `count` (integer, optional): Minimum number of occurrences required

### `regex`
Checks that the output matches a regular expression pattern.

```json
{
  "type": "regex",
  "target": "output",
  "pattern": "Probability.*?\\d+%",
  "flags": "si",
  "description": "Must contain probability with percentage"
}
```

**Parameters:**
- `pattern` (string, required): Regular expression pattern
- `flags` (string, optional): Regex flags (s=dotall, i=case-insensitive, m=multiline)
- `capture_group` (integer, optional): If set, asserts the captured group is non-empty

### `json_schema`
Validates that structured output (extracted from the response) conforms to a JSON Schema.

```json
{
  "type": "json_schema",
  "target": "structured_output",
  "schema": { ... },
  "description": "Output structure must match expected schema"
}
```

**Parameters:**
- `schema` (object, required): A valid JSON Schema (draft-07 or later)
- `extract_from` (string, optional): JSONPath or regex to extract the JSON from freeform text

**How structured output is extracted:**
1. If the skill returns a JSON code block, parse it directly
2. If `extract_from` is specified, use it to locate JSON within the response
3. Otherwise, attempt to parse any ```json fenced block in the output

### `citation_valid`
Verifies that legal citations in the output use the correct format for the specified jurisdiction.

```json
{
  "type": "citation_valid",
  "target": "output",
  "jurisdiction": "TW",
  "description": "Taiwan citations must use ROC format"
}
```

**Parameters:**
- `jurisdiction` (string, required): ISO country code or jurisdiction identifier
- `strict` (boolean, optional, default: false): If true, ALL citations must be verified as real

**Jurisdiction citation patterns:**

| Jurisdiction | Valid Patterns |
|---|---|
| `US` | Bluebook format: `*Case* v. *Case*, XXX U.S. XXX (YYYY)` |
| `UK` | OSCOLA: `*Case* [YYYY] UKSC/EWCA/EWHC XX` |
| `EU` | CURIA: `Case C-XXX/YY` or ECLI format |
| `TW` | `最高法院X年度台上字第X號判決`, `釋字第X號` |
| `NL` | ECLI:NL format or Hoge Raad citation |
| `DE` | BVerfG/BGH format with Aktenzeichen |
| `FR` | Cour de cassation / Conseil d'État format |

### `not_contains` (negative assertion)
Ensures the output does NOT contain a specific string.

```json
{
  "type": "not_contains",
  "target": "output",
  "value": "I cannot",
  "description": "Skill should not refuse the request"
}
```

### `length`
Checks output length constraints.

```json
{
  "type": "length",
  "target": "output",
  "min": 500,
  "max": 10000,
  "description": "Response should be substantial but not excessive"
}
```

## Running Evaluations

### Command

```bash
# Run all evals for a specific skill
./scripts/run-evals.sh --skill adversarial-analysis

# Run all evals for a plugin
./scripts/run-evals.sh --plugin cross-border-wealth

# Run a specific eval by ID
./scripts/run-evals.sh --eval-id eval-001

# Run all evals
./scripts/run-evals.sh --all

# Run with verbose output
./scripts/run-evals.sh --skill contract-review --verbose

# Run and output JSON results
./scripts/run-evals.sh --skill contract-review --output results.json
```

### Execution Flow

1. **Load eval file** — parse the JSON, validate against schema
2. **Prepare context** — set up the skill's expected environment (mock profile, etc.)
3. **Execute skill** — invoke the skill with the eval's `input.prompt` and `input.context`
4. **Capture output** — store raw text output and any structured output
5. **Run assertions** — evaluate each assertion against the captured output
6. **Score** — compute weighted score based on assertion results
7. **Report** — output pass/fail with detailed assertion results

### Environment Setup

Evals run in an isolated environment with:
- A mock practice profile (pre-populated CLAUDE.md)
- No network access to external MCP servers (unless explicitly configured)
- Deterministic model settings (temperature=0, seed fixed)
- Timeout of 120 seconds per eval

## Scoring Methodology

### Per-Assertion Scoring

Each assertion produces a binary result (pass=1.0, fail=0.0) or a partial score for graduated assertions.

### Weighted Score Calculation

```
eval_score = sum(assertion_score[i] * weight[assertion_type[i]]) / sum(weight[assertion_type[i]])
```

Default weights (can be overridden per eval):

| Assertion Type | Default Weight | Rationale |
|---|---|---|
| `contains` | 1.0 | Basic structural check |
| `not_contains` | 1.0 | Basic negative check |
| `regex` | 1.0 | Pattern matching |
| `json_schema` | 2.0 | Structural completeness is important |
| `citation_valid` | 1.5 | Citation accuracy is critical for legal tools |
| `length` | 0.5 | Length is a soft constraint |

### Pass/Fail Threshold

Default: `pass_threshold: 0.8` (80% weighted score required to pass)

Can be adjusted per eval:
- Critical skills (citation-verification): 0.9
- Creative skills (adversarial-analysis): 0.7
- Structural skills (matter-workspace): 0.85

### Aggregate Reporting

```
Skill Score = (passed_evals / total_evals) * 100%

Plugin Score = mean(all skill scores)

Overall Score = mean(all plugin scores)
```

### Result Format

```json
{
  "run_id": "eval-run-20240615-001",
  "timestamp": "2024-06-15T10:30:00Z",
  "skill": "adversarial-analysis",
  "plugin": "cross-border-wealth",
  "results": [
    {
      "eval_id": "eval-001",
      "name": "Basic treaty shopping position test",
      "status": "pass",
      "score": 0.92,
      "assertions": [
        { "type": "contains", "value": "ADV-", "result": "pass" },
        { "type": "contains", "value": "OPP-", "result": "pass" },
        { "type": "regex", "pattern": "...", "result": "pass" },
        { "type": "json_schema", "result": "fail", "error": "missing field: probability_assessment.partial_denial" },
        { "type": "citation_valid", "jurisdiction": "TW", "result": "pass" }
      ],
      "duration_ms": 45000,
      "model": "claude-opus-4-7",
      "token_usage": { "input": 2500, "output": 3800 }
    }
  ],
  "summary": {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "score": 0.92
  }
}
```

## Writing Good Evals

### Principles

1. **Test behavior, not wording.** Use `contains` and `regex` to check for concepts, not exact phrases.
2. **One eval, one scenario.** Don't test multiple skills in one eval.
3. **Include edge cases.** Test boundary conditions (minimal input, conflicting jurisdictions, ambiguous facts).
4. **Realistic inputs.** Use prompts that actual users would provide.
5. **Graduated difficulty.** Include easy (smoke test), medium (typical use), and hard (edge case) evals.
6. **Citation accuracy matters.** Always include `citation_valid` assertions for skills that produce legal citations.
7. **Avoid brittleness.** Don't assert on exact formatting that might legitimately vary.

### Eval Difficulty Levels

| Level | Purpose | Pass Threshold | Example |
|---|---|---|---|
| `smoke` | Basic functionality check | 0.95 | Does the skill produce any structured output? |
| `easy` | Standard use case | 0.85 | Simple NDA review with obvious red flags |
| `medium` | Typical complexity | 0.80 | Multi-jurisdiction treaty analysis |
| `hard` | Edge cases and ambiguity | 0.70 | Conflicting authorities, novel legal questions |
| `adversarial` | Attempts to break the skill | 0.60 | Misleading inputs, jurisdiction traps |

### Common Patterns

**Testing for completeness:**
```json
[
  { "type": "contains", "value": "## Executive Summary" },
  { "type": "contains", "value": "## Next Steps" },
  { "type": "regex", "pattern": "\\|.*\\|.*\\|" }
]
```

**Testing for balanced analysis:**
```json
[
  { "type": "regex", "pattern": "ADV-\\d{3}", "count": 3 },
  { "type": "regex", "pattern": "OPP-\\d{3}", "count": 3 },
  { "type": "contains", "value": "Probability" }
]
```

**Testing for jurisdiction awareness:**
```json
[
  { "type": "contains", "value": "Taiwan" },
  { "type": "contains", "value": "個人資料保護法" },
  { "type": "citation_valid", "jurisdiction": "TW" }
]
```

## Directory Structure

```
scripts/
├── eval-framework.md          # This document
├── eval-schema.json           # JSON Schema for eval files
├── run-evals.sh               # Eval runner script
└── evals/
    ├── adversarial-analysis.eval.json
    ├── contract-review.eval.json
    ├── regulatory-gap-analysis.eval.json
    ├── privacy-impact-assessment.eval.json
    ├── ai-governance-triage.eval.json
    ├── citation-verification.eval.json
    ├── salecraft-compliance.eval.json
    ├── taiwan-law-specialist.eval.json
    ├── legal-translation.eval.json
    └── matter-workspace.eval.json
```

## CI Integration

Evals can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/skill-evals.yml
name: Skill Evaluations
on:
  pull_request:
    paths:
      - 'cross-border-wealth/skills/**'
      - 'legal-pathways/skills/**'

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run affected skill evals
        run: |
          CHANGED_SKILLS=$(git diff --name-only ${{ github.event.pull_request.base.sha }} | grep 'skills/' | cut -d'/' -f3 | sort -u)
          for skill in $CHANGED_SKILLS; do
            ./scripts/run-evals.sh --skill "$skill" --output "results-${skill}.json"
          done
      - name: Check results
        run: |
          for f in results-*.json; do
            score=$(jq '.summary.score' "$f")
            if (( $(echo "$score < 0.8" | bc -l) )); then
              echo "FAIL: $f scored $score (threshold: 0.8)"
              exit 1
            fi
          done
```
