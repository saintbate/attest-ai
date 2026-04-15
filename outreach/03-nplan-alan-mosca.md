**To:** Alan Mosca — CTO, nPlan
**Find via:** LinkedIn (Alan Mosca, nPlan)

---

**Subject:** EU AI Act implications for schedule forecasting systems

Hi Alan,

nPlan's dataset — 750K completed project schedules representing $2.5T in capital spend — is a genuinely unique asset. The probabilistic forecasting angle is smart.

I'm reaching out about the EU AI Act, which becomes enforceable for high-risk systems on August 2. Your systems sit in an interesting classification zone: AI generating project schedules that influence resource allocation, worker deployment, and risk assessment on critical infrastructure (HS2, Network Rail, Anglian Water) could fall under Annex III — both Area 2 (critical infrastructure) and Area 4 (worker management).

Even from London, the Act applies if EU-based organizations use the system or if you're selling into EU markets. Given GV's involvement, I'd expect regulatory readiness is already on the radar.

We built Attest — an open-source compliance SDK for AI systems. It wraps your models, classifies risk against all eight Annex III categories, logs inferences, detects drift, and generates Annex IV technical documentation from runtime data. Designed so engineering teams can handle compliance without bolting on a separate department.

Repo: https://github.com/saintbate/attest-ai
Overview: https://attest-ai-eta.vercel.app

Would be happy to spend 20 minutes walking through the specific classification questions for a scheduling/forecasting system — the high-risk boundary isn't always obvious for predictive AI.

Best,
Nick
Vertical AI LLC
