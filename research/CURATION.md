# Attest Research Curation

Arxiv search (~180 papers, post-2024) across six tracks. This is the tight list — the papers that should directly inform Attest's roadmap, ordered by implementation priority.

---

## Tier 1 — This is the blueprint

These five papers are the closest prior art to what Attest is doing. Read all five.

### [2604.13767] Making AI Compliance Evidence Machine-Readable
**Published:** April 15, 2026 (last week)
**Link:** https://arxiv.org/abs/2604.13767
**Why it matters:** This paper proposes **OSCAL** — the NIST standard already used for FedRAMP cybersecurity compliance — as the interchange format for AI governance. They test it on two Annex III high-risk systems (credit scoring + medical imaging segmentation) and ship an open-source SDK that generates OSCAL Assessment Results as a byproduct of training. Three-layer architecture: policy → evidence → enforcement.

**For Attest:**
- Seriously consider emitting OSCAL alongside Markdown Annex IV docs. OSCAL is what conformity assessment bodies will parse programmatically. "We output OSCAL" is a huge credibility signal to procurement.
- The three-layer model (policy / evidence / enforcement) is cleaner than Attest's current flat structure. Reorganize accordingly.
- They call this "Compliance-as-Code" — steal that framing for marketing.

---

### [2406.18211] AI Cards: Machine-Readable AI and Risk Documentation Inspired by the EU AI Act
**Published:** June 26, 2024
**Link:** https://arxiv.org/abs/2406.18211
**Why it matters:** In-depth analysis of the AI Act's technical documentation provisions, specifically on risk management. Proposes "AI Cards" as a holistic framework combining technical specs, context of use, and risk management — both human- and machine-readable (Semantic Web / JSON-LD).

**For Attest:**
- Your Annex IV generator currently produces Markdown. Add a JSON-LD sidecar using their schema. Now your docs are machine-queryable across the AI value chain.
- VINCI/Bouygues procurement will eventually want to *diff* AI Cards across vendors. Being first-mover on the structured output wins that.

---

### [2512.12443] AI Transparency Atlas: Framework, Scoring, and Real-Time Model Card Evaluation Pipeline
**Published:** December 13, 2025
**Link:** https://arxiv.org/abs/2512.12443
**Why it matters:** Analyzed 100 Hugging Face model cards + 5 frontier models — found 947 unique section names and extreme naming variation. Built a weighted framework with 8 sections / 23 subsections using **Annex IV + Stanford Transparency Index** as baselines. Built an automated scoring pipeline (LLM consensus). Frontier labs score ~80% compliance, most providers below 60%.

**For Attest:**
- The 8-section / 23-subsection schema is a ready-made Annex IV checklist. Map Attest's generator output to it exactly.
- Their scoring pipeline is a direct product feature: "Attest Compliance Score — how audit-ready is your system?" Free tier output; paid tier to fix gaps.
- Safety-critical disclosures weighted at 25% / 20% — matches EU AI Act prioritization.

---

### [2603.28558] T-Norm Operators for EU AI Act Compliance Classification
**Published:** March 30, 2026
**Link:** https://arxiv.org/abs/2603.28558
**Why it matters:** Direct comparison of three neuro-symbolic classifiers on a **benchmark of 1,035 annotated AI system descriptions** across four risk categories (prohibited / high / limited / minimal). Gödel semantics: 84.5% accuracy, 85% borderline recall but 0.8% false positives. Lukasiewicz and Product: zero false positives, lower recall.

**For Attest:**
- Your current classification is rule-based keyword matching. This paper's benchmark alone (1,035 examples) is worth building against — it validates whether your classifier is actually any good.
- The finding "operator choice is secondary to rule base completeness" is the right takeaway: don't over-engineer the classifier, expand the keyword library and test against their benchmark.
- Contact the authors for the LGGT+ dataset. Even if you don't use their neuro-symbolic approach, the labeled data is gold.

---

### [2603.22322] AEGIS: Operational Infrastructure for Post-Market Governance of Adaptive Medical AI Under US and EU Regulations
**Published:** March 2026
**Link:** https://arxiv.org/abs/2603.22322
**Why it matters:** Name collision aside — this is a medical-AI-specific version of what Attest is building. "Operational infrastructure for post-market governance" is almost your tagline. Focuses on adaptive (continuously learning) systems, which is where Article 72 gets hardest.

**For Attest:**
- Read this to see what "post-market monitoring infrastructure" looks like when designed by academics who know the regulation cold.
- Their vertical is medical. Yours is construction. Same playbook, different customer.
- If they've open-sourced it, consider whether construction is differentiated enough or if you'll get leap-frogged by a medical team expanding horizontally.

---

## Tier 2 — Drift detection upgrades

Your current implementation is Mann-Whitney U on confidence distributions. These two papers give you meaningful upgrades you can ship this week.

### [2406.17813] DriftLens: Unsupervised Concept Drift Detection from Deep Learning Representations in Real-Time
**Link:** https://arxiv.org/abs/2406.17813
**Why it matters:** Unsupervised (no labels needed — which is exactly Attest's constraint), works on embeddings rather than raw outputs, detects drift in 15/17 benchmark use cases, runs at least 5x faster than prior methods, correlation ≥0.85 with actual drift, and **identifies representative drift samples as explanations**.

**For Attest:**
- Swap this in for your current Mann-Whitney approach. Same input interface, better output.
- The "identifies representative drift samples" feature is a sales demo goldmine: "Here are the 5 images from last week that broke your model."
- Has code on GitHub. Likely 1–2 days of integration work.

---

### [2604.09358] Drift-Aware Multi-Scale Dynamic Learning (DA-MSDL)
**Link:** https://arxiv.org/abs/2604.09358
**Why it matters:** Uses MMD (Maximum Mean Discrepancy) for unsupervised drift detection — industry-standard statistical test, beats U-tests on feature distributions. Designed for **industrial monitoring applications** (steel sintering). Proactive: triggers adaptation *before* inference degrades.

**For Attest:**
- MMD is a better default drift detector than Mann-Whitney U for multivariate feature distributions. Cleaner story for customers: "MMD is a standard statistical test used in industrial monitoring."
- The "proactive adaptation" framing is good pitch language: "Don't wait for performance to drop — catch drift as it forms."

---

## Tier 3 — Calibration for defensible compliance claims

### [2604.12951] The Verification Tax: Fundamental Limits of AI Auditing in the Rare-Error Regime
**Link:** https://arxiv.org/abs/2604.12951
**Why it matters:** Proves there is a **statistical noise floor** below which calibration claims are meaningless. The widely cited Guo et al. 2017 result (ECE 0.012) is below this floor. As models improve, verifying calibration becomes exponentially harder. Pipeline depth K compounds verification cost at rate L^K.

**For Attest (critical):**
- This paper tells you what you *cannot* defensibly claim. If you market a customer's system as "well calibrated (ECE < 0.02)" and they have low error rates, you're making statistically unsupported claims. Lawsuit risk.
- Attest should report calibration intervals **with uncertainty bounds**, not point estimates. Differentiates you from competitors who will happily report ECE point values.
- Cite this paper in Annex IV documentation when reporting calibration: "Measured ECE subject to the verification floor of Wang (2026)."

---

### [2604.08639] VOLTA: The Surprising Ineffectiveness of Auxiliary Losses for Calibrated Deep Learning
**Link:** https://arxiv.org/abs/2604.08639
**Why it matters:** Benchmarks 10 popular uncertainty quantification methods (MC Dropout, SWAG, ensembles, temp scaling, energy-based OOD, Mahalanobis, etc.). Result: a simple approach — deep encoder + learnable prototypes + cross-entropy + post-hoc temperature scaling — beats most of them. ECE 0.010 vs. 0.044–0.102 for baselines.

**For Attest:**
- When you add a calibration module, start with post-hoc temperature scaling. Cheap, no retraining, well-understood. Add complexity only if customers need it.
- Attest can offer a "calibration audit" — run their model on held-out data, report raw vs. calibrated ECE. Good demo/lead-gen tool.

---

## Tier 4 — Adversarial testing for construction CV

The EU AI Act requires "robustness" but doesn't define how to measure it. These papers are your starting point for a future `attest.robustness()` module.

### [2411.06146] AI-Compass: Multi-Module Testing Tool for AI Systems
**Link:** https://arxiv.org/abs/2411.06146
**Why it matters:** Already does what you might want to build — adversarial robustness, interpretability, and neuron analysis across image classification, object detection, and other modalities. Open-source tool.

**For Attest:** Either integrate this directly (wrap their API into `attest.test()`) or use their evaluation methodology to structure your own. Don't rebuild from scratch.

---

### [2604.06865] Physical Adversarial Attacks on AI Surveillance Systems
**Link:** https://arxiv.org/abs/2604.06865
**Why it matters:** Directly applicable to construction CV. Reviews physical attacks on person detection, multi-object tracking, visible-infrared sensing. Taxonomy of 4 threat vectors: temporal persistence, sensing modality, carrier realism, system-level objective.

**For Attest:** Construction customers (Buildots, viAct, OpenSpace) all do person/worker detection. This paper tells you what adversarial robustness testing should actually probe for. Sales angle: "Your PPE detector works — but does it work when someone's wearing a printed pattern designed to fool it?"

---

### [2502.02537] Uncertainty Quantification for Collaborative Object Detection Under Adversarial Attacks
**Link:** https://arxiv.org/abs/2502.02537
**Why it matters:** TUQCP framework — combines adversarial training with conformal prediction for object detection. Bridges your Tier 3 (calibration) and Tier 4 (robustness) tracks.

**For Attest:** Conformal prediction is the bridge between calibrated confidence and adversarial robustness. Worth understanding even if you don't implement — customers will ask.

---

## Tier 5 — Competitive/strategic context

Read these to understand the landscape you're competing in.

### [2604.04749] AI Trust OS — Continuous Governance Framework for Autonomous AI Observability and Zero-Trust Compliance
**Link:** https://arxiv.org/abs/2604.04749
**Why it matters:** Competing framework. Focuses on LLMs, RAG pipelines, multi-agent workflows — *not* CV or regulated-industry AI. Uses observability-driven discovery of AI systems.

**For Attest:**
- Direct adjacent positioning. They're going after enterprise AI governance horizontally. You're going vertical (construction).
- Their "telemetry evidence over manual attestation" principle is the same north star as Attest.
- If they build a construction vertical, you have a problem. Move fast.

---

### [2601.11702] PASTA: Multi-Policy AI Compliance Evaluation
**Link:** https://arxiv.org/abs/2601.11702
**Why it matters:** LLM-powered pairwise evaluation across 5 major policies, ~$3 per model, expert agreement ρ≥0.626.

**For Attest:**
- Direct competitor at the evaluation layer. But they're not instrumenting inference — they're evaluating documentation. You're collecting evidence at runtime. Complementary, not overlapping.
- Their cost benchmark ($3/model) is useful — know where the commoditized floor is.

---

### [2406.17548] Laminator: Verifiable ML Property Cards Using Hardware-Assisted Attestations
**Link:** https://arxiv.org/abs/2406.17548
**Why it matters:** If/when compliance evidence itself becomes a trust problem ("Did the vendor really log these inferences, or did they fabricate the JSON?"), hardware attestation (Intel TDX, AMD SEV) becomes relevant.

**For Attest:** Year 2+ feature. But mention it in the roadmap — it's where audit-grade ends up going.

---

### [2510.24142] Monitoring and Observability of Machine Learning Systems: Current Practices and Gaps
**Link:** https://arxiv.org/abs/2510.24142
**Why it matters:** Survey paper on the state of ML monitoring. Direct evidence of gaps in the market. Useful for positioning copy and investor decks.

---

## Strategic takeaways

1. **Two highest-impact things to ship this week:** DriftLens integration (Tier 2) + OSCAL output format (Tier 1). Both are real functionality improvements that are also strong sales talking points.

2. **Biggest defensibility risk:** The AI Trust OS paper. An enterprise-AI-governance startup with $10M could enter construction in 6 months. You need to be the default answer for construction-AI compliance before that happens. This is why the outreach push matters — customer logos are your moat.

3. **Build the AI Transparency Atlas schema into your Annex IV generator.** Their 8/23 schema is already research-validated and baselined against Annex IV. Free structure, free credibility.

4. **The Verification Tax paper changes what you can claim.** Review your landing page and marketing materials — if anything promises calibration accuracy below 1%, soften it or add uncertainty bounds. This paper will be cited in audit disputes within a year.

5. **The 1,035-example classification benchmark (2603.28558) is a free evaluation dataset.** Run your classifier against it. If you score comparably, you have a public benchmark number for sales decks. If you don't, you know exactly where to improve.

---

## Suggested implementation sequence

**Week 1:**
- [ ] Read the 5 Tier-1 papers
- [ ] Integrate DriftLens (or at least MMD) in `attest.monitor`
- [ ] Add OSCAL JSON output alongside Markdown in Annex IV generator

**Week 2:**
- [ ] Restructure Annex IV generator to match AI Transparency Atlas 8/23 schema
- [ ] Run Attest's classifier against the LGGT+ benchmark, publish results
- [ ] Add temperature scaling-based calibration module

**Week 3:**
- [ ] Write a blog post / landing page section citing these papers — "Attest is built on the current academic state of the art." Credibility at scale.
- [ ] Add verification-bounds language to any calibration reporting

**Later / roadmap:**
- [ ] `attest.test()` adversarial robustness module (wrap AI-Compass)
- [ ] Hardware-attested property cards (Laminator direction)
- [ ] Conformal prediction support for inference confidence bounds
