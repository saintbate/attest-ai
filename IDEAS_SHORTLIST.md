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

> **[POPULATE AFTER RUNNING RESEARCH TOOL]**
>
> Format per candidate:
>
> ### Candidate N — <Short name>
> - **One-line thesis:** ...
> - **Buyer:** ... (role, company type, budget line)
> - **Forcing function:** ... (regulation, deadline, cycle)
> - **MVP shape:** ... (what ships in 30 days)
> - **Defensibility path:** ... (what compounds over 18 months)
> - **Biggest risk:** ... (the one thing that kills it)
> - **Score:** U/BA/D/BC/TAM/PF/SV = n/n/n/n/n/n/n → **total / 35**
> - **What would have to be true to pivot here?** ...

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
