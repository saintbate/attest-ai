# Input Evidence Plan

> **Status:** Minimum version (v1) shipped Apr 2026 — SHA-256 hash of
> input + customer-supplied reference. Medium (v2) and Maximum (v3)
> versions specified but not built; do not start on v2 until a paying
> customer asks for snapshot capture by name.
>
> **Why this exists:** Many of our outreach targets (Buildots, viAct,
> OpenSpace, Smartvid, DeepQual) are camera-based AI vendors. Article 12
> logging for their systems must be reproducible at audit time, and the
> underlying video typically cannot leave the customer's environment.
> Input evidence linking is how we bridge those two constraints.

---

## 1. Design principle

> Attest never stores customer inputs. We store references.

Every escalation of this feature keeps that principle. v1 stores a hash
and an optional reference. v2 stores low-resolution snapshots **only at
explicit customer opt-in** and only for flagged alerts. v3 stores short
clips **only under a signed DPA and only for regulated-industry
customers on paid plans**. If we ever need to violate this principle to
close a deal, we walk away from the deal.

---

## 2. v1 — Minimum (shipped)

### What the customer enables

```python
import attest

model = attest.wrap(
    my_model,
    name="safety-inspector",
    purpose="PPE violation detection",
    hash_input=True,
)

result = model(frame)

if result["confidence"] > 0.9:
    model.log_evidence(
        ref="s3://customer-bucket/frames/2026-04-16T14:33:02.123Z.jpg",
        source_type="image/jpeg",
    )
```

### What Attest captures

- SHA-256 of the input frame (from `numpy` array, `PIL.Image`, `torch`
  tensor, `bytes`, or a file path). Never the frame itself.
- Size in bytes (for audit-time verification).
- Source-type string (`image/array/uint8`, `video_frames/array/uint8`,
  `tensor/float32`, `image/jpeg`, etc.).
- Customer-supplied `ref` — typically an object-store path, a frame ID,
  a presigned URL, or a monotonic timestamp.

### What ships in OSCAL

A new observation type `Input evidence linking (Article 12
reproducibility)` with properties:

- `evidence_hash_coverage` — fraction of inferences with a hash
- `evidence_ref_coverage` — fraction with a customer reference
- `evidence_records_total`

### Cost

~10-30 ms of extra per-inference latency on typical image inputs
(hashing is the bottleneck). Zero storage overhead — a hash is 64
characters.

### What it does NOT cover

- Inputs that never enter the wrap boundary (e.g. preprocessing happens
  *before* `attest.wrap()` sees them, changing the bytes → hash doesn't
  match raw frame)
- Streams where customer rotates frames faster than we hash

---

## 3. v2 — Medium (specified, not built)

### Trigger to build

A paying customer (any tier) explicitly asks for visual audit evidence
AND agrees in writing that Attest may store low-resolution snapshots
for alerts above a threshold.

### What the customer enables

```python
model = attest.wrap(
    my_model,
    name="safety-inspector",
    purpose="PPE violation detection",
    hash_input=True,
    capture_snapshot_on=lambda result: result.get("confidence", 0) > 0.9,
    snapshot_resolution=(320, 240),
    snapshot_format="jpeg",
    snapshot_quality=60,
)
```

### What Attest adds

- Downscaled JPEG snapshot (~20-50 KB) stored on the customer's own
  Attest instance (self-hosted) or in a customer-owned S3/GCS bucket
  that Attest writes to via IAM role.
- Snapshot is linked to the inference record by UUID.
- Dashboard renders the snapshot next to the inference event for
  oversight review.
- Snapshot retention mirrors inference-log retention (10 years).

### Data-handling requirements (blockers before v2 ships)

- Written DPA (data processing agreement) template for customers.
- Documented snapshot storage location (customer-controlled default).
- GDPR Art. 28 processor language in the MSA.
- Clear data subject access flow: given an evidence UUID, return or
  delete the snapshot on customer request.
- Snapshot encryption at rest (AES-256, customer-managed keys option).
- Opt-in per-system, never global.
- Under no circumstances do we snapshot on *every* inference — only on
  the alert predicate.

### Engineering cost

~3-5 engineer-days given the v1 scaffolding. Dashboard work is the
largest slice.

---

## 4. v3 — Maximum (specified, not built)

### Trigger to build

A paying Scale-tier ($36k/yr) or Enterprise customer in a regulated
industry (construction safety, medical imaging, critical
infrastructure) asks for event-linked clips as part of their conformity
assessment preparation.

### What the customer enables

```python
model = attest.wrap(
    my_model,
    name="safety-inspector",
    purpose="PPE violation detection",
    hash_input=True,
    capture_clip_on=lambda result: result.get("confidence", 0) > 0.9,
    clip_pre_roll_s=2,
    clip_post_roll_s=3,
    clip_storage="s3://customer-bucket/attest-clips/",
)
```

### What Attest adds

- 5-second clip around each high-confidence alert, encoded via ffmpeg,
  stored in a customer-owned bucket Attest writes to.
- Clip is linked to the inference record and to the OSCAL Evidence
  bundle as a `link` resource.
- Dashboard clip player with timeline scrubbing and frame-by-frame
  review. Linked to the oversight-decision flow from the Art. 14
  feature (see `GOVERNANCE_PLAN.md`).
- Per-clip access log (who viewed what, when) for chain-of-custody
  evidence at audit time.

### Data-handling requirements (blockers)

Everything in v2 plus:

- Minimum 90-day professional indemnity insurance.
- A reviewed-and-signed BAA template if any customer approaches
  healthcare-adjacent workloads (medical construction, hospital
  surveillance).
- A privacy-impact-assessment template pre-populated for customers.
- Chain-of-custody guarantees: write-once object-lock on clip storage.
- Auto-redaction option (blur faces / license plates) via a plug-in
  interface — we do *not* ship the redaction model ourselves; we
  ship the plug-in contract.

### Engineering cost

~2-3 engineer-weeks including the chain-of-custody logging, clip
player, oversight integration. Non-trivial.

---

## 5. What we're deliberately not doing at any tier

- **Training on customer visual data.** Ever. Not for internal drift
  baselines, not for anything.
- **Cross-customer data pooling.** Each customer's evidence lives in
  their own instance or bucket; we don't aggregate snapshots or clips.
- **Shipping a face / license-plate redaction model.** Too much legal
  exposure around false-negative claims. We provide the plug-in
  contract only.
- **Accepting clip storage on Attest-managed infrastructure by
  default.** Customer-owned storage is the default; we will not
  operate a central clip vault.

---

## 6. Upgrade path reference

| Version | Stores | Cost | Customer needs to sign |
|---|---|---|---|
| v1 (shipped) | Hash + ref only | ~1 engineer-day | Standard MSA |
| v2 (spec) | + low-res snapshots on alert | 3-5 engineer-days | MSA + DPA |
| v3 (spec) | + 5-second event clips | 2-3 engineer-weeks | MSA + DPA + (BAA if healthcare-adjacent) |

Move up a tier only when a paying customer asks by name. Do not
speculatively build down the roadmap.
