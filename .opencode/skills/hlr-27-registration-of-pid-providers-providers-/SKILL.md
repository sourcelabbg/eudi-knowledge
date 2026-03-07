---
name: "hlr-27-registration-of-pid-providers-providers-"
description: "Use when working with EUDI high-level requirements for 'Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.16 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties"
  - "A. General requirements for Member State registration processes <!-- omit from toc -->"
  - "B. General requirements for the issuance of access certificates <!-- omit from toc -->"
  - "C. Requirements for the registration of PID Providers <!-- omit from toc -->"
  - "D. Requirements for the registration of Attestation Providers <!-- omit from toc -->"
  - "E. Requirements for the registration of Relying Parties <!-- omit from toc -->"
  - "F. Requirements for the contents of access certificates <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~2084 -->

#### A.2.3.16 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties

##### A. General requirements for Member State registration processes <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_01 | Member States SHALL provide processes and mechanisms for PID Providers, QEAA Providers, PuB-EAA Providers, non-qualified EAA Providers, and Relying Parties to register in a registry. *Note: Member States may choose to implement a single registry for all these roles, or a separate registry for each of these roles.* |
| Reg_01a | Member States SHALL register a common set of data about a) PID Providers, b) QEAA Providers, c) PuB-EAA Providers, d) non-qualified EAA Providers. and e) Relying Parties, according to the relevant requirements in [Technical Specification 6](../../technical-specifications/ts6-common-set-of-rp-information-to-be-registered.md). *Note: For PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers, the common set of data specified in [Technical Specification 6] include the attestation type(s) that the provider intends to issue to Wallet Units.* |
| Reg_01b | Empty |
| Reg_02 | Member States SHALL make publicly available all necessary details and documentation about the registration processes for their registry. |
| Reg_03 | Member States SHALL publish the registry entries online, in a sealed or signed machine-readable common format suitable for automated processing, according to the relevant requirements in [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md), for the purpose of transparency to Users and other stakeholders. |
| Reg_04 | Member States SHALL make the registry entries available online, in a human-readable format. The website used for this purpose SHALL use a secure channel protecting the authenticity and integrity of the information in the registry during transport. Member States SHALL NOT require authentication or prior registration and authorisation of any person wishing to retrieve the information in the registry. |
| Reg_05 | Empty |
| Reg_06 | Member States SHALL support the common API specified in [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md) for to enable automated retrieval of registry entries from the Member States' registries. *Note: [Technical Specification 5] specifies the use of a secure channel protecting the authenticity and integrity of the information in the registry during transport, and does not require authentication or prior registration and authorisation of any entity wishing to retrieve the information in the registry.* |
| Reg_07 | A Member State SHALL enable a registered PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party to update the information registered on it, using a process comparable to the original registration process. For Relying Parties, this SHALL be possible using the API or user interface mentioned in Reg_24. |
| Reg_08 | A registered PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party SHALL make any updates necessary to ensure the continued correctness of the registered information without undue delay. |
| Reg_09 | Member States SHALL log all changes made on the information registered regarding a PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party, including at least initial registration, updates, deletion of information, and suspension or cancellation. |

##### B. General requirements for the issuance of access certificates <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_10 | A Member State SHALL ensure that an Access Certificate Authority notified according to [[Topic 31](./annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---notification-and-publication-of-pid-provider-wallet-provider-attestation-provider-access-certificate-authority-and-provider-of-registration-certificates)] issues an access certificate to all PID Providers, QEAA Providers, PuB-EAA Providers, non-qualified EAA Providers registered in one of the Member State's registries. |
| Reg_10a | A Member State SHALL ensure that an Access Certificate Authority notified according to [[Topic 31](./annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---notification-and-publication-of-pid-provider-wallet-provider-attestation-provider-access-certificate-authority-and-provider-of-registration-certificates)] issues one or more access certificates to all Relying Parties registered in one of the Member State's registries. A Relying Party SHALL receive a separate access certificate for each of its Relying Party Instances. |
| Reg_11 | A Member State SHALL ensure that the issuance process of access certificates by their notified Access Certificate Authority(s) complies with ETSI TS 119 411-8. In addition, the Access Certificate Authority(s) SHALL comply with at least the normalised certificate policy (‘NCP’) requirements as specified in ETSI EN 319- 411-1. |
| Reg_12 | Empty |
| Reg_13 | Empty |
| Reg_14 | Empty |
| Reg_15 | Empty |
| Reg_16 | Empty |
| Reg_17 | Empty |
| Reg_18 | Empty |

##### C. Requirements for the registration of PID Providers <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_19 | A Member State SHALL approve a PID Provider according to a well-defined policy before including it in its PID Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of PID Providers in its Registry. |
| Reg_20 | A Member State SHALL identify PID Providers at a level of confidence proportionate to the risk arising from the potential harm a fraudulent PID Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |
| Reg_20a | A Registrar SHALL provide a method to suspend or cancel a registered PID Provider. |
| Reg_20b | A Registrar SHALL have a policy for the suspension or cancellation of a registered PID Provider, which SHALL specify that a PID Provider is suspended or cancelled at least on request of the PID Provider or of a competent national authority. |

##### D. Requirements for the registration of Attestation Providers <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_21 | A Member State SHALL approve an Attestation Provider according to a well-defined policy before including it in its Attestation Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of Attestation Providers in its Registry. These processes and rules SHOULD consider any relevant differences between QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers. |
| Reg_22 | A Member State SHALL identify Attestation Providers (i.e., QEAA Providers, PuB-EAA Providers and non-qualified EAA Providers) at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Attestation Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |
| Reg_22a | A Registrar SHALL provide a method to suspend or cancel a registered Attestation Provider. |
| Reg_22b | A Registrar SHALL have a policy for the suspension or cancellation of a registered Attestation Provider, which SHALL specify that an Attestation Provider is suspended or cancelled at least on request of the Attestation Provider or of a competent national authority. |

##### E. Requirements for the registration of Relying Parties <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_23 | Empty |
| Reg_24 | A Member State SHALL enable a Relying Party to register remotely, using an API or user interface. |
| Reg_25 | A Member State SHALL identify a Relying Party at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Relying Party could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |
| Reg_26 | With respect to Reg_25, a Member State SHALL consider whether a registering entity intends to act as an intermediary. *Note: According to the [European Digital Identity Regulation], an intermediary is a Relying Party.* |
| Reg_27 | Empty |
| Reg_28 | Empty |
| Reg_29 | A Member State SHALL have a policy for the cancellation of a registered Relying Party, which SHALL specify that a Relying Party is cancelled at least on request of the Relying Party or of a competent national authority. |
| Reg_30 | Empty |

##### F. Requirements for the contents of access certificates <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Reg_31 | An access certificate SHALL contain a name for the PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party, in a format suitable for presenting to a User. |
| Reg_32 | The common Certificate Policy mentioned in Reg_12 SHALL require that an access certificate contains an EU-wide unique identifier for the PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party, and SHALL specify a method for deriving such identifiers. *Note: a) The EU-wide unique identifier could, for example, be a composition of a unique identifier of the Registrar, defined in the policy, and a unique identifier for the Relying Party allocated by this Registrar. b) This Relying Party identifier is identical in all access certificates issued to a given entity.* |
| Reg_33 | Empty |
