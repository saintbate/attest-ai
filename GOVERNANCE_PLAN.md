# Governance Plan — Articles 9 & 14

> **Status:** Spec (not built). Timeline: ship Article 9 flow within 2 weeks,
> Article 14 flow within 4 weeks. Revisit after first 3 discovery calls —
> this is a *response to critique*, not a customer-validated requirement yet.
>
> **Why now:** The landing-page repositioning ("runtime evidence for
> high-risk AI") is honest but narrow. Adding structured capture for
> Articles 9 and 14 closes the gap between "evidence layer" and "a thing
> you can hand your auditor" without pretending to replace a compliance
> lead. These two articles are also the ones buyers will ask about most
> often in a discovery call ("so what about risk management / human
> oversight?"). Having even a basic structured answer beats "you need a
> consultant for that."

---

## 1. Design principle

Attest **captures structure**; the customer **writes content**.

- We never generate the text of a risk register or an oversight plan.
  Auto-generated compliance prose is a credibility-destroyer.
- We provide forms, schemas, and guided questions that produce
  machine-readable YAML + human-readable Markdown.
- Every field has a "who fills this in" label so it's obvious that this
  is the customer's work product, not Attest's output.
- Every field also has an Article reference so the reviewer can audit it.

If we ever ship LLM-generated compliance language, it must be **marked
as draft** and signed by the customer before it can be exported.

---

## 2. Article 9 — Risk Management System

### What the Act actually requires

A documented, iterative, lifecycle-long process for identifying,
analysing, evaluating, and mitigating known and foreseeable risks to
health, safety, and fundamental rights. Art. 9 §2–7 list the specific
steps (identification, estimation/evaluation, adoption of measures,
testing). A single spreadsheet is the current industry norm; notified
bodies want to see it and will ask when it was last reviewed.

### What Attest ships

A per-system **risk register** stored as structured YAML, editable in
the dashboard, exportable as Markdown and OSCAL.

**Data model addition (`AISystem`):**

```python
@dataclass
class RiskEntry:
    entry_id: str
    hazard: str                 # short label ("false negative on PPE")
    description: str            # 1-2 sentence customer-written detail
    affected: str               # "worker", "operator", "third party", etc.
    likelihood: Literal["rare", "possible", "likely", "frequent"]
    severity: Literal["negligible", "marginal", "critical", "catastrophic"]
    mitigation: str             # customer-written
    mitigation_owner: str       # customer name/role
    residual_risk: Literal["low", "medium", "high", "unacceptable"]
    tested: bool = False
    last_reviewed: float | None = None
    notes: str = ""

@dataclass
class AISystem:
    ...
    risk_register: list[RiskEntry] = field(default_factory=list)
    risk_register_last_reviewed: float | None = None
    risk_register_owner: str = ""   # name + role of Art. 9 responsible person
```

**Seed hazards per Annex III category.** When a system is classified
into, say, Annex III §4 (worker monitoring), we pre-seed 5–8 common
hazards (false positive triggering unfair disciplinary action; false
negative missing a real violation; demographic performance gap; model
gaming by workers; single-point-of-failure in deployment; etc.). The
customer can delete, edit, or add. This is the most useful thing we do
here — most teams don't know where to start.

**CLI:**

```bash
attest risk init <system-id>       # scaffolds a register with seed hazards
attest risk add <system-id>        # interactive form for a new entry
attest risk list <system-id>
attest risk review <system-id>     # marks risk_register_last_reviewed = now
attest risk export <system-id>     # writes risk_register.md + .yaml
```

**Dashboard page:** `/systems/<id>/risk-register`
- Table of entries (hazard | likelihood | severity | owner | last reviewed)
- Add / edit / delete entry form
- "Review register" button that updates the timestamp and records *who*
  clicked it in a log (evidence: the register is maintained, not stale)
- Badge at the top: green if reviewed < 90 days, yellow < 180, red older

**Annex IV integration.** The existing Annex IV Markdown template gets
a new "Risk Management System" section populated from the register.
The OSCAL generator gets a new observation type `risk-register-entry`
and rolls up an Art. 9 finding status (satisfied / gap) based on
whether the register exists + has a recent review timestamp.

**What we are NOT building here:**
- Auto-generated risk descriptions.
- A judgement that the register is "adequate" — that's a notified body
  call or a self-declaration by the provider.
- Integration with the customer's corporate risk framework (we emit
  structured data; their GRC tool can ingest).

### Effort estimate

- Data model + persistence: 0.5 day
- Seed hazards by Annex III category: 1 day (content work)
- CLI: 0.5 day
- Dashboard page: 1.5 days
- Annex IV + OSCAL wiring: 0.5 day
- **Total: ~4 engineer-days**

---

## 3. Article 14 — Human Oversight

### What the Act actually requires

Measures designed to enable natural persons overseeing the system's
operation, during use, to (a) understand capacities and limits, (b)
remain aware of automation bias, (c) correctly interpret the output,
(d) decide not to use / override the output, and (e) intervene or
interrupt. Art. 14 §4 lists these explicitly.

### What Attest ships

A per-system **human oversight plan** stored as structured YAML,
editable in the dashboard, exportable as Markdown.

**Data model addition:**

```python
@dataclass
class OversightRole:
    role_id: str
    role_name: str              # "site safety officer", "reviewer"
    contact: str                # email / team
    rights: list[Literal["review", "override", "suspend", "escalate"]]
    escalates_to: str | None = None
    response_time_sla: str = "" # free text, e.g. "within 4 hours"

@dataclass
class OversightPlan:
    oversight_model: Literal["human-in-loop", "human-on-loop", "human-in-command"]
    decision_rights: list[OversightRole]
    pre_deployment_training: str = ""       # what training oversight staff got
    automation_bias_mitigations: str = ""   # Art. 14 §4(b)
    intervention_procedure: str = ""        # Art. 14 §4(e), free-text SOP
    interpretation_guidance: str = ""       # Art. 14 §4(c)
    last_reviewed: float | None = None
    owner: str = ""

@dataclass
class AISystem:
    ...
    oversight_plan: OversightPlan | None = None
```

**Guided questions** (dashboard wizard, 5 steps, ~10 minutes):
1. **Mode.** Is the model's output acted on automatically (on-loop),
   always reviewed by a person before action (in-loop), or is the
   system only advisory (in-command)? Pick one; each choice pre-fills
   template language.
2. **Who has decision rights?** Add 1–N roles with their override /
   suspend / escalate rights.
3. **Training.** Free text: how oversight staff were trained to
   understand this model's limits.
4. **Bias & intervention.** Two short paragraphs on automation bias
   mitigations and the intervention procedure.
5. **Review & sign.** Owner types their name; timestamp recorded.

**Logging tie-in (the real value).** For systems with `oversight_model
= "human-in-loop"`, we add an optional argument to `attest.wrap()`:

```python
model = attest.wrap(
    underlying_model,
    name="safety-inspector",
    purpose="PPE violation detection",
    oversight_log=True,   # new
)
```

When `oversight_log=True`, each inference includes an `oversight_decision`
field (accepted / overridden / not-reviewed-within-sla) that the
customer sets via `model.log_oversight(inference_id, "overridden",
reviewer="alice")`. The dashboard surfaces an "oversight compliance"
metric: % of high-confidence calls reviewed within SLA. This is the
Art. 14 analogue of drift detection — ongoing evidence, not just a
written plan.

**CLI:**

```bash
attest oversight init <system-id>
attest oversight review <system-id>
attest oversight export <system-id>
```

**Annex IV integration.** New section populated from `OversightPlan`.
OSCAL gets an `oversight-plan` observation and an Art. 14 finding
status based on plan existence + recent review + (for in-loop systems)
>=50% of recent high-confidence calls having an oversight decision
logged.

**What we are NOT building:**
- An oversight UI for the customer's reviewers (that lives in their app).
- A judgement on whether the plan is sufficient for a given deployment.

### Effort estimate

- Data model + persistence: 0.5 day
- Dashboard wizard: 2 days
- Oversight log plumbing (SDK-side): 1 day
- CLI: 0.5 day
- Annex IV + OSCAL wiring: 0.5 day
- **Total: ~4.5 engineer-days**

---

## 4. Rollout sequence

| Week | Work | Ship target |
|---|---|---|
| 1 | Art. 9 data model, seed hazards, CLI | Private build |
| 2 | Art. 9 dashboard + Annex IV / OSCAL wiring | Private build, demo-able |
| 3 | Art. 14 data model + wizard | Private build |
| 4 | Art. 14 oversight log + export + Annex IV / OSCAL wiring | Ready to demo in discovery calls |

Every feature must ship with an update to the landing-page "Attest
produces" list *and* the pricing page "included in every paid plan"
list. If a feature isn't worth updating the marketing copy for, it
isn't done.

---

## 5. What we're explicitly *not* solving

- **Art. 10 (data governance).** Requires documented training-data
  provenance, bias testing, and representativeness arguments. We don't
  see customer training data in production — this belongs in their
  MLOps stack (e.g. WhyLabs, Arize) plus a written policy. We emit a
  stub reference in the Annex IV doc and link out.
- **Art. 13 (transparency / instructions for use).** Customer writes
  the user-facing doc. We can provide a template in a future release.
- **Art. 43 (conformity assessment).** Notified body for Annex I
  safety-component systems; self-declaration for Annex III. Not ours.
- **Art. 47 (declaration of conformity).** Legal document signed by
  the provider. Not ours.

The landing-page scope section and PRICING.md §2 both call these out by
name. Do not let marketing or sales walk that line back.

---

## 6. Revisit triggers

Rebuild this plan if any of these happen in the first 60 days:

- A discovery call reveals a hidden article-level blocker we're
  missing (e.g. "we can't sign until we see Art. 10 support").
- A paying pilot customer churns citing insufficient Art. 9 or 14 depth.
- A horizontal competitor ships the same structured-capture approach,
  in which case we push further into *runtime* evidence (SLA logs,
  automated testing of Art. 15 robustness claims) that generic
  platforms can't cheaply replicate.
