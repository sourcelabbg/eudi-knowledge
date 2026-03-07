---
name: "arf-issuance-reqs"
description: "Use when implementing PID or attestation issuance, including lifecycle states, batch issuance, key binding, and trust requirements between issuers and wallet units."
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~5096 -->

#### 6.6.1 PID or attestation lifecycle

[Section 4.6.6](#466-pid-or-attestation) above presented the lifecycle of a PID
or attestation within a Wallet Unit:

1. Using their Wallet Unit, the User requests the issuance of a PID or an
attestation from a PID Provider or an Attestation Provider. The required trust
relationships for issuance are discussed in [Section 6.6.2](#662-pid-or-attestation-issuance)
below.
2. Once the PID or attestation is issued into the Wallet Unit, the User can
present attributes from it to a Relying Party Instance, according to the User's
decision and depending on successful authentication of the Relying Party. The
required trust relationships for presenting PIDs and attestations, including
User approval and Relying Party authentication, are discussed in [Section 6.6.3](#663-pid-or-attestation-presentation-to-a-relying-party).
3. Instead of presenting attributes to a Relying Party, a User can also present
them to another User, meaning that their Wallet Unit is interacting with another
Wallet Unit. This is discussed in [Section 6.6.4](#664-pid-or-attestation-presentation-to-another-wallet-unit).
4. The PID Provider or the Attestation Provider remains responsible for managing
the PID or attestation over its lifetime. Management may include re-issuing the
PID or attestation with the same or with different attribute values. The
Provider can also revoke the PID or the attestation, possibly based on a request
of the User. The management of PIDs and attestations is discussed in [Section 6.6.6](#666-pid-or-attestation-management).
5. Finally, [Section 6.6.7](#667-pid-or-attestation-deletion) discusses what
happens if a User decides to delete a PID or an attestation from their Wallet
Unit.

#### 6.6.2 PID or attestation issuance

##### 6.6.2.1 Required trust relationships

The lifecycle of a PID or an attestation starts when a User, using their Wallet
Unit, requests a PID Provider or an Attestation Provider to issue the PID or an
attestation to their Wallet Unit. The following trust relationships are
established during issuance:

1. The Wallet Unit authenticates the PID Provider or Attestation Provider using
the access certificate referred to in [Section 6.3](#63-trust-throughout-a-pid-provider-or-an-attestation-provider-lifecycle).
This ensures that the User can trust that the PID or attestation they are about
to receive, is issued by an authenticated PID Provider or Attestation Provider
respectively. See [Section 6.6.2.2](#6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider)
below describing how this will be done.
2. The PID Provider or Attestation Provider authenticates the User, meaning that
the Provider is sure about the identity of the User. This is necessary to enable
determination of the values of the attributes that the Provider will attest to.
For instance, a PID Provider needs to authenticate the User to ensure it
provides a PID containing the correct family name and date of birth. The method
by which the PID Provider or Attestation Provider performs User identification
and authentication is out of scope of the ARF, as these processes are specific
to each PID Provider or Attestation Provider. However, for a PID, these
processes will satisfy the requirements for Level of Assurance High in
[Commission Implementing Regulation (EU) 2015/1502](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015R1502).
For other attestations, user authentication is performed on a security level
commensurate with the required level of security for the attestation issued.
3. The PID Provider or Attestation Provider authenticates and validates the
Wallet Unit, see [Section 6.6.2.3](#6623-pid-provider-or-attestation-provider-validates-the-wallet-unit)
below.
4. The PID Provider or Attestation Provider verifies that the Wallet Provider
did not revoke the Wallet Unit. This is described in [Section 6.6.2.4](#6624-pid-provider-or-attestation-provider-verifies-that-wua-is-not-revoked).
5. After the PID or attestation is issued to the Wallet Unit, the Wallet Unit
verifies the authenticity of the PID or attestation; see [Section 6.6.2.5](#6625-wallet-unit-verifies-pid-or-attestation).
6. The User will activate a PID before they can use it; see [Section 6.6.2.6](#6626-user-activates-the-pid).
7. If the [OpenID4VCI] Credential Issuer metadata for an attestation contains an
embedded disclosure policy, the Wallet Unit
retrieves the policy and stores it locally, so that it can apply the policy in
case a Relying Party requests attributes from the attestation. See [Section 6.6.2.7](#6627-provisioning-embedded-disclosure-policies).

More detailed requirements for the issuance process of PIDs and attestations,
for instance regarding the issuance protocol, are included in [Topic 10](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a237-topic-10---issuing-a-pid-or-attestation-to-a-wallet-unit).

##### 6.6.2.2 Wallet Unit authenticates the PID Provider or Attestation Provider

As shown in [Figure 12](#61-scope), a Wallet Unit downloads the LOTE(s) for Access
Certificate Authorities and Providers of registration certificates from the relevant Trusted List or LoTE Provider(s), possibly after having located them via the Commission common trust
infrastructure. Similarly, the Wallet Unit downloads all Trusted Lists and LoTEs for PID Providers and Attestation Providers. See [Section 6.3.2](#632-pid-provider-or-attestation-provider-registration-and-notification)
for more information on these Trusted Lists and LoTEs.

To start the process of requesting a PID or an attestation, the User directs the
Wallet Unit to contact the PID Provider or Attestation Provider. The User may
for example use the Wallet Unit to scan a QR code or tap an NFC tag to do so.
Note that no centralised service discovery mechanism for PID or attestation
issuance is foreseen.

Before requesting the issuance of a PID or an attestation, the Wallet Unit
authenticates the PID Provider or the Attestation Provider. To do so, the Wallet
Unit verifies the access certificate presented to it by the PID Provider or
Attestation Provider in its Issuer metadata according to [OpenID4VCI].
Additionally, to verify the legal status of the Provider and the type(s) of
attestation it issues, the Wallet Unit checks the registration information
contained in the registration certificate (if available in the Issuer metadata)
or in the online service of the Registrar indicated in the access certificate.

The Wallet Unit also verifies that the access certificate and registration
certificate (if provided) are valid and authentic.

##### 6.6.2.3 PID Provider or Attestation Provider validates the Wallet Unit

###### 6.6.2.3.1 Verifies the authenticity of the Wallet Unit

As shown in [Figure 12](#61-scope), a PID Provider or an Attestation Provider
downloads the Wallet Provider LoTE(s) it needs from the relevant Trusted
List or LoTE Provider(s), possibly after having located them via the Commission's common
trust infrastructure.

Note that for PID Providers it is not mandatory to possess all Wallet Provider
LoTEs, if there are multiple. This is because it is not mandatory for a
PID Provider to accept all certified Wallet Solutions in the EUDI Wallet
ecosystem. Each PID Provider will choose which LoTEs they need to
subscribe to. This is different for Attestation Providers: they must accept all
Wallet Solutions and hence must possess all Wallet Provider LoTEs.

[Section 6.5.3](#653-wallet-unit-activation) above described that a Wallet
Provider issues WUAs and WIAs to the Wallet Unit. When the Wallet Unit requests the issuance of a PID or an attestation, it sends a WIA, and in most cases also a WUA, to the PID Provider or the Attestation Provider. The PID Provider or Attestation Provider verifies the signature
over the WIA and the WUA, using the Wallet Provider trust anchor obtained from the Trusted
List. This proves that the Wallet Unit is authentic and is provided by a trusted Wallet
Provider. For more details see [Topic 9](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation) and [Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md).

###### 6.6.2.3.2 Optionally, validates the properties of the WSCA/WSCD or the keystore

A WUA describes the certifications and the other relevant properties of the
WSCA/WSCD or a keystore. The security level of the WSCA/WSCD is a key determinant for reaching
the overall Level of Assurance (LoA) High, as required for the PID in the Wallet
Unit. PID Providers therefore may want to validate a WUA describing the WSCA/WSCD to verify that the WSCA/WSCD indeed complies with the requirements for Level of Assurance High.

For other device-bound attestations, the Attestation Provider decides on the
required level of security and indicates this in the Credential Issuer metadata specified in [OpenID4VCI]. The Wallet Unit selects a WSCA/WSCD or keystore that complies with this, and sends a WUA describing this WSCA/WSCD or keystore to the Attestation Provider. The Attestation Provider can validate the WUA to verify that the WSCA/WSCD or keystore indeed complies with its security requirements.

###### 6.6.2.3.3 Verifies that key for new PID or device-bound attestation is protected by the WSCD or keystore

Knowing the properties of the WSCA/WSCD or keystore is not very useful if the PID Provider or
Attestation Provider cannot be sure that the private key for their new PID or device-bound
attestation is indeed protected by that WSCA/WSCD. To enable this, each WUA contains one or more public keys. By including these keys into a WUA, the Wallet Provider attests that all of the associated private keys are indeed stored in the WSCA/WSCD or keystore described in the WUA. This ARF does not specify how the Wallet Provider verifies that this is indeed the case. However, the Wallet Provider could use the mechanisms for key attestation as provided by the OS of the User's device. The PID Provider or Attestation Provider can use each of these keys to bind a new PID or attestation to.

Apart from verifying the authenticity of the WUA, the PID Provider or Attestation Provider also must verify that the WUA is bound to the context of the PID or attestation issuance process. In other words, that it was not copied and replayed by an attacker. [OpenID4VCI] and [Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md) describe two methods for doing so. In both methods, during the issuance process, the PID Provider or Attestation Provider sends a nonce to the Wallet Unit. Subsequently it verifies that either

- The WUA contains this nonce, meaning that the Wallet Provider signed it during the issuance process, or
- The Wallet Unit signed this nonce using the private key corresponding to one of the public keys in the WUA, thereby proving possession of that key.

##### 6.6.2.4 PID Provider or Attestation Provider verifies that WUA is not revoked

[Section 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit)
above described that a Wallet Provider issues one or more Wallet Unit Attestations (WUA) to the Wallet Unit. A WUA
contains revocation information. During the lifetime of the Wallet Unit, the
Wallet Provider regularly verifies that the security of the Wallet Unit is not
breached or compromised. If the Wallet Unit is no longer secure, the Wallet
Provider revokes all of the corresponding WUAs. The WUA thus allows PID
Providers and Attestation Providers to verify that the Wallet Unit is not
revoked.

Moreover, [Section 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit)
also explains that [CIR 2024/2977] requires that PID Providers must verify
regularly, during the entire lifetime of the PID, whether the Wallet Unit on
which that PID is residing is revoked by the Wallet Provider. They can do this
using the revocation information in the WUA they received during PID issuance.
PID Providers must also verify regularly whether the Wallet Provider has been
suspended or cancelled in the associated LoTE. If either of these events
happens, the PID Provider must revoke the PID. Therefore, by verifying the
revocation status of the PID, the Relying Party Instance implicitly verifies the
revocation status of the Wallet Unit. See [Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md)
for more information.

Attestation Providers can use the same mechanism as well, to provide the same assurance
to Relying Parties, although this is not required by the CIR. See also [Section 6.6.3.12](#66312-relying-party-optionally-trusts-issuer-to-regularly-verify-that-wallet-unit-is-not-revoked).

[Topic 38](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2322-topic-38---wallet-unit-revocation)
describes Wallet Unit revocation in more detail.

Once it has done all verifications, the PID Provider or Attestation Provider
will issue the PID or attestation to the Wallet Unit.

##### 6.6.2.5 Wallet Unit verifies PID or attestation

After the Wallet Unit receives the PID or attestation, it will

- verify that the PID or attestation it received matches the request.
- verify the signature of the PID or attestation, using the appropriate trust
anchor if available, in the same way as described for a Relying Party Instance in [Section 6.6.3.6](#6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation). Note that for a non-qualified attestation, the Wallet Unit may not be in possession of the necessary trust anchor.
- show the contents (i.e., attribute values) of the new PID or attestation to
the User and request the User's approval for storing the new PID or attestation.
When requesting approval, the Wallet Unit shows the contents of the PID or
attestation to the User. The Wallet Unit also informs the User about the
identity of the PID Provider or Attestation Provider, using the subject
information from the PID Provider's or Attestation Provider's access certificate.

If any of these verifications fail, the Wallet Unit will delete the PID or
attestation, and will inform the User that issuance was not successful.
Otherwise, the Wallet Unit will store the PID or attestation and will inform the
User that issuance was successful. If it supports the Digital Credentials API,
see [Section 4.4.3](#443-remote-presentation-transaction-flows), the Wallet Unit
will also disclose the fact that it contains the new PID or attestation to the Digital
Credentials API framework, unless the User has disabled such disclosure.

##### 6.6.2.6 User activates the PID

[Commission Implementing Regulation (EU) 2015/1502](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015R1502)
requires that for an eID means on Level of Assurance High, an activation process
is implemented to verify that the eID means was delivered only into the
possession of the person to whom it belongs. In the context of the EUDI Wallet,
this means that it must be verified that a PID is issued into the Wallet Unit of
the PID subject. Note that activation is required only for PIDs, since the
[European Digital Identity Regulation] only requires PIDs to be issued at LoA
High.

PID Providers, in combination with Wallet Providers, have to ensure that the PID
issuing process complies with this requirement, see also requirement ISSU_05 in
Annex 2. During certification the responsible CAB decides whether the
implemented process is indeed compliant.

The ARF does not specify a process or mechanism for PID activation. PID
Providers and Wallet Providers are free to specify a suitable mechanism. Several
options have been suggested, but others may be used as well:

1. Wallet Providers, PID Providers, and CABs could decide that no additional
mechanism for PID activation is needed, if they conclude that existing
mechanisms are sufficient to ensure that the new PID can only end up on the
device used by the subject of the PID:
    - User authentication to the Wallet Unit that starts the request for PID issuance,
    - Mutual authentication and secure communication between the Wallet Unit and
    the PID Provider (as specified in [OpenID4VCI]), and
    - User authentication to the PID Provider using an eID means on LoA High or
    another identification means, as part of the PID issuance process.
2. Another option is to let the WSCA/WSCD perform identity matching during PID
issuance. This would require that the Wallet Provider identifies the Wallet
User, and puts some identifying data, for instance User first and last name, in
the WSCA/WSCD. Then, during PID issuance, the WSCA verifies that the data in the
new PID match the data stored in the WSCA/WSCD.
3. A third option is to perform activation by using an activation code shared
via a trusted channel. In this setup, the Wallet Provider would identify the
Wallet User and store a random activation code in the WSCA/WSCD. The Wallet
Provider would share the activation code with the relevant PID Provider,
indicating the Wallet User's identity. During PID issuance, the PID Provider
would retrieve the correct activation code and send the code to the PID
subject's known address. To activate the PID, the PID subject (who is also the
Wallet User) enters the code in the Wallet Instance.

Note that options 2 and 3 introduce a need for the Wallet Provider to identify
the Wallet User. As explained in [Section 6.5.3.6](#6536-wallet-provider-sets-up-a-user-account-for-user),
this is not needed for any other purpose, and any implications for the privacy
of the User need to be assessed. Also, these options require additional
functionality of the Wallet Instance and the WSCA/WSCD, which would probably
mean that PID activation can be done only for specific combinations of a Wallet
Provider and a PID Provider. However, as pointed out in [Section 6.5.2.3](#6523-user-validates-that-wallet-solution-is-usable-with-relevant-pid),
this is allowed.

##### 6.6.2.7 Provisioning embedded disclosure policies

##### 6.6.2.7.1 Introduction

During attestation issuance, an Attestation Provider can optionally create an
embedded disclosure policy for the attestation. If so, the Attestation Provider
will provide it to Wallet Units during attestation issuance, by including it in
the Issuer metadata (defined in [OpenID4VCI]) for that attestation. Such an
embedded disclosure policy contains rules determining which (types of) Relying
Parties are allowed by the Attestation Provider to receive the attestation.

Note that the [European Digital Identity Regulation] does not contain a requirement
for PIDs to be able to contain an embedded disclosure policy, but only for QEAAs
and PuB-EAAs.

For more information regarding embedded disclosure policies, please refer to the
[Discussion Paper for Topic D](./discussion-topics/d-embedded-disclosure-policies.md).

###### 6.6.2.7.2 Types of embedded disclosure policies

Annex III of [CIR 2024/2979] defines the following common embedded
disclosure policies that must be supported:

> 1. 'No policy' indicating that no policy applies to the electronic attestations
of attributes.
> 2. 'Authorised relying parties only policy', indicating that wallet users may only
disclose electronic attestations of attributes to authenticated relying parties
which are explicitly listed in the disclosure policies.
> 3. 'Specific root of trust' indicating that wallet users should only disclose
the specific electronic attestation of attributes to authenticated wallet-relying
parties with wallet-relying party access certificates derived from a specific
root (or list of specific roots) or intermediate certificate(s).

The first of these policies is the default and will be applied if the
Attestation Provider does not provide an embedded disclosure policy for an
attestation.

For expressing conditions on Relying Parties, an embedded disclosure policy will
refer to information included in the access certificate provided to the Wallet
Unit by the Relying Party. Note that access certificates are signed and hence
the information they contain is authenticated.

Wallet Units, as well as the mechanisms used for defining and evaluating
policies, will provide support for at least policies 2. and 3. above. The
Commission will ensure a technical specification is created that specifies how
these policies will be formatted.

###### 6.6.2.7.3 Distributing embedded disclosure policies

An Attestation Provider will provide an embedded disclosure policy, if any, in
the Credential Issuer metadata specified in [OpenID4VCI]. This does not require
modifications to the attestation format. Embedded disclosure policies will be
integrated directly into the metadata, rather than being "linked" using a URL
and stored by the Attestation Provider. The approach ensures that the Wallet
Unit is not required to communicate with the Attestation Provider in order to be
able to obtain and evaluate a policy for an attestation requested by a Relying
Party. Instead, during issuance of an attestation, the Wallet Unit retrieves any
relevant disclosure policy from the Credential Issuer metadata and stores it
locally. A consequence of this approach is that an Attestation Provider will
revoke an attestation if a relevant embedded disclosure policy must be updated.

##### 6.6.2.8 Batch issuance

Batch issuance means that instead of issuing a single PID or attestation to a
Wallet Unit, a PID Provider or Attestation Provider issues a batch of them. All
PIDs or attestations in a batch have the same attestation type, attribute values
and technical validity period. Apart from that, all of the descriptions in this section
6.6.2 apply regardless of the number of attestations issued (single or batch).

Batch issuance is discussed in more detail in the [Discussion Paper for Topic B](././discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md).
