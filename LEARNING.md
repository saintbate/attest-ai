# What to Know — A Founder's Curriculum for Attest

> **Audience:** You, in the next 4–12 weeks.
> **Optimization target:** Be the person on the other end of the discovery
> call that a CTO at Buildots or a GC at OpenSpace can trust to understand
> their actual problem — legally, technically, and commercially.
> **Anti-goal:** Reading a 300-page regulation and remembering nothing.

This is a **prioritized** curriculum, not a comprehensive one. Skip
anything marked Tier 3/4 until Tier 1/2 is solid.

---

## Tier 1 — Non-negotiable (this week, ~8-12 hours)

These are the facts you'll get asked about on literally every sales call.
If you don't know them cold, you lose the call.

### 1. EU AI Act — structural knowledge, not full text

You do **not** need to read all 458 pages. You need to know:

- **The four risk tiers:** unacceptable (banned), high-risk, limited-risk (transparency only), minimal. Most construction AI is **high-risk**.
- **Two routes to high-risk classification:**
  - **Article 6(1):** AI used as a safety component of a product regulated by one of the EU's product-safety laws (e.g. Machinery Regulation). Triggers high-risk automatically.
  - **Article 6(2) + Annex III:** AI falling into one of 8 listed categories. Construction mainly hits §2 (critical infrastructure), §4 (employment / worker management), and sometimes §1 (biometrics).
- **The 10 provider obligations** (Articles 9–15, 43, 47, 72 + Article 17 QMS). These are the rows in your OSCAL output. Memorize the one-line purpose of each.
- **Provider vs deployer vs importer vs distributor.** Your customers are **providers** (they build the AI). VINCI / Bouygues are **deployers** (they use it on site). Different obligations.
- **Conformity assessment (Article 43):** two routes — *internal control* (the provider self-attests) vs *notified body involvement* (a third party certifies). Most Annex III systems self-attest; biometric systems require notified body.
- **Enforcement dates:**
  - **2 Feb 2025:** prohibited practices banned
  - **2 Aug 2025:** GPAI obligations + governance structure live
  - **2 Aug 2026:** high-risk Annex III obligations enforceable *(our deadline)*
  - **2 Aug 2027:** high-risk safety-component obligations (Article 6(1) route)
- **Penalties (Article 99):** up to €35M or 7% turnover for prohibited; **€15M or 3%** for high-risk non-compliance; €7.5M or 1.5% for misleading info.

**Where to learn:**
- [Future of Life Institute — AI Act Explorer](https://artificialintelligenceact.eu/) — article-by-article browser, best UX.
- [aiact-info.eu](https://www.aiact-info.eu/) — clean article text.
- [Official consolidated text, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — for direct quotes in emails and docs.

**Time budget:** 4 hours. Read Articles 3 (definitions), 6, 9–15, 43, 72 plus Annex III and Annex IV. Skim the rest.

### 2. Your own product — inside and out

You built this, but do you know:

- Every output your SDK writes to disk and what field it maps to in Annex IV?
- What `attest classify` returns for a borderline case (limited vs high)?
- What happens when `detect_drift` is called on <20 records?
- The exact command to generate an OSCAL file and what a reviewer does with it?

**Action:** run every CLI command once. Read every template. Break something on purpose, then fix it. You will be asked for a live demo.

**Time budget:** 3 hours this week, plus whenever something changes.

### 3. Your 5 outreach targets, cold

For each of Buildots, viAct, nPlan, DeepQual, OpenSpace — know without
looking it up:

- Stage and last funding round
- Their likely Annex III category and *why*
- Who the EU deployers/customers are (or might be)
- One reason their CTO hasn't already solved this

**Time budget:** 2 hours to refresh; then 20 min before every call on that specific company.

---

## Tier 2 — Strong professional (this month, ~20-30 hours)

Knowledge that makes you sound like you've been in this space for 5 years
instead of 5 weeks. Comes up in ~half of calls.

### 4. Harmonised standards & ISO/IEC 42001

The AI Act relies on **harmonised standards** published by CEN-CENELEC
JTC 21 to give providers "presumption of conformity." Knowing which
standards are in draft vs published is how you sound credible about
what compliance will actually look like.

- **ISO/IEC 42001:2023** — the AI Management System standard. The likely "ISO 27001 of AI." Buyers will ask if you're aligned with it.
- **ISO/IEC 23894** — risk management for AI.
- **ISO/IEC 23053** — framework for AI systems using ML.
- CEN-CENELEC JTC 21 work programme (Google it — the document moves).

**Where to learn:**
- [ISO/IEC 42001 standard page](https://www.iso.org/standard/81230.html) (you don't need to buy it — the executive summary is enough).
- Look at one [published harmonised standard mandate M/593](https://single-market-economy.ec.europa.eu/sectors/automotive-industry/standardisation-automotive-sector_en) to see how the EU delegates standard-making.

**Time budget:** 3-4 hours. Don't rabbit-hole.

### 5. GDPR intersections

Construction AI often processes worker biometrics, personal data in
timesheets, or identifiable video footage. That triggers GDPR on top of
the AI Act.

- **Article 22 GDPR:** right not to be subject to solely automated decisions with legal/significant effects.
- **DPIA:** Data Protection Impact Assessment often required when AI processes personal data at scale.
- **Legal basis for training data:** consent, legitimate interest, or contract — each has tradeoffs.

**Time budget:** 2 hours. You don't need to become a GDPR expert; you need to know when to say "that's a GDPR question, not an AI Act question" — they have different teams at customers.

### 6. Notified bodies & conformity assessment

Customers will eventually ask: *who actually certifies this?*

- **NANDO database** — official list of notified bodies. As of 2026, **no notified body is yet designated for AI Act Annex III conformity assessment**. This is important context: the system is still being built.
- Positioning leaders: **BSI** (UK/global), **TÜV SÜD** / **TÜV Rheinland** (Germany), **DEKRA**, **Bureau Veritas**.
- Self-assessment is the dominant path for most Annex III systems. Attest helps you *prepare* the technical file; the provider signs the Declaration of Conformity (Art. 47).

**Time budget:** 2 hours.

### 7. ML monitoring / the technical depth customers will probe

You ship drift detection. Know the literature well enough to answer:

- KS vs MMD vs PSI (population stability index) vs chi-squared — when does each shine?
- Calibration: temperature scaling, Platt scaling, conformal prediction. What's the difference between *accuracy* and *calibration*, and why does the AI Act Article 15 care about both?
- Model cards (Mitchell et al., 2019) and datasheets (Gebru et al., 2018) — these predate Annex IV and heavily influenced it.
- Post-hoc explainability (SHAP, LIME) vs inherently interpretable models.

**Where to learn:**
- Chip Huyen — *Designing Machine Learning Systems* (chapters 8–10 specifically, not the whole book).
- The original Model Cards paper (Mitchell et al.) — 10 pages.
- The original Datasheets paper (Gebru et al.) — 12 pages.
- DriftLens paper (Greco et al., 2024) — already in `attest/research/`.

**Time budget:** 8-10 hours over a month.

### 8. Competitive landscape

Already briefed earlier in the project notes. Re-read once a month.

- **Governance/documentation:** Credo AI, Trustible, Holistic AI.
- **Observability:** Arize, Fiddler, Arthur, Luminos, Robust Intelligence (now Cisco).
- **LLM-specific:** Dynamo AI, Lakera.
- Track their **funding rounds, product releases, case studies**. A new Arize construction case study is a signal worth reacting to.

**Time budget:** 30 minutes a week, ongoing.

---

## Tier 3 — Depth (next 3 months, ~15-20 hours)

### 9. Adjacent EU regulations

- **Machinery Regulation 2023/1230** — applies to safety components (including AI ones) in machines. Overlaps with AI Act Art. 6(1).
- **General Product Safety Regulation (GPSR) 2023/988** — general duty of safety for products sold in the EU.
- **AI Liability Directive (proposed, as of 2026 still politically contested)** — would create presumptions of fault in AI-caused harm cases.
- **Product Liability Directive (revised, 2024)** — software, including AI, is now clearly a "product" for strict liability purposes.

**Why it matters:** a sophisticated customer will ask "how does this interact with machinery safety?" You need a one-sentence answer, not a blank stare.

### 10. Construction industry specifics

- **Top 10 European GCs** by revenue: VINCI, Bouygues, ACS/Hochtief, Strabag, Eiffage, Skanska, Ferrovial, NCC, PORR, Webuild. Know who's pushing AI adoption.
- **Construction tech stack:** BIM (Revit, ArchiCAD), common data environments (Autodesk Construction Cloud, Procore), CV platforms (OpenSpace, Buildots, Cintoo, DroneDeploy).
- **Regulators you'll hear about:** national construction authorities, labor inspectorates (for worker monitoring AI).
- **Key industry events:** Hamburg AI Summit in Construction, Autodesk University, Digital Construction Week London, BAU Munich.

**Time budget:** read a quarterly industry report (e.g. Roland Berger, McKinsey) — 2 hours.

### 11. B2B SaaS fundamentals

If you've done SaaS before, skim. If not:

- **Metrics:** ARR, NRR (net revenue retention — the one that matters most), gross margin, CAC payback, logo churn vs revenue churn.
- **Sales motion:** PLG vs sales-led vs hybrid. You're doing founder-led sales → eventually sales-led. Not PLG for compliance tooling.
- **Contract structures:** MSA + SOW, order forms, DPA (data processing addendum — every EU customer will want one).
- **Reading:** Jason Lemkin (SaaStr) on early-stage sales; David Skok's "SaaS Metrics 2.0."

**Time budget:** 4-6 hours if new to SaaS.

---

## Tier 4 — Optional / long-arc

Only do these if you're still deep in Attest 6+ months from now.

- **IAPP AIGP certification** (AI Governance Professional). Launched 2024, taken seriously in the compliance world. ~40 hours of study, ~$600 exam. Gives you a credential buyers will Google.
- **ISO/IEC 42001 Lead Implementer course** (PECB or similar). More technical. ~40 hours + exam.
- **Reading:** *The Worlds I See* (Fei-Fei Li — history and trajectory of CV); *Weapons of Math Destruction* (O'Neil — why AI regulation exists at all); *Atlas of AI* (Crawford).
- **Attend one event in person:** Digital Construction Week London (~June) is probably your highest-ROI single event.

---

## Ongoing habits — 30 minutes a week

The regulation and market move. Have standing inputs.

- **Subscribe to:** [IAPP AI Governance newsletter](https://iapp.org/news/), [Euractiv Digital](https://www.euractiv.com/sections/digital/), [AI Act Newsletter (Hadrien Pouget / Marietje Schaake)](https://substack.com/@aiact).
- **Follow on LinkedIn:** Kai Zenner (EPP AI Act negotiator), Dragos Tudorache (rapporteur), Gabriele Mazzini (former Commission lead on the Act), Nathalie Smuha (KU Leuven).
- **Follow on arXiv:** the drift detection + calibration tags (you already have the script).
- **GitHub watch:** OSCAL, AI Verify Foundation toolkit — adjacent projects that will shape standards.
- **One conference talk a month.** 45 minutes, on your lunch break. Look at CPDP, FAccT, NeurIPS policy track recordings.

---

## What you can safely *not* know

Saying "I don't know, but I can find out by tomorrow" is better than
bluffing. Topics it is **completely fine** to defer on:

- The full text of GDPR Chapters 3-9 (you just need Article 22 and the DPIA concept).
- Every national implementation law — they're still being drafted.
- The AI Liability Directive as of 2026 — it's stalled; don't over-invest until it moves.
- Detailed US state AI laws (Colorado, California) unless a customer explicitly operates there.
- Model interpretability theory at a research depth — know the techniques exist, leave the math to your customers' data scientists.

---

## Sequence for the next 30 days

| Week | Focus | Hours |
|---|---|---|
| 1 | Tier 1 #1 (AI Act structure) + Tier 1 #2 (your product) | 8 |
| 2 | Tier 1 #3 (targets, per call) + Tier 2 #4 (ISO 42001) | 6 |
| 3 | Tier 2 #5 (GDPR) + Tier 2 #7 (ML monitoring depth) | 8 |
| 4 | Tier 2 #6 (notified bodies) + Tier 2 #8 (competitors) | 4 |

That's 26 hours — one evening + one weekend morning per week for a
month. Enough to be genuinely credible with anyone short of a specialist
lawyer or an ML-ops veteran. And enough to *know what you don't know*,
which is most of the game.

---

*Update this doc the first time a customer asks a question you couldn't
answer. That question goes into Tier 1.*
