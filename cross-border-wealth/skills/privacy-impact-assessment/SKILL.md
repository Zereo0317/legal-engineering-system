---
name: privacy-impact-assessment
description: >
  Conduct a Privacy Impact Assessment (PIA) or Data Protection Impact Assessment
  (DPIA) for cross-border data flows. Covers GDPR Art. 35 methodology, Taiwan
  PDPA requirements, and transfer impact assessments.
argument-hint: '[processing activity | data flow | system name]'
tools:
  - westlaw_eu_compliance_search
  - westlaw_eu_compliance_article
  - westlaw_search_eu_law
  - westlaw_search_taiwan_judgments
  - westlaw_get_taiwan_statute
  - web_search
categories:
  - privacy
  - data-protection
  - compliance
version: 0.1.0
---

# /privacy-impact-assessment

Conducts a structured Privacy Impact Assessment (PIA) or DPIA for cross-border data processing activities. Follows GDPR Article 35 methodology while incorporating Taiwan PDPA requirements and assessing cross-border transfer mechanisms.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Scope the assessment.** Determine:
   - Processing activity or system under review
   - Data controller(s) and processor(s) involved
   - Jurisdictions involved (data origin, processing location, storage location)
   - Whether a full DPIA is required (GDPR Art. 35 threshold test):
     - Systematic and extensive profiling with significant effects?
     - Large-scale processing of special categories / criminal data?
     - Systematic monitoring of public areas?
     - New technologies with high-risk characteristics?
     - Two or more of the Article 29 WP criteria met?

3. **Data flow mapping.** Document:

   | Stage | Data | Source | Destination | Legal Basis | Transfer Mechanism |
   |---|---|---|---|---|---|
   | Collection | [categories] | Data subject (TW) | Controller (TW) | Consent / Art. 19 PDPA | N/A (domestic) |
   | Processing | [categories] | Controller (TW) | Processor (EU) | Legitimate interest | SCCs + supplementary measures |
   | Storage | [categories] | Processor (EU) | Sub-processor (US) | Contract | SCCs + TIA |
   | ... | ... | ... | ... | ... | ... |

4. **Necessity and proportionality assessment:**
   - Is the processing necessary for the stated purpose?
   - Could the purpose be achieved with less data?
   - Is the data minimization principle satisfied?
   - Are retention periods justified?
   - Is there a less intrusive alternative?

5. **Risk assessment matrix:**

   | # | Risk | Likelihood | Severity | Overall Risk | Affected Rights |
   |---|---|---|---|---|---|
   | R-001 | Unauthorized access to financial data | Medium | High | 🟠 High | Confidentiality, financial privacy |
   | R-002 | Cross-border transfer to inadequate country | Low | High | 🟡 Medium | Data sovereignty, remedies |
   | R-003 | Purpose creep beyond original consent | Medium | Medium | 🟡 Medium | Autonomy, purpose limitation |
   | ... | ... | ... | ... | ... | ... |

6. **Taiwan PDPA-specific requirements (個人資料保護法):**
   - Article 6: Restrictions on sensitive data (medical, genetics, sex life, health exam, criminal record)
   - Article 7: Consent requirements — specific, informed, freely given
   - Article 8/9: Notice obligations at collection
   - Article 19: Legal bases for non-public-sector processing
   - Article 20: Purpose limitation for use
   - Article 21: International transfer restrictions (competent authority may restrict)
   - Article 27: Industry-specific codes of conduct
   - Article 12: Security measures obligation

7. **Transfer Impact Assessment (TIA)** for each cross-border flow:
   - Destination country adequacy status
   - Laws and practices in destination that may impinge on data protection
   - Transfer mechanism in use (SCCs, BCRs, consent, necessity)
   - Supplementary measures needed (encryption, pseudonymization, contractual)
   - Effective remedies available to data subjects

8. **Mitigation measures:**

   | Risk # | Mitigation | Type | Residual Risk | Owner | Deadline |
   |---|---|---|---|---|---|
   | R-001 | Implement encryption at rest + MFA | Technical | 🟢 Low | IT Security | 30 days |
   | R-002 | Execute SCCs + supplementary measures | Legal | 🟡 Medium | Legal | 60 days |
   | R-003 | Implement purpose limitation controls + audit | Organizational | 🟢 Low | DPO | 45 days |

9. **DPIA report structure:**
   - Executive summary
   - Processing description and data flows
   - Necessity and proportionality
   - Risk assessment
   - Mitigation measures
   - Residual risk acceptance
   - DPO consultation record
   - Supervisory authority consultation (if required under Art. 36)

10. **Offer next steps:**
    > 1. **Full DPIA report** — formal document for regulatory file
    > 2. **Transfer mechanism** — I'll draft SCCs/supplementary measures for [specific transfer]
    > 3. **Privacy notice** — draft PDPA Art. 8 compliant notice
    > 4. **Consent mechanism** — design Art. 7 PDPA compliant consent flow
    > 5. **Vendor assessment** — evaluate processor's data protection posture
    > 6. **Something else**
