---
name: jurisdiction-scanner
description: >
  Compare jurisdictions for a specific structuring purpose — holding company,
  IP vehicle, trust, treasury, operating entity. Returns a scored comparison
  matrix across tax, treaties, substance, privacy, cost, and stability.
  The "shopping" skill for the legal engineering optimizer.
argument-hint: '[purpose] [jurisdiction list or "suggest"]'
tools:
  - westlaw_search_eu_law
  - westlaw_oecd_get_treaty
  - westlaw_oecd_mli_status
  - web_search
categories:
  - structuring
  - tax
  - research
version: 0.1.0
---

# /jurisdiction-scanner

Compares jurisdictions as building blocks for a specific structuring purpose. Each jurisdiction is a LEGO piece with specific properties — the scanner helps you pick the right pieces.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Clarify the purpose.** What kind of entity or arrangement is being placed? Options:
   - Holding company (pure equity holding)
   - IP holding vehicle (patents, trademarks, software, know-how)
   - Treasury / financing vehicle (intercompany loans, cash pooling)
   - Operating company (real employees, real customers)
   - Trust or foundation (wealth preservation, succession)
   - Investment vehicle (fund, VCC, SPC, LP)
   - Real estate holding
   - Headquarters / management company
   - Special purpose: [user specifies]

   If not clear from $ARGUMENTS, ask.

3. **Get the jurisdiction list.** From $ARGUMENTS, or if "suggest" or no list provided, suggest 5-8 jurisdictions commonly used for the stated purpose based on the practice profile's existing footprint.

   Common sets by purpose:
   | Purpose | Typical candidates |
   |---|---|
   | HoldCo | Netherlands, Luxembourg, Singapore, Hong Kong, UAE, Ireland, UK, Switzerland |
   | IP vehicle | Ireland, Netherlands, Luxembourg, Singapore, Switzerland, Cyprus, Malta |
   | Treasury | Luxembourg, Netherlands, Ireland, Singapore, Hong Kong |
   | Trust | BVI, Cayman, Jersey, Guernsey, Singapore, New Zealand, Liechtenstein, South Dakota |
   | Foundation | Liechtenstein, Panama, Netherlands, Curaçao |
   | Investment vehicle | Cayman, Luxembourg, Singapore (VCC), Ireland (ICAV), BVI, Delaware |
   | Real estate | jurisdiction of the property + Luxembourg, Netherlands |

4. **For each jurisdiction, assess these dimensions** (use web search to verify current data):

   ### A. Corporate Tax
   - Headline corporate tax rate
   - Effective rate after incentives / IP box / special regimes
   - Participation exemption (dividends from subsidiaries)
   - Capital gains exemption on disposal of participations
   - CFC rules that could attribute income upstream
   - Minimum tax (Pillar Two / domestic minimum tax)

   ### B. Withholding Tax
   - Domestic WHT on dividends, interest, royalties (without treaty)
   - Key treaty rates to/from the client's primary jurisdictions
   - EU Parent-Subsidiary Directive / Interest & Royalties Directive (if EU)

   ### C. Treaty Network
   - Number of tax treaties in force
   - Quality of treaty network (does it cover the client's key jurisdictions?)
   - LOB / PPT provisions in key treaties
   - MLI status and reservations

   ### D. Substance Requirements
   - Economic substance regime (if any)
   - Minimum substance indicators (employees, office, directors, expenditure)
   - Cost of maintaining adequate substance
   - Director residency requirements

   ### E. Privacy & Confidentiality
   - UBO register (public / restricted / none)
   - CRS / FATCA participation
   - Exchange of information agreements
   - Banking secrecy status
   - Trust registration requirements

   ### F. Setup & Maintenance Cost
   - Incorporation cost
   - Annual maintenance (registered agent, filing, audit)
   - Cost of local directors / substance providers
   - Timeline to incorporate

   ### G. Stability & Reputation
   - Political stability
   - Rule of law / judicial quality
   - EU/OECD grey/black list status
   - Reputational perception (is this jurisdiction seen as a "tax haven"?)

   ### H. Special Considerations
   - Immigration / visa programs linked to investment
   - Crypto / digital asset regulations
   - Sharia compliance (for Gulf-connected clients)
   - Language of legal system
   - Time zone alignment with client operations

5. **Build the comparison matrix.** Produce a table with jurisdictions as columns and dimensions as rows, with scores (🟢 / 🟡 / 🟠 / 🔴) and key data points.

6. **Rank and recommend.** Score each jurisdiction for the stated purpose considering the practice profile's risk posture and existing footprint. The best jurisdiction is not always the cheapest — it's the one that fits the overall structure with the least friction.

7. **Offer next steps:**

   > **What next?**
   > 1. **Deep dive** — I'll do a full analysis of [top-ranked jurisdiction] for this purpose
   > 2. **Structure design** — I'll design a structure using [recommended jurisdiction] and connect it to your existing entities
   > 3. **Treaty mapper** — I'll map the treaty routes from [jurisdiction] to your operating jurisdictions
   > 4. **HTML report** — interactive comparison matrix with sortable columns and heat map
   > 5. **Something else**

## Verification

All tax rates, treaty rates, and regulatory data are verified via web search before inclusion. Each data point is tagged with its source. If a data point cannot be verified, it's tagged `[model knowledge — verify]`. The reviewer note lists which jurisdictions' data was web-verified and which relied on model knowledge.
