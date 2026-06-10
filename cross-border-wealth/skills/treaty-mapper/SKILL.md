---
name: treaty-mapper
description: >
  Map the bilateral tax treaty network between jurisdictions. Find optimal routing
  paths to minimize withholding tax on dividends, interest, and royalties. Check
  LOB/PPT eligibility. Verify treaty rates against current text.
argument-hint: '[jurisdiction pair | "from X to Y" | "route dividends from A to B" | --verify]'
tools:
  - westlaw_oecd_get_treaty
  - westlaw_oecd_model_convention
  - westlaw_oecd_commentary
  - westlaw_oecd_mli_status
  - web_search
categories:
  - tax
  - structuring
version: 0.1.0
---

# /treaty-mapper

Maps the bilateral tax treaty network and finds optimal routing paths for cross-border flows. The chessboard skill — treaties are the squares, flows are the pieces.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` for existing treaty network and jurisdiction footprint.

2. **Determine the query.** From $ARGUMENTS:
   - **Direct lookup:** "What's the WHT on dividends from Singapore to Netherlands?" → look up the specific treaty rate
   - **Route optimization:** "Route royalties from US OpCo to ultimate beneficiary in Taiwan" → find the path through the treaty network that minimizes total WHT
   - **Network map:** "Map all treaty routes from Ireland" → show the full treaty network from a jurisdiction
   - **Verification:** `--verify` → re-verify all treaty positions in the practice profile

3. **For each treaty lookup:**
   - Search for the current bilateral tax treaty between the two jurisdictions
   - Find the applicable article (typically: Art. 10 dividends, Art. 11 interest, Art. 12 royalties)
   - Record: treaty rate, conditions (e.g., "10% if beneficial owner holds ≥25% capital"), effective date
   - Check for protocols or amendments that modify the rate
   - Check MLI impact (does the MLI modify this treaty? What reservations apply?)
   - Verify via web search against the treaty text or an authoritative treaty database

4. **For route optimization:**
   - Identify all possible paths from source to destination through intermediate jurisdictions
   - For each path, calculate the total withholding cost at each border crossing
   - For each intermediate jurisdiction, check:
     - Is there a participation exemption that eliminates tax on receipt?
     - Does the intermediate entity qualify for the treaty (LOB/PPT)?
     - What substance is needed in the intermediate jurisdiction?
     - What is the cost of maintaining the intermediate entity?
   - Rank paths by: total WHT cost → substance cost → complexity → defensibility

5. **Produce the route analysis:**

   ```
   Route: US OpCo → [IE HoldCo] → [NL HoldCo] → TW Ultimate Beneficiary

   Leg 1: US → IE (dividend)
     Treaty rate: 5% (Art. 10(2), ≥10% ownership)
     IE tax on receipt: 0% (participation exemption)
     Substance needed: [level]

   Leg 2: IE → NL (dividend)
     Treaty rate: 0% (EU Parent-Subsidiary Directive)
     NL tax on receipt: 0% (participation exemption)
     Substance needed: [level]

   Leg 3: NL → TW (dividend)
     Treaty rate: 10% (NL-TW treaty, Art. 10)
     TW tax on receipt: [rate]

   Total WHT: 5% + 0% + 10% = ~14.5% effective
   vs. Direct (US → TW): 30% (no treaty)
   Saving: ~15.5 percentage points
   ```

6. **Flag treaty shopping risk.** For each intermediate entity:
   - PPT risk: would a reasonable person conclude the arrangement's principal purpose was obtaining the treaty benefit?
   - LOB risk: does the entity satisfy the applicable LOB test?
   - Beneficial ownership: is the entity the beneficial owner, or just a conduit?
   - Tag: ✅ Defensible | ⚠️ PPT risk | ❌ Likely denied

7. **Offer next steps:**

   > **What next?**
   > 1. **Implement** — I'll design the entities needed for route [N] with substance specifications
   > 2. **Compare routes** — I'll analyze the top 3 routes side by side
   > 3. **Deep dive on treaty** — I'll pull the full treaty text for [treaty pair]
   > 4. **Case research** — I'll find cases on treaty shopping / PPT challenges in [jurisdiction]
   > 5. **HTML report** — interactive treaty route map with flow diagrams
   > 6. **Something else**
