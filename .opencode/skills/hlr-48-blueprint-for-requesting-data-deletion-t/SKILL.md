---
name: "hlr-48-blueprint-for-requesting-data-deletion-t"
description: "Use when working with EUDI high-level requirements for 'Blueprint for requesting data deletion to Relying Parties'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.27 Topic 48 - Blueprint for requesting data deletion to Relying Parties"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~848 -->

#### A.2.3.27 Topic 48 - Blueprint for requesting data deletion to Relying Parties

| **Index** | **Requirement specification** |
| -- | -- |
| DATA_DLT_01 | A Wallet Provider SHALL ensure that its Wallet Units support the possibilities mentioned in DATA_DLT_02, allowing a User to request from a Relying Party the erasure of their attributes that were presented by that Wallet Unit to that Relying Party, in accordance with Article 17 of Regulation (EU) 2016/679. |
| DATA_DLT_02 | A Wallet Unit SHALL support at least the following possibilities to send a data erasure request to a Relying Party: a) Open a URL in an external browser to ask for the deletion of data in a web form provided by the Relying Party, b) Open an external mail client and start a draft e-mail to the Relying Party, with a suitable template text, c) open an external phone client and start a phone call. Depending on whether a Relying Party URL, e-mail address, and/or phone number was logged for the relevant attestation presentation transaction (see requirement DASH_03 in [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency)), the Wallet Unit SHALL offer the User to use one or more of these possibilities. |
| DATA_DLT_02a | If the User initiates sending a data erasure request for a particular attestation presentation transaction, but no Relying Party URL, e-mail address, or telephone number is available in the log for that transaction, the Wallet Unit SHALL connect to the URL of the online service of the Registrar indicated in the log to obtain this information. The Wallet Unit SHALL inform the User that it must connect to the Registrar to look up the contact information it needs to send a data deletion request. *Note: This situation may occur if there was no registration certificate in the presentation request and the User did not request the Wallet Unit to obtain the information registered about the Relying Party from the Registrar. See RPRC_16 - RPRC_18 in [Topic 44](./annex-2.02-high-level-requirements-by-topic.md#a2326-topic-44---registration-certificates-for-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties).* |
| DATA_DLT_03 | A Wallet Instance SHALL provide a function where the User may select one Relying Party to which a data deletion request must be submitted. |
| DATA_DLT_04 | Empty |
| DATA_DLT_05 | A Wallet Unit SHALL include the initiation of a data deletion request in a log, so it can be displayed to the User via the dashboard as specified in [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency). *Note: Because the request is sent by an external web browser, e-mail client, or phone client (see DATA_DLT_02), the Wallet Unit can only log the initiation of the request.* |
| DATA_DLT_06 | For the initiation of a data deletion request, the log SHALL contain at least: - Date and time of the initiation of the request, - Name and unique identifier of the Relying Party to which the request was made, - Attributes requested to be deleted. |
| DATA_DLT_07 | Before executing a data deletion request, a Relying Party SHALL authenticate the requesting User (or the request itself), using appropriate authentication mechanisms of its own choosing. The Relying Party SHOULD use the authentication or signature facilities offered by the User's Wallet Unit for this purpose. |
| DATA_DLT_08 | Wallet Units, Relying Parties, and Registrars SHALL comply with the relevant requirements in [Technical Specification 7](../../technical-specifications/ts7-common-interface-for-data-deletion-request.md). |
