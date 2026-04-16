# Attest — Pricing & Packaging v0.1

> **Status:** Working draft for outbound conversations (not a public price page yet).
> **Audience:** Internal / used to anchor a founder-led sales conversation.
> **Owner:** Vertical AI LLC

---

## 1. Who signs the PO — mapped to current outreach targets

Until we have a designated "AI Governance Officer" in the market, the buyer is
whichever executive already owns **shipping the product in the EU**. Across
our top 5 targets, that's the CTO or founding CEO — **not** a compliance
officer or legal team.

| Target | Likely PO signer | Backing budget line | Pitch frame |
|---|---|---|---|
| Buildots | CTO / VP Eng | Engineering infra / deal enablement | "Don't block your next VINCI deal." |
| viAct | CEO (founder-led) | Growth / EU expansion | "Unblock the EU market move." |
| nPlan | CTO (Alan Mosca) | Engineering / R&D | "Your forecasting sits in Annex III §2 today." |
| DeepQual | CEO (founder) | Discretionary | "Compliance is mandatory; don't build it twice." |
| OpenSpace | VP Eng or GC | Engineering or Compliance | "EU customer growth = EU AI Act exposure." |

**Implication:** We are selling to a **CTO / founding CEO**, with an appeal to
**deal enablement**, not to a governance professional. Pricing and
packaging must feel like a **tool a small engineering team buys**, not an
enterprise GRC contract.

---

## 2. What we actually sell (outcomes, not features)

1. **EU deal unblock** — artifact bundle (Annex IV Markdown + OSCAL-aligned JSON) that a deployer's procurement / legal can accept as evidence.
2. **Evidence, on autopilot** — runtime logging, drift detection, classification that keeps that bundle current.
3. **One fewer hire** — avoid a €120-180k compliance engineer by shipping the SDK + dashboard.

We do **not** sell: "certified compliant," a legal opinion, or a notified-body
substitute. Sell **evidence generation + continuous monitoring**; the customer
still owns legal sign-off.

---

## 3. Packaging

Three published tiers + a bespoke one. Numbers are **anchors**, not floors —
the first two paid logos are worth discounting for.

### Pilot — $2,500 / 90 days
The "it's easier to say yes than no" tier.

- Up to **3 AI systems**
- Founder-led onboarding (we wrap your first model with you on a call)
- **Classification + gap analysis** delivered as a written report
- **First Annex IV document + OSCAL JSON** export
- Drift alerts on **1 metric / system** (Slack or email)
- Success criterion: customer agrees to a Team-tier annual or tells us why not

### Team — $12,000 / year (or $1,200 / month, annual commit)
The default for a small construction-AI product team.

- Up to **5 high-risk AI systems**
- Unlimited Annex IV + OSCAL regenerations
- Drift detection (KS, MMD, Mann-Whitney) with alerts
- Compliance dashboard, inventory, requirements tracker
- **Included inference volume:** 10M records / yr (overage bundled in 5M chunks at $500 each)
- Email support, 2 business-day response

### Scale — $36,000 / year
For teams with multiple EU products or regulated deployers.

- Up to **20 high-risk systems**
- SSO (Google / Azure AD)
- **Retention:** full 10-year retention built in
- **Webhook fan-out** (Slack, PagerDuty, custom)
- Priority support, 1 business-day response
- Quarterly "regulation review" call (what changed, what you owe)

### Enterprise — custom, minimum $75,000 / year
Triggered when **any** of: >20 systems, data residency requirement, security
questionnaire, procurement insists on a master agreement, or audit log
pipelining to the customer's SIEM.

---

## 4. Pricing anchors (so the number doesn't feel random)

| Alternative the buyer is comparing us to | Cost |
|---|---|
| Hiring one in-house compliance / ML-ops engineer | €120-180k / year fully loaded |
| Credo AI / Trustible / enterprise governance platform | ~$50-200k / year (public rumor range) |
| Fiddler AI / Arize (observability layer) | $75-150k+ / year |
| Consulting project to produce a one-off Annex IV | $30-60k fixed |
| One AI Act fine, high-risk non-compliance | Up to **€15M or 3% of global turnover** |

Attest Team at $12k sits at **~10% of hiring one person**, **~15-25% of
enterprise governance tooling**, and **~20-40% of a one-off consulting
engagement** — while being *continuous* instead of one-shot. That's the
value story.

---

## 5. Discount ladder for first logos (use sparingly)

Goal: **get to 3 paying logos by end of Q3 2026.** Paid > free. A cheap
paid customer has an opinion and sends feedback; a free one ghosts.

| Ask | Allowed give |
|---|---|
| "Can we pilot for free?" | No. Pilot stays paid — drop to $1,500 if budget is the blocker. |
| "We're pre-Series A, can you halve it?" | Team @ $6k/yr for year one, back to list in year two, written into the order form. |
| "We want to be a reference / case study" | 20% off year one **if** case study is pre-agreed and published within 90 days of go-live. |
| "Procurement wants multi-year" | Team: 10% off for 2-yr, 15% off for 3-yr. Scale: 15% / 20%. |
| "Can you throw in custom integrations?" | No, or scope them as paid services ($180-250/hr, minimum 20 hours). |

**Never do:** revenue share, deferred payment, equity-for-license, or
unlimited-systems pricing dressed up as a flat fee.

---

## 6. The 30-second pricing conversation (founder script)

When a target on a call asks *"How much?"* — do **not** dodge. Say:

> "Two tiers live today. A 90-day **pilot** at $2,500 — we wrap your first
> model, deliver a classification + gap analysis and your first Annex IV
> bundle. Most teams convert to **Team** at $12,000 a year, which covers up
> to five high-risk systems with continuous drift detection and regenerable
> docs. If you already have more than five EU-facing models, we'd look at
> **Scale** at $36,000. Which one are you closer to?"

Then **shut up.** Their response tells you which tier they're in and
what objection to handle.

---

## 7. Red flags / invoices we won't take

- **"Compliance-as-a-service"** interpreted by the buyer as "you own our
  legal risk." We do not. Decline politely; refer to a law firm.
- **Conformity-assessment stamp.** We are not a notified body.
- **Replacing the customer's technical writer.** We generate the draft;
  they edit and sign.
- **Usage-only / 100% variable pricing.** Our costs aren't that variable,
  and customers hate surprise bills. Always include a platform fee.

---

## 8. Decisions and open questions for the next 30 days

**Decided:**
- **No free pilots, ever.** A paid pilot is a signal that we believe in the
  product and that the buyer believes the problem is real. Free customers
  ghost; paying customers give feedback. If budget is truly the blocker,
  we will drop the pilot to $1,500, but the invoice still ships.

**Still open:**
- [ ] Does OSCAL output actually move the needle, or is Markdown enough
  for today's buyers? (Ask directly in the demo.)
- [ ] At what customer count do we need a real billing system vs. a
  Stripe invoice link?
- [ ] Is there a construction-specific add-on (e.g. Procore integration)
  that justifies a premium — or is the vertical angle already priced in?

---

## 9. How we take payment

At current scale (pre-first-customer to first ~10 paying logos), the
payment stack is **Stripe Invoicing, sent manually from the dashboard**.
No integration code, no self-serve checkout, no subscription engine.

### The stack

| Layer | Tool | Why |
|---|---|---|
| Legal entity | **Vertical AI LLC** | Already exists. Must own the bank account and Stripe account. |
| Business bank | **Mercury** (or Relay) | Free, opens in days, integrates with Stripe cleanly. Never route to a personal account. |
| Invoicing | **Stripe Invoicing** (not Checkout, not Subscriptions) | Hosted payment pages, ACH + card, zero code. |
| Bookkeeping | Spreadsheet until 10 customers, then **QuickBooks Online** or **Wave** | Not Stripe's job. |

### Fees

- **ACH:** 0.8%, **capped at $5 per transaction.** Preferred for anything >$1k.
- **Card:** 2.9% + $0.30. On a $12k Team invoice that's $348 — steer customers to ACH when you can.
- **Stripe Tax (optional):** ~$0.50 per invoice. Worth enabling the moment we invoice a non-US customer, not before.

### Payment terms

| Product | Term | Rationale |
|---|---|---|
| Pilot ($2,500) | **Due on receipt** or Net 15 | Small enough to bypass corporate AP; ask for fast pay. |
| Team annual ($12k) | **Net 30** | B2B default. Don't fight it. |
| Scale annual ($36k) | **Net 30**, or 50% upfront / 50% Net 60 if requested | Let procurement feel like they won something. |
| Multi-year | **Annual upfront, one invoice per year** | Avoid renewal fatigue, keep revenue recognition clean. |

### The invoice-sending checklist (≤ 5 minutes)

1. Customer agrees verbally or by email → same day, send Stripe invoice.
2. Line items named in the customer's language: "Attest Team annual subscription — up to 5 high-risk AI systems" (not "SaaS fee").
3. Include the **start and end dates of the subscription period** in the line item description.
4. Attach a short one-page PDF with: scope, support commitment, data handling, cancellation terms. (TODO: draft this template — see *Open questions*.)
5. Send. Follow up at +7 days if unpaid; +21 days if still unpaid, get on a call.

### EU customers

- **Reverse-charge VAT** is the norm for B2B sales to EU-established companies with a valid VAT ID. The invoice shows 0% VAT and a note: *"Reverse charge applies — Article 196 of Council Directive 2006/112/EC."*
- Capture the customer's VAT ID on the order form. Stripe Tax automates the invoice markup.
- Do **not** collect VAT yourself until we have an EU establishment — that's a different tax regime entirely.

### When to revisit this section

- Customer #5 signs: evaluate Stripe Subscriptions for auto-renewal.
- Customer #10 signs: evaluate self-serve checkout for the Pilot tier only.
- First EU customer signs: enable Stripe Tax, add VAT field to the order form.
- First customer churns: document the cancellation flow (pro-rated refund? sunset period? data export?).

---

*Iterate this doc after every discovery call. Prices go up the moment we
have three paying logos; they don't go down after that.*
