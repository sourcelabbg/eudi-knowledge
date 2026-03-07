---
name: "arf-trust-model"
description: "Use when understanding the EUDI trust framework, provider registration, and lifecycle management for Wallet Providers, PID Providers, Attestation Providers, and Relying Parties."
sections:
  - "6.1 Scope"
  - "6.2 Trust throughout a Wallet Provider lifecycle"
  - "6.2.1 Wallet Provider lifecycle"
  - "6.2.2 Wallet Provider notification"
  - "6.2.3 Wallet Provider invalidation"
  - "6.3 Trust throughout a PID Provider or an Attestation Provider lifecycle"
  - "6.3.1 PID Provider or Attestation Provider lifecycle"
  - "6.3.2 PID Provider or Attestation Provider registration and notification"
  - "6.3.3 Suspension or cancellation of the registration of a PID Provider or Attestation Provider"
  - "6.4 Trust throughout a Relying Party lifecycle"
  - "6.4.1 Relying Party lifecycle"
  - "6.4.2 Relying Party registration"
  - "6.4.3 Relying Party suspension or cancellation"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~6170 -->

### 6.1 Scope

This chapter explains how trust works in the EUDI Wallet system, how it is established,
maintained, validated, and managed. It describes the rules and assumptions that decide
whether different parts of the system, like a wallet app, a user's device, or a
service provider, can be trusted.

![Figure 12](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_12_Trust_Model.png)

```mermaid
stateDiagram-v2
  state "Relying Party Instance" as tklJ06Eg1gI686ZZUtUN-59
  state "Wallet Provider" as tklJ06Eg1gI686ZZUtUN-58
  state "Relying Party" as tklJ06Eg1gI686ZZUtUN-57
  state "tklJ06Eg1gI686ZZUtUN-56" as tklJ06Eg1gI686ZZUtUN-56
  state "tklJ06Eg1gI686ZZUtUN-53" as tklJ06Eg1gI686ZZUtUN-53
  state "2" as 2
  state "Relying Party" as 3
  state "Wallet Unit" as 20
  state "Wallet Provider" as 19
  state "Relying Party Instance" as 11
  state "Common trust infrastructure(Metadata + URLs of the Trusted Lists and LoTEs)EU Commisson" as 5
  state "- PID Provider- Attestation Provider&nbsp; (QEAA/EAA/Pub-EAA" as 6
  state "RegistrarMember States" as 14
  state "OqG462VzuzaBs0EC9eQU-37" as OqG462VzuzaBs0EC9eQU-37
  state "WUA" as tklJ06Eg1gI686ZZUtUN-42
  state "AccesCA" as tklJ06Eg1gI686ZZUtUN-44
  state "Provider of registrationcertificates" as tklJ06Eg1gI686ZZUtUN-47
  state "tklJ06Eg1gI686ZZUtUN-60" as tklJ06Eg1gI686ZZUtUN-60
  state "RegistrarMember States" as tklJ06Eg1gI686ZZUtUN-61
  state "AccesCA" as tklJ06Eg1gI686ZZUtUN-62
  state "Provider of registrationcertificates" as tklJ06Eg1gI686ZZUtUN-63
  state "tklJ06Eg1gI686ZZUtUN-67" as tklJ06Eg1gI686ZZUtUN-67
  state "Member States" as tklJ06Eg1gI686ZZUtUN-68
  state "User" as tklJ06Eg1gI686ZZUtUN-71
  19 --> 20 : Issues<br/>WUAs
  19 --> 20 : AuthN
  20 --> 11 : AuthN & AuthZ<br/>Request PIDs,<br/>attestations
  11 --> 3 : Send registration<br/>certificate(s)<br/>(optional)
  11 --> tklJ06Eg1gI686ZZUtUN-44 : Issue access<br/>certificate
  3 --> tklJ06Eg1gI686ZZUtUN-44 : Issue access<br/>certificate
  3 --> tklJ06Eg1gI686ZZUtUN-47 : Issue registration<br/>certificates(s)<br/>(optional)
  6 --> tklJ06Eg1gI686ZZUtUN-62 : Issue access<br/>certificate(s)
  6 --> tklJ06Eg1gI686ZZUtUN-63 : Issue<br/>registration<br/>certificate(s)<br/>(optional)
  19 --> tklJ06Eg1gI686ZZUtUN-68 : Registers as<br/>Wallet Provider
```

Figure 12 illustrates the main entities and their relationships in the trust model
of the EUDI Wallet ecosystem.

At its core is the **Wallet Unit** (top middle, blue), which interacts with
various entities throughout its lifecycle. The Wallet Unit lifecycle is detailed
in [Section 6.5](#65-trust-throughout-a-wallet-unit-lifecycle) and consists of
installation, activation, management, and uninstallation. Each Wallet Unit is a
configuration of a **Wallet Solution**, comprising a
**Wallet Instance**, a **WSCA/WSCD**, and one or more **keystores**, provided by
a **Wallet
Provider** or by the **User's device**. The User installs a Wallet Instance on their device, which leads to the activation of the Wallet Unit by the Wallet Provider. The Wallet Provider manages a Wallet Unit until it is uninstalled by the User.
The Wallet Provider ensures that a valid Wallet Unit is in possession of at
least one **Wallet Unit Attestation (WUA)** and at least one **Wallet Instance Attestation (WIA)**, which can serve as an attestation of cryptographic keys and of the Wallet Instance, respectively, towards PID Providers or Attestation Providers. The Wallet Provider can revoke the WUAs, if
needed, to revoke the Wallet Unit. See [Section 6.5](#65-trust-throughout-a-wallet-unit-lifecycle).

The Wallet Unit handles User **PIDs** and **attestations** (QEAAs, PuB-EAAs, and
non-qualified EAAs). PIDs are issued by **PID Providers** and attestations by
**Attestation Providers**, both positioned to the left of the Wallet Unit in
[Figure 12](#61-scope). Before interacting with a Wallet Unit, these Providers
must be registered by a **Registrar**. Upon registration, they receive an
**access certificate** from a
**Access Certificate Authority** associated with the Registrar. They may
optionally obtain a **registration certificate** from an associated
**Provider of registration certificates**.
See [Section 6.3](#63-trust-throughout-a-pid-provider-or-an-attestation-provider-lifecycle).

After a Wallet Unit has received a PID or attestation, it can present **User
attributes** to **Relying Party Instances** (right side of [Figure
11](#61-scope)). These instances are hardware/software setups enabling
**Relying Parties** to interact with Wallet Units. Like a PID Provider or
Attestation Providers, Relying Parties register with a
**Registrar** in their Member State, and receive an **access certificate** for
each of their Relying Party Instances.
A Relying Party may optionally obtain one or more
**registration certificates** from a Provider of registration certificates
*associated with the Registrar. This is discussed in [Section 6.4](#64-trust-throughout-a-relying-party-lifecycle).

Notes:

- This conceptual trust model may be implemented with slight variations across
Member States, such as adopting one or multiple Certification Authorities or
leveraging existing entities that already fulfil this role.
- For PIDs, qualified EAAs, PuB-EAAs, access certificates, and registration
certificates, interoperability is essential ([Section
4.2.3](#423-interoperability)). Interoperability is achieved by using a PKI
following X.509 certificate standards
([RFC5280](https://datatracker.ietf.org/doc/html/rfc5280),
[RFC3647](https://datatracker.ietf.org/doc/html/rfc3647)). Non-qualified EAAs
may adopt alternative trust models and verification mechanisms.
- The model supports both remote and proximity use cases, though technical
measures and authentication mechanisms may vary.
- This version of the ARF does not yet include trust interactions for
qualified electronic signatures or seals; see [Topic 16](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2310-topic-16---signing-documents-with-a-wallet-unit)
and [Topic 37](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2337-topic-37---qes----remote-signing---technical-requirements)
in Annex 2.
- Besides the trust relationships described in this chapter, other trust
relations are established as well. For instance, Users, PID Providers,
Attestation Providers, and Relying Parties trust certification bodies and
Trusted List or LoTE Providers. This trust is primarily rooted in authority and in
procedural measures, such as public oversight, published security and
operational policies, and audits, rather than in technical measures. To verify
that entities are indeed interacting with a trusted authority, standard
technical measures suitable for the context will be used.

### 6.2 Trust throughout a Wallet Provider lifecycle

#### 6.2.1 Wallet Provider lifecycle

[Section 4.6.2](#462-wallet-provider) presented the lifecycle of a Wallet Provider:

1. The Wallet Provider is notified to the
Commission by a Member State. This is discussed in [Section 6.2.2](#622-wallet-provider-notification).
1. Under specific conditions, a Member State may decide to change the status of a
registered Wallet Provider to Invalid. This is discussed in [Section 6.2.3](#623-wallet-provider-invalidation).

#### 6.2.2 Wallet Provider notification

[Figure 12](#61-scope) depicts the Wallet Provider to the top of the Wallet
Unit. To the left and below of this, the figure also shows that a Member State notifies the Wallet Provider and its (certified) Wallet Solution(s) to the European Commission. Note that Wallet Providers are not registered in the sense of [CIR 2025/848], like Relying Parties, PID Providers, and Attestation Providers are. Wallet Providers consequently do not receive access certificates or registration certificates. This is because there is no need for interoperability between Wallet Providers and Wallet Unit; each Wallet Provider only needs to communicate with its own Wallet Units.

The Wallet Solution provided by the Wallet Provider is certified as described in
[Chapter 7](#7-wallet-solution-certification-and-risk-management).

If the notification process is successful, the trust anchors
of the Wallet Provider are included in a Wallet Provider LoTE. During
issuance of a PID or an attestation, the PID Provider or the Attestation
Provider can use these trust anchors to verify the authenticity of a WIA and WUA
Attestation signed by the Wallet Provider, so they can be sure they are dealing
with an authentic Wallet Unit from a trusted Wallet Provider.
See [Section 6.6.2.3](#6623-pid-provider-or-attestation-provider-validates-the-wallet-unit),
[Topic 9](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation).

More details on the Wallet Provider notification process can be found in [Topic 31](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---notification-and-publication-of-pid-provider-wallet-provider-attestation-provider-access-certificate-authority-and-provider-of-registration-certificates).

#### 6.2.3 Wallet Provider invalidation

The Member State may decide to notify the Commission that the Wallet Provider's status in the
corresponding LoTE should be changed to Invalid. As a result of this status
change, PID Providers and Attestation Providers will no longer
trust the trust anchors of the Wallet Provider, which they need to verify the WUAs and WIAs they receive from Wallet Units. They will therefore refuse to issue PIDs and attestations to any Wallet Unit provided by that Wallet Provider. The Member State can subsequently notify the Commission that the Wallet Provider's status should be changed to Valid again.

Note that independently of the status of the Wallet Provider, its Wallet Solution may be suspended or cancelled, see [Section 4.6.3](#463-wallet-solution). In that case, the Wallet Provider (if necessary) revokes all associated Wallet Units, see [Section 6.5.4.2](#6542-wallet-unit-revocation). The result is the same: PID Providers and Attestation Providers will stop issuing PIDs and attestations to these Wallet Units.

### 6.3 Trust throughout a PID Provider or an Attestation Provider lifecycle

#### 6.3.1 PID Provider or Attestation Provider lifecycle

[Section 4.6.5](#465-pid-provider-or-attestation-provider) presented the
lifecycle of a PID Provider or Attestation Provider:

1. A PID Provider or an Attestation Provider is registered by a Registrar in its Member State. This is discussed in [Section 6.3.2](#632-pid-provider-or-attestation-provider-registration-and-notification).
2. Under specific conditions, the REgistrar may decide to suspend or
cancel registration of a registered PID Provider or Attestation Provider. This
is discussed in [Section 6.3.3](#633-suspension-or-cancellation-of-the-registration-of-a-pid-provider-or-attestation-provider).

#### 6.3.2 PID Provider or Attestation Provider registration and notification

##### 6.3.2.1 Introduction

[Figure 12](#61-scope) depicts the PID Providers and Attestation Providers to
the left of the Wallet Unit. To the left and below of this, the figure also
shows that each PID Provider and Attestation Provider will register itself with
a Registrar in its Member
State. The Member State conditionally notifies a PID Provider or Attestation Provider to the
European Commission:

- **PID Providers** are notified to the Commission.
- **QEAA Providers** are not notified to the Commission, except for establishing the [Art. 22](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2014.257.01.0073.01.ENG#d1e2162-73-1) Trusted List once a qualified status is granted.
- The purpose of the notification of **PuB-EAA Providers** is mainly to the attention of QTSPs issuing qualified certificates for electronic signatures or seals to PuB-EAA Providers. QTSPs are expected to verify the Trusted List of PuB-EAA Providers prior to issuing a qualified certificate to any entity claiming to be a PuB-EAA Provider.
- **Non-qualified EAA Providers** are not notified to the Commission.

If the registration and notification processes are successful, at least the
following happens:

- Data about the PID Provider or Attestation Provider is included in the
registry of the relevant Registrar.
- The PID Provider or Attestation Provider receives an access certificate and
optionally one or more registration certificates.
- The trust anchors of the PID Provider or Attestation Provider are conditionally included in
a Trusted List or LoTE.

These processes are discussed in the next subsections.

##### 6.3.2.2 Data about the PID Provider or Attestation Provider is included in the registry

When a PID Provider or Attestation Provider is registered, the Registrar
registers a set of data about the PID Provider or Attestation Provider in its
register. The Registrar makes the contents of the register available to the
general public, both in machine-readable and human-readable format. High-level
requirements on the registration process can be found in [Topic 27](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2316-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties).

The data to be registered about a PID Provider, QEAA Provider, PuB-EAA Provider,
or EAA Provider includes the attestation type(s) that the Provider intends to
issue to Wallet Units. This enables Wallet Units and Relying Parties to verify
that a given PID Provider or Attestation Provider registered its intent to issue
a specific attestation type. For example, a PuB-EAA Provider may have registered
for issuing mDLs, but not to issue diplomas.

Regarding PID Providers or QEAA Providers it may be argued that Wallet Units do
not have to do this verification, since these are trusted parties. Nevertheless,
it is beneficial if a Wallet Unit verifies if a PID Provider or QEAA Provider is
registered for issuing a PID or a particular type of QEAA, prior to requesting
the issuance of such a PID or QEAA. Doing this helps to prevent attempts to
issue a PID or attestation while not being entitled to do so, either
fraudulently or as a result of an error.

##### 6.3.2.3 PID Provider or Attestation Provider receives an access certificate and a registration certificate

When a PID Provider or Attestation Provider is registered by a Member State, a
Access Certificate Authority (see [Section 3.18](#318-access-certificate-authorities)
issues an access certificate to the PID Provider or to the Attestation
Provider. A PID Provider or an Attestation Provider needs such a certificate to
authenticate itself towards a Wallet Unit when issuing a PID or an attestation
to it, as described in [Section 6.6.2.2](#6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider).

A PID Provider access certificate does not indicate that its subject is a PID
Provider. Similarly, an Attestation Provider access certificate does not
indicate that its subject is a QEAA Provider, a PuB-EAA Provider, or a
non-qualified EAA Provider. Furthermore, the access certificate of a PID
Provider or Attestation Provider does not contain the Provider's registration to
issue attestations of a specific type, for instance an mDL or diploma. Such
information is included in the registration certificates (if issued), and in any
case available in the Registrar's online service.

Such information is instead available via the Registrar's online service.
Additionally, the same information is included in a registration certificate
issued to the PID Provider or Attestation Provider by a Provider of registration
certificates, if the Registrar has a policy of issuing such certificates - see
[Section 3.17](#317-registrars). To manage both situations, either with use of a
registration certificate or without, the Credential Issuer metadata of a PID
Provider or Attestation Provider contains a URL to the Registrar's online
service, which a Wallet Unit can use to obtain information on the Provider's
registration. A Wallet Unit can use the information in the registration
certificate (or obtained from the Registrar service) to verify that an
Attestation Provider it is contacting to issue a specific type of attestation is
in fact registered for that type of attestation.

Note that an Attestation Provider may simultaneously be a Relying Party, for
instance in case it intends to request data from the User's PID during issuance
of an attestation. Such an Attestation Provider would then register both as a
Relying Party (which is called a Service Provider in [Technical Specification 5](./technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md))
and as a QEAA Provider, PuB-EAA Provider, or non-qualified EAA Provider. In that
case, the Attestation Provider will receive a single registration certificate
including both roles. Registration certificates for Relying Parties are
discussed in [Section 6.4.2](#642-relying-party-registration).

See [Section 6.6.2.2](#6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider)
to learn more about how Wallet Units may use a PID Provider's or Attestation
Provider's registration certificate.

##### 6.3.2.4 PID Provider or Attestation Provider trust anchors are conditionally included in a Trusted List or LoTE

For a PID Provider, successful
registration and notification also means that the PID Provider is notified to the
European Commission and that its trust anchors are included in a LoTE. Similarly, the trust anchors of a QEAA Provider are included in a Trusted List once it gets the qualified status.
Relying Parties can use these trust anchors to verify the authenticity of PIDs
and QEAAs they obtain from Wallet Units.

Although PuB-EAA Providers are notified to the Commission, no trust anchors will
be included in the corresponding Trusted List. This is because Relying Parties
do no need such trust anchors for the verification of a PuB-EAA. Instead, a
Relying Party will need the trust anchor of the QTSP that signed the qualified
certificate of the PuB-EAA Provider. See [Section 6.6.3.6](#6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation)
for more details.

Non-qualified EAA Providers are not notified and their trust anchors are not
included in a Trusted List or LoTE by a Member State. However, if a Relying Party
requests a non-qualified EAA from a Wallet Instance, it must know how to obtain
the domain-specific trust anchor it needs to verify the signature over that EAA.
To help with this, [Topic 12](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a239-topic-12---attestation-rulebooks)
recommends that the applicable Rulebook specifies the mechanisms enabling this.
This mechanism may be a LoTE. However, other methods may be used as well, and even
if such a LoTE exists, it does not have to comply with the requirements
in [Topic 31](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---pid-provider-wallet-provider-attestation-provider-and-access-certificate-authority-notification-and-publication).

High-level requirements on the PID Provider or Attestation Provider notification
process, as well as on the information registered and published in the respective Trusted List or LoTE, can be found in
[Topic 31](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---pid-provider-wallet-provider-attestation-provider-and-access-certificate-authority-notification-and-publication).

#### 6.3.3 Suspension or cancellation of the registration of a PID Provider or Attestation Provider

Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a PID Provider or Attestation Provider. The conditions for this
will be specified by each Registrar.

Suspension or cancellation implies that the PID Provider's or Attestation Provider's
access certificates are revoked. As a result, the PID Provider or Attestation
Provider will no longer be able to issue PIDs or attestations to Wallet Units.

For a PID Provider, QEAA Provider, or PuB-EAA Provider, suspension or
cancellation also implies that its status in the respective Trusted List or LoTE will be
changed to Invalid. As a result, Relying Parties will no longer trust PIDs or
attestations issued by that Provider. For non-qualified EAA Providers, the
applicable Rulebook (see [Topic 12](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a239-topic-12---attestation-rulebooks))
may define similar mechanisms ensuring that Relying Parties will no longer
trust the trust anchors of EAA Providers of which the registration was suspended
or cancelled.

When a Registrar suspends or cancels the registration of a PID Provider or Attestation
Provider, the PID Provider or Attestation Provider revokes all of their PIDs or
attestations as described in [Section 6.6.3.7](#6637-relying-party-verifies-that-the-pid-or-attestation-is-not-revoked).

### 6.4 Trust throughout a Relying Party lifecycle

#### 6.4.1 Relying Party lifecycle

[Section 4.6.7](#467-relying-party) presented the lifecycle of a Relying Party:

1. A Relying Party is registered by a Registrar in the Member State where it
resides. Relying Party registration is discussed in [Section 6.4.2](#642-relying-party-registration).
2. Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a Relying Party. This is discussed in [Section 6.4.3](#643-relying-party-suspension-or-cancellation).

#### 6.4.2 Relying Party registration

[Figure 12](#61-scope) depicts the Relying Party Instance to the right of the
Wallet Unit. A Relying Party Instance is a combination of hardware and software
used by a Relying Party to interact with a Wallet Unit. A Relying Party can operate
multiple Relying Party Instances. This will happen especially in case the
interactions with the Wallet Unit take place in proximity; for instance, a
border control agency at an airport employing multiple lines (each operated by
an agency employee) where arriving passengers can present their PID. However, a
single Relying Party operating multiple Relying Party Instances can also happen
in a remote context, for example if there is an operational system (including a
remote Relying Party Instance) next to a fallback system used for business
continuity purposes. A Relying Party may also use multiple remote Relying Party
Instances for load distribution.

[Figure 12](#61-scope) also shows the Relying Party. Below that, it shows that
each Relying Party will register itself with a Registrar in its Member State.
If the registration process is successful, the Registrar includes the Relying
Party in its public registry.

A Relying Party may register in the context of several services, having different
intended uses. Each intended use will require a different set of attributes to be
obtained from a Wallet Unit. As a result, a single Relying Party may register
multiple times and may be issued more than one registration certificate.

As a result of successful registration,

- a Provider of registration certificates (see [Section 3.19](#319-providers-of-registration-certificates))
associated with the Registrar will issue one or more registration certificates
to the Relying Party, if the Member State has a policy of issuing such registration
certificates. The purpose of the registration certificate is described in
[Section 6.6.3.3](#6633-wallet-unit-allows-user-to-verify-that-relying-party-does-not-request-more-attributes-than-it-registered).
Issuing registration certificates is optional. However, if registration certificates are issued, the Provider of registration certificates complies with the harmonised requirements in Implementing Regulation (EU) 2025/848 (including those for the associated policy and practice statement in Annex V).
- an Access Certificate Authority (see [Section 3.18](#318-access-certificate-authorities))
associated with the Registrar issues an access certificate to each Relying Party
Instance of the Relying Party. A Relying Party Instance needs such a certificate
to authenticate itself towards Wallet Units when requesting the presentation of
attributes, as described in [Section 6.6.3.2](#6632-wallet-unit-authenticates-the-relying-party-instance).
Issuing access certificates to a registered Relying Party is mandatory.

High-level requirements on the Relying Party registration process can be found
in [Topic 27](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2316-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties).

#### 6.4.3 Relying Party suspension or cancellation

Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a registered Relying Party. The conditions for this will be
specified by each Registrar.

Suspension or cancellation involves revocation of all valid access certificates of the Relying Party by the relevant Access CA, such that the Relying
Party is no longer able to interact with Wallet Units.
