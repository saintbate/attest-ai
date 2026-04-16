# Attest Pilot Services Agreement — Template

> **How to use this:** copy this file to `outreach/signed/{company}-{date}.md`
> when a pilot closes, fill in the `{braces}`, export to PDF
> (`pandoc input.md -o output.pdf`), and send via DocuSign or plain email
> reply-with-"I accept".
>
> **Read before first use:**
> - This template is a **starting point drafted by a founder, not a
>   lawyer.** Before sending the first executed copy, have a US business
>   lawyer do a 30-minute review (budget $500–1,000). Repeat when anything
>   material changes.
> - Specific items to confirm with counsel: governing law / venue,
>   limitation-of-liability cap, data-processing language for EU
>   customers, whether you need an MSA + Order Form structure or a single
>   agreement is enough at this scale.
> - For customers below $10k, a shorter **letter-style agreement** (see
>   "Appendix A — Letter form" at the bottom) sent by email is often
>   cleaner than a DocuSign. Both are included here.

---

# Pilot Services Agreement

**This Pilot Services Agreement ("Agreement")** is entered into as of
**{EFFECTIVE DATE}** (the "Effective Date") by and between:

**Vertical AI LLC**, a {STATE} limited liability company with its
principal office at {ADDRESS}, doing business as "Attest" (**"Provider"**);

and

**{CUSTOMER LEGAL NAME}**, a {CUSTOMER JURISDICTION} {entity type} with its
principal office at {CUSTOMER ADDRESS} (**"Customer"**).

Provider and Customer are each a "Party" and together the "Parties."

---

## 1. Services

1.1 **Pilot Program.** Provider will deliver the "Attest Pilot," a
90-day engagement consisting of:

- (a) Access to the Attest software development kit ("SDK") and
  compliance dashboard for use with up to **three (3)** AI systems
  operated by Customer (each, a "System");
- (b) One (1) onboarding call of up to sixty (60) minutes;
- (c) A written Classification and Gap Analysis Report for each System,
  mapping the System to EU AI Act risk categories and identifying
  outstanding provider obligations under Chapter III, Section 2 of
  Regulation (EU) 2024/1689;
- (d) One (1) initial Annex IV technical documentation export per
  System, in Markdown and OSCAL-aligned JSON format;
- (e) Drift monitoring on one (1) metric per System, with alerts
  delivered to an email or webhook of Customer's choosing;
- (f) Email support with a two (2) business-day response target.

1.2 **Exclusions.** The Pilot does **not** include: legal advice, notified-body
certification, on-site consulting, custom integrations beyond the items
listed in §1.1, or any warranty of regulatory outcome. Provider is not a
notified body, a law firm, or Customer's designated compliance officer.

1.3 **Out of Scope Work.** Additional services may be provided on
written request at **$200 per hour**, subject to a separately agreed
written statement of work.

---

## 2. Term

2.1 This Agreement begins on the Effective Date and continues for
**ninety (90) calendar days** (the "Pilot Term") unless terminated
earlier under §9.

2.2 **Conversion.** At least fifteen (15) days before the end of the
Pilot Term, the Parties will discuss whether to convert the engagement
to Provider's annual "Team" subscription (currently $12,000 per year,
up to five Systems). If converted within thirty (30) days after the
Pilot Term ends, **the $2,500 Pilot fee will be credited against the
first annual Team fee.** Conversion terms will be memorialized in a
separate Order Form.

---

## 3. Fees and Payment

3.1 **Pilot Fee.** Customer will pay Provider a one-time fee of
**USD $2,500** (the "Pilot Fee") for the Services described in §1.

3.2 **Invoice.** Provider will issue an invoice on the Effective Date.
The Pilot Fee is **due on receipt** unless otherwise stated on the
invoice.

3.3 **Taxes.** The Pilot Fee is exclusive of sales, use, VAT, or
similar taxes. Customer is responsible for any such taxes imposed on
the purchase of Services, excluding taxes based on Provider's net
income. For EU-established Customers providing a valid VAT
identification number, reverse-charge VAT applies pursuant to Article
196 of Council Directive 2006/112/EC.

3.4 **Late Payment.** Undisputed amounts not paid within thirty (30)
days of the invoice date may accrue interest at 1.0% per month or the
maximum permitted by applicable law, whichever is lower.

---

## 4. Customer Responsibilities

Customer will:

- (a) identify a technical contact authorized to integrate the SDK and
  attend the onboarding call;
- (b) provide reasonable information about each System (name,
  description, purpose, deployment context, framework) required for
  classification;
- (c) not attempt to reverse engineer, redistribute, or sublicense the
  SDK except as expressly permitted;
- (d) use the Services in compliance with applicable law.

---

## 5. Data and Confidentiality

5.1 **Architecture.** The Attest SDK runs inside Customer's runtime
environment and logs inference metadata to a database controlled by
Customer (by default, a local SQLite file). **Provider does not receive
raw model inputs or outputs** under the Pilot. Information shared with
Provider under §1.1(c) (Classification and Gap Analysis) is limited to
what Customer chooses to disclose.

5.2 **Confidentiality.** Each Party agrees to keep the other Party's
non-public information confidential and to use it only for purposes of
this Agreement. Obligations survive for two (2) years after the end of
the Pilot Term. Standard exclusions apply for information that is
public, independently developed, or required to be disclosed by law.

5.3 **No Personal Data.** The Services are not designed to process
personal data. If Customer expects to share personal data with Provider,
a separate Data Processing Addendum must be executed first.

---

## 6. Intellectual Property

6.1 **Provider IP.** Provider retains all right, title, and interest in
the Attest SDK, dashboard, documentation templates, and any
improvements thereto. Provider grants Customer a non-exclusive,
non-transferable, revocable license during the Pilot Term to use the
SDK and Services solely for Customer's internal business purposes.

6.2 **Customer IP.** Customer retains all right, title, and interest in
Customer's AI systems, training data, inference data, and any
Classification and Gap Analysis Report or Annex IV documentation
generated for Customer under this Agreement.

6.3 **Feedback.** If Customer provides suggestions or feedback,
Provider may use that feedback without obligation, provided Provider
does not identify Customer as the source without Customer's prior
written consent.

---

## 7. Warranties and Disclaimers

7.1 **Mutual.** Each Party warrants that it has authority to enter this
Agreement.

7.2 **Disclaimer.** **THE SERVICES ARE PROVIDED "AS IS." PROVIDER DOES
NOT WARRANT THAT THE SERVICES WILL CAUSE CUSTOMER TO BE COMPLIANT WITH
THE EU AI ACT OR ANY OTHER LAW, REGULATION, OR STANDARD.** Compliance
is ultimately determined by the competent authorities and notified
bodies; the Services are intended to assist Customer's compliance
program, not replace it. All other warranties, express or implied,
including merchantability and fitness for a particular purpose, are
disclaimed to the extent permitted by law.

---

## 8. Limitation of Liability

8.1 Except for breaches of §5 (Confidentiality) or §6 (Intellectual
Property), **each Party's total aggregate liability arising out of or
relating to this Agreement shall not exceed the total fees paid or
payable by Customer under this Agreement** (i.e., the Pilot Fee).

8.2 **Excluded Damages.** Neither Party will be liable for any
indirect, incidental, consequential, special, punitive, or exemplary
damages, or for lost profits or lost business, even if advised of the
possibility of such damages.

---

## 9. Termination

9.1 **For Convenience.** Either Party may terminate this Agreement for
convenience upon thirty (30) days' written notice.

9.2 **For Cause.** Either Party may terminate this Agreement
immediately on written notice if the other Party materially breaches
this Agreement and fails to cure within fifteen (15) days of receiving
written notice of the breach.

9.3 **Effect of Termination.** Upon termination, Customer's license
under §6.1 ends. If Customer terminates for Provider's uncured material
breach, Provider will refund the pro-rated unused portion of the Pilot
Fee. Sections 3 (amounts owing), 5, 6, 7, 8, and 10 survive termination.

---

## 10. General

10.1 **Governing Law and Venue.** This Agreement is governed by the
laws of the State of {STATE}, without regard to conflicts-of-law
principles. The Parties consent to the exclusive jurisdiction of the
state and federal courts located in {COUNTY}, {STATE}.

10.2 **Entire Agreement.** This Agreement is the entire agreement of
the Parties and supersedes any prior agreements regarding the subject
matter. Amendments must be in writing signed by both Parties.

10.3 **Assignment.** Neither Party may assign this Agreement without
the other's prior written consent, except in connection with a merger,
acquisition, or sale of substantially all assets.

10.4 **Notices.** Notices under this Agreement must be in writing and
sent by email to **batemannick66@gmail.com** (Provider) or
**{CUSTOMER NOTICE EMAIL}** (Customer), with acknowledgment of receipt.

10.5 **Force Majeure.** Neither Party is liable for delays or failures
caused by events beyond reasonable control.

10.6 **Counterparts; Electronic Signature.** This Agreement may be
signed in counterparts, including by electronic signature, each of
which is an original and all of which together form one instrument.

---

## Signatures

**Vertical AI LLC ("Provider")**

Signature: ____________________________

Name: Nicholas Bateman

Title: {Founder / Managing Member}

Date: ________________

---

**{CUSTOMER LEGAL NAME} ("Customer")**

Signature: ____________________________

Name: {CUSTOMER SIGNATORY NAME}

Title: {CUSTOMER SIGNATORY TITLE}

Date: ________________

---

# Appendix A — Letter form (for customers <$5k who want low friction)

For first-draft pilots with friendly counterparties, an email-reply
agreement can replace the full document above. Use sparingly and
**only when the customer prefers speed over formality.**

```
Subject: Attest Pilot — please reply "I accept" to confirm

Hi {FirstName},

This email sets out the terms of the Attest Pilot for {CustomerName}.
If you reply "I accept" (or ask for edits), we're engaged.

1. Services: the Attest Pilot as described on
   https://attest-ai-eta.vercel.app/pricing.html — up to 3 AI systems,
   90-day term starting {Effective Date}, one onboarding call, a
   classification + gap analysis report, first Annex IV + OSCAL export,
   and drift alerts on one metric per system.

2. Fee: USD $2,500, due on receipt. I'll send a Stripe invoice on the
   Effective Date; ACH or card both work.

3. Conversion: if you move to our Team plan within 30 days of the
   pilot ending, the $2,500 is credited against year one.

4. Data: Attest runs in your environment. I don't receive raw inputs
   or outputs. I treat anything you share in writing as confidential
   for two years.

5. Limits: Attest is evidence-generation and monitoring software, not
   legal advice and not a notified-body certification. My liability
   under this engagement is capped at the fee you pay.

6. Either of us can cancel on 30 days' written notice; if I'm in
   uncured material breach, you get a pro-rated refund.

7. Governing law: {STATE}, USA.

Reply "I accept" and I'll send the invoice and our onboarding call
link today.

Best,
Nick
Vertical AI LLC
batemannick66@gmail.com
```

---

## Changelog

- **v0.1 ({DATE})** — initial draft. Not yet reviewed by counsel. Do
  not use for contracts above $10k or for customers in the EEA until
  reviewed.
