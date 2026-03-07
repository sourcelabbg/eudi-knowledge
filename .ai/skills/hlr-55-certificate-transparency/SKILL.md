---
name: "hlr-55-certificate-transparency"
description: "Use when working with EUDI high-level requirements for 'Certificate Transparency'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.33 Topic 55 - Certificate Transparency"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~289 -->

#### A.2.3.33 Topic 55 - Certificate Transparency

| **Index** | **Requirement specification** |
| -- | -- |
| CT_01 | An Access CA issuing access certificates SHALL register these in a CT log according to RFC 9162, if such a log is available for access certificates. |
| CT_02 | An Access CA issuing access certificates SHALL describe in its CPS how it logs all access certificates. |
| CT_03 | In case a CT log provider for access certificates is available, all Access CAs SHALL act as monitors in the CT ecosystem. Access CAs SHOULD still monitor the CT logs in situations of temporary unavailability. |
| CT_04 | An Access CA SHALL include at least one Signed Certificate Timestamp (SCT) in each access certificate. |
| CT_05 | When verifying an access certificate during PID or attestation issuance or presentation, a Wallet Unit SHALL also verify that the access certificate includes at least one valid Signed Certificate Timestamp (SCT). |
| CT_06 | If an access certificate does not include a valid SCT, a Wallet Unit SHALL handle this as a failure or Relying Party authentication, in compliance with all requirements in [[Topic 6](./annex-2.02-high-level-requirements-by-topic.md#a234-topic-6---relying-party-authentication-and-user-approval)] and in particular requirement RPA_06a. |
