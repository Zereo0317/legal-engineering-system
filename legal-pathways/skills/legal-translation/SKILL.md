---
name: legal-translation
description: >
  Translate legal documents with precision, maintaining legal meaning across
  EN, ZH-TW, ZH-CN, FR, and DE. Produces terminology tables, preserves
  clause structure, and flags untranslatable legal concepts.
argument-hint: '[document | term | "EN→ZH-TW" | language pair]'
tools:
  - web_search
categories:
  - translation
  - multilingual
  - documentation
version: 0.1.0
---

# /legal-translation

Translates legal documents and terminology with legal precision — not just linguistic accuracy. Maintains the legal effect of language across jurisdictions, flags concepts that don't have direct equivalents, and produces terminology tables for consistent translation throughout a matter.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`.

2. **Identify translation parameters:**
   - Source language and target language(s)
   - Supported pairs: EN ↔ ZH-TW ↔ ZH-CN ↔ FR ↔ DE (any combination)
   - Document type: contract, legislation, court decision, regulatory filing, correspondence
   - Purpose: official filing, internal reference, client communication, academic
   - Jurisdiction context: which legal system's terminology should control?
   - Register: formal (court filing), professional (client memo), accessible (client explanation)

3. **Pre-translation analysis:**
   - Identify jurisdiction-specific legal terms that require special handling
   - Flag terms with no direct equivalent in target language
   - Note false friends (terms that look similar but have different legal meanings)
   - Identify defined terms that must be translated consistently throughout

4. **Translation principles:**

   | Principle | Explanation | Example |
   |---|---|---|
   | Legal equivalence over literal | Use the target jurisdiction's equivalent concept | "consideration" → 對價 (TW) not 考慮 |
   | Preserve legal effect | The translation must have the same legal consequence | "shall" → 應 (mandatory) not 將 (future) |
   | Flag non-equivalents | Some concepts don't translate — explain them | "trust" has no direct civil law equivalent |
   | Consistent terminology | Same English term = same target term throughout | Pick one translation and stick to it |
   | Structural preservation | Maintain clause numbering, cross-references | Art. 3(2)(a) → 第3條第2項第1款 |

5. **Terminology table.** For every translated document, produce:

   | Source Term | Target Term | Notes | Alternative |
   |---|---|---|---|
   | consideration | 對價 | Contract law; not "thoughtfulness" | 約因 (academic) |
   | fiduciary duty | 受託人義務 / 忠實義務 | No perfect TW equivalent; explain | 信賴義務 |
   | force majeure | 不可抗力 | Both systems have this concept | — |
   | representations and warranties | 聲明與保證 | Common but technically distinct in CL | 陳述與擔保 |
   | indemnification | 補償 / 賠償 | 補償 = make whole; 賠償 = damages | — |
   | governing law | 準據法 | PIL term | 適用法律 (informal) |

6. **Format preservation rules:**
   - Clause numbers: maintain original numbering system OR convert to target system (flag which)
   - Cross-references: update all internal cross-references if numbering changes
   - Defined terms: use consistent formatting (quotes, bold, or 「」)
   - Recitals/Whereas clauses: convert to target jurisdiction convention
   - Signature blocks: adapt to target jurisdiction practice
   - Dates: convert format (2024/03/15 → March 15, 2024 → 民國113年3月15日)

7. **Quality checks:**
   - [ ] All defined terms translated consistently
   - [ ] Cross-references still accurate after translation
   - [ ] Legal effect preserved (not just meaning)
   - [ ] Jurisdiction-specific formalities maintained
   - [ ] No false friends introduced
   - [ ] Untranslatable concepts flagged and explained
   - [ ] Register appropriate for stated purpose
   - [ ] Date and currency formats converted

8. **ZH-TW ↔ ZH-CN specific issues:**
   - Different legal terminology for same concept (ROC vs. PRC law)
   - 公司 (TW Company Act) vs. 公司 (PRC Company Law) — different legal frameworks
   - 個人資料保護法 (TW PDPA) vs. 个人信息保护法 (PRC PIPL) — not interchangeable
   - Traditional vs. simplified characters (obvious but important for official documents)
   - Taiwan uses 民國 year; PRC uses Western calendar

9. **Output format:**
   - Side-by-side bilingual (for review)
   - Target language only (for filing)
   - Annotated translation (with translator's notes for complex passages)
   - Terminology table appended

10. **Offer next steps:**
    > 1. **Full document translation** — complete translation with terminology table
    > 2. **Terminology review** — I'll produce a term list for approval before translating
    > 3. **Back-translation** — translate back to source to verify accuracy
    > 4. **Certification language** — add translator's certification for official use
    > 5. **Comparative terms** — terminology comparison across all supported languages
    > 6. **Something else**
