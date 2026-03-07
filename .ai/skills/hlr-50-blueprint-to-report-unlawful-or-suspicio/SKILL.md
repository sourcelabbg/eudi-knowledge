---
name: "hlr-50-blueprint-to-report-unlawful-or-suspicio"
description: "Use when working with EUDI high-level requirements for 'Blueprint to report unlawful or suspicious request of data'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.28 Topic 50 - Blueprint to report unlawful or suspicious request of data"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~861 -->

#### A.2.3.28 Topic 50 - Blueprint to report unlawful or suspicious request of data

| **Index** | **Requirement specification** |
| -- | -- |
| RPT_DPA_01 | A Wallet Unit SHALL enable the User to start the process of reporting a suspicious presentation request to a DPA. When prompted by the User, a Wallet Unit SHALL provide the contact details of the DPA which supervises the Relying Party that made the suspicious request, if available in the log for that request (see DASH_03). If the contact details of the supervising DPA are not available in the log, the Wallet Unit SHALL provide the contact details of the DPA of the region in which the Wallet Provider is residing. In addition, the Wallet Unit MAY also provide the contact details of other DPAs, taken from the European Data Protection Board website (<https://www.edpb.europa.eu/about-edpb/about-edpb/members_en>). *Note: The DPA contact details may be unavailable in the log if there was no registration certificate in the presentation request and the User did not request the Wallet Unit to obtain the information registered about the Relying Party from the Registrar. See RPRC_16 - RPRC_18 in [Topic 44](./annex-2.02-high-level-requirements-by-topic.md#a2326-topic-44---registration-certificates-for-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties).* |
| RPT_DPA_02 | The Wallet Unit SHALL offer the User the option to report a suspicious request to a DPA via the transaction log presented in the dashboard, see [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency). |
| RPT_DPA_02a | A Wallet Unit SHALL support at least the following possibilities to report a suspicious presentation request to a DPA, depending on what contact details are available for the DPA: a) Open a URL in an external browser to report the request in a web form provided by the DPA. b) Open an external e-mail client and start a draft e-mail to the DPA, with a suitable template text, c) open an external phone client and start a phone call. |
| RPT_DPA_03 | Empty |
| RPT_DPA_04 | A Wallet Provider SHALL ensure that a Wallet Unit allows its User to substantiate a report sent to a DPA, including by attaching relevant information to identify the Relying Party and the Users' claims in a machine-readable format. *Note: The log kept by the Wallet Unit is standardised in [Technical Standard 10](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts10-data-portability-and-download-(export).md) and is machine-readable in order to enable data portability. An excerpt from this log therefore can be used to substantiate the report.* |
| RPT_DPA_05 | A Wallet Unit SHALL log the fact that it initiated the sending of a report to a DPA (see RPT_DPA_02a), as specified in [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency). |
| RPT_DPA_05a | For a report sent to a DPA, the log SHALL contain at least: a) the date and time when the report was sent, b) the name and country of the DPA, and c) the channel and contact information used for initiating sending the report, i.e., the URL, e-mail address, or phone number of the DPA. |
| RPT_DPA_06 | Wallet Units, Data Protection Authorities, and Registrars SHALL comply with the relevant requirements in [Technical Specification 8](../../technical-specifications/ts8-common-interface-for-reporting-of-wrp-to-dpa.md). |
