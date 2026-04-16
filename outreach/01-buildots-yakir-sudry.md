**To:** Yakir Sudry — CTO, Buildots
**Find via:** LinkedIn (Yakir Sudry, Buildots)
**Also CC/follow up:** Ori Silberberg (VP Product & Engineering)

---

**Subject:** VINCI and Bouygues will ask you about this by August

Hi Yakir,

Congrats on the Series D — $166M is a clear signal that the market trusts what you're building.

I'm reaching out because of your EU deployments specifically. Your partnerships with VINCI and Bouygues Construction put Buildots' CV systems on EU construction sites analyzing worker activity and site progress. Under the EU AI Act, that's classified as high-risk AI (Annex III — worker management and safety components). Enforcement starts August 2.

The practical problem: VINCI and Bouygues will need to show their regulators that every AI system in their supply chain is compliant. That means they'll be asking you for Annex IV technical documentation, conformity assessments, logging evidence, and drift monitoring data. If you can't produce it, they have to stop using you — or risk fines up to €35M.

We built Attest to handle this for construction AI companies. It's a Python SDK — wraps your CV models, automatically classifies risk, logs every inference, monitors for accuracy drift, and generates Annex IV documentation from actual runtime data. One-line integration, no changes to your inference pipeline.

Here's the repo: https://github.com/saintbate/attest-ai
And the overview: https://attest-ai-eta.vercel.app

Worth 20 minutes to walk through how this maps to your specific systems?

Best,
Nick
Vertical AI LLC
