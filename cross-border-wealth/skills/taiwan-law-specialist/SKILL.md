---
name: taiwan-law-specialist
description: >
  Taiwan-specific legal analysis covering Personal Data Protection Act (個人資料保護法),
  Consumer Protection Act (消費者保護法), Fair Trade Act (公平交易法), Company Act
  (公司法), and Securities and Exchange Act (證券交易法). Bilingual analysis with
  proper Taiwan citation format.
argument-hint: '[legal question | statute | "PDPA" | "CPA" | "FTA" | "Company Act"]'
tools:
  - westlaw_search_taiwan_judgments
  - westlaw_get_taiwan_statute
  - westlaw_search_taiwan_interpretations
  - web_search
categories:
  - taiwan
  - domestic-law
  - specialist
version: 0.1.0
---

# /taiwan-law-specialist

Provides Taiwan-specific legal analysis with bilingual (English/Traditional Chinese) output and proper citation formatting. Covers the major regulatory frameworks relevant to cross-border wealth structures, technology companies, and commercial operations in Taiwan.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Identify the legal question and applicable framework(s):**

   | Framework | Chinese Name | Key Areas |
   |---|---|---|
   | Personal Data Protection Act | 個人資料保護法 (個資法) | Data collection, processing, international transfer, breach notification |
   | Consumer Protection Act | 消費者保護法 (消保法) | Distance selling, unfair terms, product liability, advertising |
   | Fair Trade Act | 公平交易法 (公平法) | Unfair competition, misleading advertising, monopoly, mergers |
   | Company Act | 公司法 | Incorporation, governance, directors' duties, shareholder rights |
   | Securities and Exchange Act | 證券交易法 (證交法) | Public offerings, insider trading, disclosure, tender offers |
   | Business Mergers and Acquisitions Act | 企業併購法 | M&A structures, tax incentives, labor protections |
   | Financial Holding Company Act | 金融控股公司法 | Financial group structure, cross-selling, firewalls |
   | Money Laundering Control Act | 洗錢防制法 | AML obligations, suspicious transaction reporting |
   | Tax Collection Act | 稅捐稽徵法 | Tax administration, penalties, statute of limitations |
   | Income Tax Act | 所得稅法 | Corporate/individual income tax, withholding, CFC rules |

3. **Analysis methodology:**

   ### Step 1: Statutory text
   - Cite the exact article(s) in both Chinese and English translation
   - Note any recent amendments (修正) with effective dates
   - Identify relevant sub-articles (項/款/目)

   ### Step 2: Regulatory interpretation
   - Competent authority interpretive letters (主管機關函釋)
   - Ministry of Justice legal opinions (法務部法律字第XXX號函)
   - Relevant administrative rules and enforcement standards (施行細則)

   ### Step 3: Case law
   - Supreme Court decisions (最高法院判決)
   - High Court decisions (高等法院判決) where relevant
   - Constitutional Court interpretations (憲法法庭判決, formerly 大法官釋字)
   - Intellectual Property Court (智慧財產法院) for IP matters

   ### Step 4: Scholarly commentary
   - Leading academic views where law is unsettled
   - Note any divergence between academic position and court practice

4. **Citation format (Taiwan):**

   | Type | Format | Example |
   |---|---|---|
   | Constitutional interpretation (old) | 司法院大法官釋字第X號解釋 | 司法院大法官釋字第603號解釋 |
   | Constitutional judgment (new) | 憲法法庭111年憲判字第X號判決 | 憲法法庭111年憲判字第13號判決 |
   | Supreme Court civil | 最高法院X年度台上字第X號民事判決 | 最高法院110年度台上字第1234號民事判決 |
   | Supreme Court criminal | 最高法院X年度台上字第X號刑事判決 | 最高法院110年度台上字第567號刑事判決 |
   | High Court | X高等法院X年度X字第X號判決 | 臺灣高等法院109年度上字第890號判決 |
   | Interpretive letter | 主管機關X年X月X日X字第X號函 | 金管會112年3月15日金管銀法字第11200123號函 |
   | Statute article | [法律名稱]第X條第X項第X款 | 個人資料保護法第6條第1項第6款 |

5. **Bilingual output format.** For key legal conclusions:

   > **English:** Under PDPA Art. 21, the competent authority may restrict international transfers of personal data if the receiving country lacks adequate protection.
   >
   > **中文:** 依個人資料保護法第21條規定，非公務機關為國際傳輸個人資料，而接收國對於個人資料之保護未有適當之法規時，中央目的事業主管機關得限制之。

6. **Common pitfalls in Taiwan law:**
   - ROC year (民國) vs. Western year — 民國112年 = 2023 CE
   - "公司" can mean Company Act company or any business entity depending on context
   - PDPA applies to both public and non-public sectors (with different rules)
   - Consumer Protection Act Art. 22 makes advertising claims contractual — extremely powerful
   - Fair Trade Act has both administrative (公平會處分) and civil (損害賠償) remedies
   - CFC rules (受控外國企業, under 所得稅法§43-3) effective from 2023

7. **Regulatory authority mapping:**

   | Area | Authority | Chinese Name |
   |---|---|---|
   | Data protection | National Development Council | 國家發展委員會 (+ sector authorities) |
   | Consumer protection | Executive Yuan Consumer Protection Committee | 行政院消費者保護會 |
   | Fair trade | Fair Trade Commission | 公平交易委員會 |
   | Securities | Financial Supervisory Commission | 金融監督管理委員會 (金管會) |
   | Tax | Ministry of Finance / National Taxation Bureau | 財政部 / 國稅局 |
   | AML | Investigation Bureau, AMLD | 調查局洗錢防制處 |
   | Company registration | Ministry of Economic Affairs | 經濟部商業司 |

8. **Offer next steps:**
   > 1. **Deep dive** — detailed analysis of [specific article/issue]
   > 2. **Compliance checklist** — all requirements under [specific act] for your situation
   > 3. **Comparative** — compare Taiwan approach with [other jurisdiction]
   > 4. **Template** — draft [document type] compliant with Taiwan requirements
   > 5. **Regulatory filing** — guide for filing with [specific authority]
   > 6. **Case research** — find relevant court decisions on [specific point]
   > 7. **Something else**
