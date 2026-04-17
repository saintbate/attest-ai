# Post-Call Follow-Up Templates

> **Use when:** you've just finished a 20-30 min discovery call and need to
> turn conversation into a decision. Paste into Gmail, fill in `{braces}`,
> remove any section that doesn't apply.
>
> **Rule:** send within 4 hours of the call. Momentum is everything.

---

## 1. Warm close — they sounded ready

**When to use:** On the call they named a real pain (EU customer ask,
deadline pressure, a specific system they're worried about). They didn't
say "let me think about it" — they asked procurement questions.

**Subject:** `Next steps — {CompanyName} + Attest`

```
Hi {FirstName},

Thanks for the time today. Quick recap of what I heard:

- You're operating {N} AI systems in EU deployments, with {specific
  system they flagged} as the most exposed under Annex III §{4|2|1}.
- {Deployer / customer name} has already asked about AI Act readiness —
  or will within the next {weeks|quarter}.
- Building the Article 11 technical file in-house would pull {X weeks of
  eng time | their compliance engineer} off the roadmap.

Based on that, Attest Team ($12,000/yr, up to 5 high-risk systems) is
the right starting tier. Covers your {flagged system} and gives you room
to add {N+1 / N+2} without a tier change.

Scope reminder so there's no surprise later: Attest produces the
**runtime evidence** the Act's technical articles require — inference
logs (Art. 12), drift signals (Art. 15/72), Annex III classification,
Annex IV + OSCAL docs (Art. 11). Your team still owns the risk
management system (Art. 9), oversight design (Art. 14), and conformity
assessment sign-off (Art. 43). We don't sell a consultant substitute.

Pricing and what's in each plan:
https://attest-ai-eta.vercel.app/pricing.html

Proposed next step: a 90-day paid pilot at $2,500 — we wrap your first
model together on a call next week, deliver a classification + gap
analysis, and produce your first Annex IV + OSCAL export. If it earns
Team tier at the 90-day mark, we roll it in with the pilot fee credited.

Reply with a thumbs up and I'll send the order form Monday. Want to
loop in {procurement / other stakeholder they mentioned}?

Best,
Nick
Vertical AI LLC

https://github.com/saintbate/attest-ai
https://attest-ai-eta.vercel.app
```

---

## 2. Neutral close — interested but not decided

**When to use:** They liked it, they get it, but they said something like
"we'll discuss internally" or "let me check with {boss / legal / co-founder}."

**Subject:** `Re: Attest — two things to help the internal conversation`

```
Hi {FirstName},

Appreciate the honest read today. Two things to make the internal
discussion easier:

1. One-page pricing + scope, so you're not summarizing from memory:
   https://attest-ai-eta.vercel.app/pricing.html

2. A sample Annex IV that Attest generates from runtime data — this is
   what {CompanyName} would hand to {deployer / auditor} on day one.
   {attach sample_annex_iv.md  OR  "happy to send one privately if
   useful — it's based on a public demo, not a real customer"}

The thing I'd flag: the {specific risk you raised on the call — e.g.
"VINCI asking for documentation", "your EU launch in Q3",
"the hire you're trying to avoid"} has a real clock. August 2 is
enforcement for high-risk. Whatever you decide on Attest, decide soon
enough to act on it.

Happy to join a second call with {CTO / legal / co-founder} if that
shortens the loop — I can do a focused 15-minute version that skips the
background and goes straight to what they'd need to sign off on.

Best,
Nick
Vertical AI LLC
```

---

## 3. Cool close — they flagged a real blocker

**When to use:** Budget, timing, competing internal initiative, or "we
already have {vendor X}". Don't fight — acknowledge and leave a door open.

**Subject:** `Re: Attest — no rush, one check-in`

```
Hi {FirstName},

Totally fair. {Repeat back the blocker in one sentence, e.g. "Getting
through the current release is the priority and compliance tooling is
Q3 at the earliest."}

Three things in case they're useful later:

- Pricing page if you want to bookmark: https://attest-ai-eta.vercel.app/pricing.html
- What I'd watch for: the first time {deployer name / a prospect}
  sends you a compliance questionnaire or asks for an Article 11
  technical file. That's when the calculus usually shifts.
- I'll check in {date — 4-8 weeks out}, not sooner. If something
  changes before then, you know where to find me.

No reply needed. Keep building.

Best,
Nick
Vertical AI LLC
```

---

## 4. No-show — they booked but didn't join

**When to use:** 10 minutes past the call time, no message. Don't make it
awkward. Send a short note.

**Subject:** `Missed you — easy to rebook`

```
Hi {FirstName},

Something came up on your end — no worries. Here's a Calendly or just
reply with two 30-min windows that work next week and I'll take the
earlier one:

{calendly link OR "mornings work best on my side, any day next week"}

Pricing and background in case you want a head start:
https://attest-ai-eta.vercel.app/pricing.html

Best,
Nick
Vertical AI LLC
```

---

## 5. The "not today but keep us posted" response — how to reply

**When to use:** They replied to your initial outreach with "interesting,
let's talk later in the year / after {release}." You want to stay warm
without being annoying.

**Subject stays on the thread.**

```
Thanks {FirstName} — makes sense. I'll check back in {month}.

One thing worth knowing now even if we don't speak again until then:
{ONE specific fact relevant to their company, pulled from the research
— e.g. "Annex III §4 (worker management) is where your progress-
monitoring CV most likely lands, not §2."}

If {specific triggering event — "a customer sends an AI Act
questionnaire", "a new EU deployment is announced", "BSI or a notified
body reaches out"} happens before then, we can move faster than a full
sales cycle — a pilot can be live in a week.

Best,
Nick
```

---

## Operating rules

1. **Send within 4 hours of the call.** Momentum > polish.
2. **Always include the pricing URL.** Don't make them ask twice.
3. **One clear ask per email.** If the ask is "sign the order form",
   don't also ask for a second call. If the ask is "bring your CTO",
   don't also attach a PDF.
4. **Never copy-paste the recap — write it fresh.** It takes 3 minutes
   and it's the part they actually read.
5. **Log the reply (or lack of one) in PRICING.md's "Open questions"
   or in a simple `outreach/_log.md`.** Patterns matter more than any
   single call.
6. **State scope honestly, once, in every follow-up.** If they think
   Attest is a full compliance solution and sign on that belief, they
   churn at renewal. Name Art. 9 / 14 / 43 out loud so the line is clear.
