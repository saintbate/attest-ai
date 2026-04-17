# Ideas Shortlist — Contingency Map

> **Purpose:** A ranked pipeline of candidate products we could pivot to
> if Attest doesn't hit the "two paid pilots by end of July" bar. Each
> candidate is scored on the same rubric as Attest so we can compare
> them honestly instead of chasing the shiniest recent paper.
>
> **Status:** Living document. Populate candidates only when Attest's
> outreach signal is ambiguous or negative — otherwise this is a
> distraction.
>
> **Stopping rule:** Max 8 candidates in the active list. When a ninth is
> added, the lowest-scoring one drops off. The top 3 are the only ones
> worth deep research. Everything below rank 5 is a holding pen.

---

## 1. Scoring rubric

Each dimension is scored 0–5. Max total: **35**. Pivot bar:
a candidate must score **>= 28** (Attest + 2) to justify
abandoning Attest early; **>= 30** to justify running in parallel.

| # | Dimension | 0 anchor | 5 anchor |
|---|---|---|---|
| 1 | **Urgency** | No forcing function; "nice to have." | Hard regulatory deadline / funding cycle / closing window with real penalty. |
| 2 | **Build accessibility** | Requires proprietary data, hardware, or >12 months of engineering. | Solo dev ships usable MVP in <30 days with current tooling. |
| 3 | **Defensibility** | Pure wrapper around a commodity API; anyone can clone. | Domain trust, data network effects, workflow lock-in, or regulatory moat that compounds. |
| 4 | **Buyer clarity** | "Someone in the org should care." | Named role with a budget line and a signed PO within 90 days of outreach. |
| 5 | **TAM shape** | Niche tool; hard ceiling < $1M ARR. | Clear path to $10M+ ARR through expansion or adjacent verticals. |
| 6 | **Personal fit** | Requires a team, sales-heavy, consumer-facing, or outside technical depth. | Solo operator, B2B, technical product, plays to founder's specific strengths. |
| 7 | **Societal value** | Extractive, speculative, or adversarial. | Real positive externality (safety, health, climate, research productivity, democratic institutions). |

**Scoring discipline:**
- Score the *opportunity shape*, not current traction. Attest has a
  working SDK; every candidate here is a hypothesis. Don't penalize
  candidates for being earlier.
- Score conservatively. If a dimension is *ambiguous*, round down.
- Never score a candidate you just read about in the last 24 hours
  above 4 on any dimension — the enthusiasm effect is real.
- Document a one-sentence reason for every score of 0-1 or 4-5.

---

## 2. Calibration baseline — Attest

**What it is:** Runtime-evidence SDK for EU AI Act Articles 11, 12, 15, 72.
Wedge: construction-AI vendors selling into EU deployments.

| # | Dimension | Score | Why |
|---|---|---|---|
| 1 | Urgency | **4** | Aug 2 2026 enforcement is real, but GDPR precedent suggests year+ grace on actual fines, softening the "must-buy-now" pressure. |
| 2 | Build accessibility | **5** | Already shipped. SDK, dashboard, OSCAL export, drift detection all work. |
| 3 | Defensibility | **2** | Thin. Vertical content + speed is the only moat; a funded horizontal (Credo, Fiddler) could match our construction narrative in weeks. |
| 4 | Buyer clarity | **3** | CTO/founding CEO at 5-50 person vertical AI vendors is identifiable, but segment may be too small/early to fund a $12k/yr tool. |
| 5 | TAM shape | **3** | Construction wedge → other high-risk verticals (safety-critical CV, industrial) is plausible. Ceiling is mid-8-figures globally unless we become the default runtime evidence layer. |
| 6 | Personal fit | **5** | Solo operator, B2B SaaS, technical product, regulation-driven sales cycle. Matches founder profile exactly. |
| 7 | Societal value | **4** | Makes AI Act workable without forcing every small AI vendor to hire a compliance team. Adjacent to AI-safety infra. |

**Total: 26 / 35.**
**Pivot bar: any candidate must score >= 28 to justify replacing Attest.**

---

## 3. Candidate themes to run

Not all themes deserve the horizon feed. Pick 3–4 before running.
Scoped so each produces a distinct shape of opportunity:

### Theme A — Post-AI-regulation infra (adjacent to Attest)
Tools for AI Act, US EO 14110 successors, UK AISI, NYC Local Law 144,
EU Product Liability Directive update. Different angles from Attest:
data governance, red-teaming as a service, AI-BOM (bill of materials),
model provenance / C2PA for model weights, eval-as-a-service for
regulated buyers. **Why interesting:** we already understand this
market; adjacency means some Attest work carries over.

### Theme B — Vertical AI "shovels" for regulated industries
Infra for a specific regulated vertical: healthcare AI ops (FDA 510(k)
for AI/ML SaMD, PCCP filings), legal AI (bar rules, privilege),
medical devices, pharma manufacturing, financial services (SR 11-7 /
model risk management). **Why interesting:** regulation creates the
forcing function; verticals create defensibility via domain trust.

### Theme C — Operational ML reliability (the non-compliance slice)
Drift, shadow testing, agent reliability, fleet management for
production ML / LLM apps. **Why interesting:** decoupled from
regulation, which means no enforcement risk. **Why risky:**
horizontal players (Arize, Fiddler, WhyLabs, LangSmith) already own
this lane; wedge would have to be a specific sub-problem they miss.

### Theme D — Post-frontier-commodity era
When base models commoditize: eval infra, model routing, agent
observability, cost optimization, agent-security (prompt injection,
jailbreak detection in production). **Why interesting:** fast-growing
budget line. **Why risky:** lots of funded entrants already; window
for a solo dev narrows monthly.

### Theme E — Climate & energy reporting infra
Carbon accounting, SEC climate rule / EU CSRD / California SB 253
reporting, grid interconnection queue tooling, RGGI/EU ETS auction
analytics. **Why interesting:** real regulation, real urgency, real
budgets. **Why risky:** crowded (Watershed, Persefoni, Sweep) and
sales cycles are long.

### Theme F — Bio / lab-infra
Protein design QC, wet-lab scheduling, reagent ordering portals,
CGMP-under-AI tooling. **Why interesting:** frontier-adjacent,
defensible. **Why risky:** outside current domain knowledge; sales
requires wet-lab credibility.

### Theme G — Defense / dual-use (non-kinetic)
Compliance, simulation, logistics, supply-chain integrity, ITAR
tooling for AI-defense vendors now that Anduril / Palantir / Shield AI
are unicorns. **Why interesting:** huge budgets, few tools, hard
mode makes it defensible. **Why risky:** multi-year sales cycles,
clearance gatekeeping, ethical bright lines.

---

## 4. Active candidate list

### Findings (first pass — Apr 2026, themes A / B / E)

**Synthesised 11 candidate product ideas from themes A, B, E.
Strict-conservative scoring (round down on ambiguity) produced one
finding worth naming:**

> **No pure green-field idea beats Attest on the rubric.**

The three candidates that cleared the minimum-research threshold
(score >= 24) are all *narrower* than Attest on some combination of
TAM, personal fit, or build accessibility. The single candidate that
scored higher than Attest (27 vs 26) is **Candidate 1 below** — which
is a *vertical pivot of Attest itself* (reuse the SDK, swap the
regulation from EU AI Act to FDA SaMD / PCCP). That's a meaningful
result:

- **If Attest fails at construction, the strongest fallback is not
  abandoning the SDK — it's moving it to medical AI post-market
  surveillance.** The code, the Annex-IV-equivalent generator, and the
  drift monitoring transfer directly. The FDA has been explicit that
  PCCP-modified devices need structured post-market evidence.
- **If Attest fails at a deeper level** (e.g. AI vendors genuinely don't
  pay for runtime evidence at any price), the next-best options are
  *completely different products* in narrower markets (interconnection
  queue navigator, 510(k) filing SaaS). Neither beats Attest today on
  the rubric, but they survive the first cut.
- **Climate / energy is harder than it looks from the outside.**
  Carbon incumbents (Watershed, Persefoni, Sweep) have saturated the
  obvious wedges. Only interconnection queue navigation and CBAM
  tooling scored above 22 in theme E. The rest scored in the high
  teens.
- **Compliance infrastructure plays (theme A) all scored lower than
  Attest.** That's not surprising — we already picked the best
  adjacent wedge when we picked Attest.

---

### Candidate 1 — Attest-FDA (medical AI post-market surveillance)

- **One-line thesis:** Port Attest's SDK + Annex-IV generator to FDA
  SaMD. Output: PCCP-aligned performance monitoring reports, post-
  market surveillance evidence, and 522 order support.
- **Buyer:** Regulatory Affairs Director or Head of Quality at AI
  medical device companies (Aidoc, Paige.AI, RapidAI, Tempus, dozens
  of smaller players). Budget line: regulatory operations /
  post-market.
- **Forcing function:** FDA's 2024 PCCP final guidance requires
  pre-specified performance monitoring for ML-modified devices. Every
  510(k)-cleared AI/ML device (950+ and growing at ~300/yr) needs
  ongoing evidence.
- **MVP shape:** Fork Attest core. Replace EU AI Act classifier with
  FDA SaMD risk categorization (Class I/II/III, IMDRF SaMD). Replace
  Annex IV template with PCCP modification summary + 21 CFR 820
  records. Ship drift detection for clinical performance metrics
  (sensitivity/specificity). ~3-4 weeks.
- **Defensibility path:** FDA-specific workflow + precedent from first
  10 customers becomes a trust moat. Regulated medical device
  customers don't switch tooling quarterly. HIPAA compliance posture +
  FDA relationship knowledge compounds.
- **Biggest risk:** Medical device sales cycles are 6-12 months; a
  solo founder without medical background may lack credibility with
  Regulatory Affairs buyers. Requires at least one RA advisor on the
  team to close deals.
- **Score:** U/BA/D/BC/TAM/PF/SV = 3/4/4/4/3/4/5 → **27 / 35**
- **What would have to be true to pivot here?** (a) Attest construction
  outreach gets zero pilot conversions in 60 days, AND (b) an inbound
  or warm intro surfaces from a medical AI company, OR (c) we can
  find a Regulatory Affairs advisor willing to co-sell for equity.

---

### Candidate 2 — Interconnection queue navigator for IPPs

- **One-line thesis:** ISO-queue intelligence SaaS that tells utility-
  scale solar/storage developers where their projects stand, what
  delays to expect, and how to strategize queue position reforms.
  Dashboard + alerts + FERC filing support.
- **Buyer:** Director of Interconnection or VP Development at
  independent power producers (IPPs) and utility-scale developers.
  Named role, $50-150k/yr budget line.
- **Forcing function:** FERC Order 2023 queue reform (2023), MISO /
  PJM / CAISO cluster study restructuring, and the fact that grid-
  interconnection delay is now the #1 constraint on US clean energy
  deployment (~2,000 GW in queue, 5-year average wait).
- **MVP shape:** Pull ISO public queue data (all 7 ISOs publish some
  form), normalise, add delay prediction + peer comparison. 4 weeks to
  a useful v1.
- **Defensibility path:** Proprietary models of queue dynamics; once
  one IPP uses us for a deal, the case study sells the next three.
  Queue intelligence compounds with historical data.
- **Biggest risk:** IPP procurement is slow; a single $1M+ deal loss
  can crater an IPP, which makes them risk-averse on new vendors.
  Also, some IPPs may build this in-house once the problem is
  formalised.
- **Score:** U/BA/D/BC/TAM/PF/SV = 4/3/4/4/3/2/5 → **25 / 35**
- **What would have to be true to pivot here?** Someone on the
  founder's network has direct IPP relationships, OR we can find a
  co-founder from the energy development world. Energy-sector trust
  is not something a compliance-background outsider builds in <6
  months.

---

### Candidate 3 — 510(k) / PCCP filing infrastructure for AI medical devices

- **One-line thesis:** Software that writes the structured portions of
  an FDA 510(k) or PCCP submission for AI/ML medical devices. Not
  full RA-as-a-service; specifically the repetitive structured
  artefacts (device description, performance testing protocols,
  labeling, PCCP modification table).
- **Buyer:** Regulatory Affairs lead at AI medical device companies;
  typically 1-3 person RA team spending $200-500k/yr on outside RA
  consultants.
- **Forcing function:** Every SaMD clearance now needs PCCP; 300+
  new AI/ML clearances per year; average 510(k) writing cost
  $100-300k in consulting.
- **MVP shape:** Structured 510(k) section generator for device
  description + performance testing protocol. FDA eSTAR template
  integration. 4-6 weeks.
- **Defensibility path:** Each accepted filing becomes a template for
  the next. FDA-specific knowledge + eSTAR integration is sticky.
- **Biggest risk:** FDA consultant firms (NAMSA, Emergo, RQM+) have
  30-year relationships with buyers; software that doesn't carry a
  name sits in the "we'll try it for a non-critical filing" slot.
- **Score:** U/BA/D/BC/TAM/PF/SV = 4/3/4/4/3/2/5 → **25 / 35**
- **What would have to be true to pivot here?** Same as Candidate 1's
  advisor requirement. Also: a credible first customer willing to run
  a filing through our tool for a reduced fee.

---

### Holding pen (scored 22–24, kept for reference, no deep work)

| Candidate | Score | One-line reason not to pursue now |
|---|---|---|
| NYC LL144 / CO AI Act bias audit SaaS | 24 | Crowded (Warden AI, Parity, Arthur); HR domain isn't home turf. |
| Clinical trial AI regulatory assistant | 24 | Pharma sales cycle is 12-18 months; domain is outside depth. |
| CBAM compliance for EU importers | 24 | Niche workflow; carbon majors will add a CBAM module in 2026. |
| Methane quantification for upstream O&G | 23 | Requires sensor/data integration; wrong industry culturally. |
| SR 11-7 model risk for mid-market banks | 23 | Validmind / Modelop / Arthur compete; bank procurement brutal. |
| AI-BOM / model provenance | 22 | No hard deadline; unclear budget-holder today. |
| Red-teaming-as-a-service for regulated AI | 22 | Haize, Repello, Promptfoo are funded; ethical edge cases. |
| EU AI Act deployer-side compliance (Art 26-29) | 20 | Org-process + enterprise sales; wrong shape for solo. |

---

### Killed (< 22 on first pass — do not revisit without new evidence)

- Legal AI privilege/confidentiality compliance (score 18; small buyer segment, bar rules are soft).
- Scope 3 supplier engagement tooling (not scored in full; Watershed/Persefoni own this and it's hand-to-hand combat).
- Bio/lab-infra candidates from Theme F — did not run (theme not selected).
- Defense / dual-use — did not run (theme not selected).

---

## 5. Operating rules

1. **Don't populate this list unless Attest signal is ambiguous or
   negative.** Every hour on this list is an hour off primary work.
2. **Score before researching more.** If a candidate scores < 24 on
   first pass, do not do additional deep research. Kill and move on.
3. **Re-score candidates monthly.** Scores drift as the market moves
   (new funded competitor, regulation passed, wave crests).
4. **Kill rule.** Any candidate ranked >= 6 on the list for more than
   60 days without a score change gets deleted.
5. **No building.** This is a paper exercise until Attest has a
   decisive outcome. Pre-building a pivot kills the current bet.
