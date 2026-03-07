---
name: "arf-attestation-mgmt"
description: "Use when implementing attestation presentation to other Wallet Units or intermediaries, attestation management (refresh, status checks), and attestation deletion."
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~6582 -->

#### 6.6.4 PID or attestation presentation to another Wallet Unit

##### 6.6.4.1 Introduction

[Section 6.6.3](#663-pid-or-attestation-presentation-to-a-relying-party) discussed
the trust relationships necessary when a Wallet Unit receives a request from a
Relying Party Instance and presents attributes to that Relying Party Instance.
However, the [European Digital Identity Regulation] requires that a Wallet Unit
is also able to receive such a request from another Wallet Unit, and present
attributes to that requesting Wallet Unit. In this context, the ARF calls the
requesting Wallet Unit the Verifier Wallet Unit, and the presenting Wallet Unit
the Holder Wallet Unit. The User of a Holder Wallet Unit is called a Holder, and
the User of a Verifier Wallet Unit is called a Verifier.

Wallet-to-Wallet interactions cover use cases where a natural person, the
Holder, wishes to present a PID or attestation to another natural person, the
Verifier, where both are using their Wallet Units. As an example, the use case
could occur in a setting where one private person (the Verifier) wants to rent
out their car to another private person (the Holder), provided the Holder has a
valid driving licence.

Note that legal entities are not allowed to bypass the processes and rules
governing Relying Parties, in particular regarding the obligation to register, by
using Wallet-to-Wallet interactions. Therefore,

- **Wallet-to-Wallet interactions will only take place in proximity, not
remotely.** This ensures that both Users are aware of the device they are
connecting to, because they have to present and scan a QR code or NFC tag. Being
in proximity also allows for out-of-band communication and authentication
possibilities between Holder and Verifier.
- **Wallet Units will be restricted in the number of times they can act as a
Verifier per unit of time.** Since many Relying Parties will need to have
frequent interactions with multiple Wallet Units, this ensures that it will not
be feasible for a Relying Party to use a Wallet Unit for all of these
interactions.
- **A User will need to select a dedicated 'Holder Wallet Unit' mode to start
using Wallet-to-Wallet interactions.** If this mode is selected, a Holder Wallet
Unit will clearly indicate to its User that they are presenting attributes to
another natural person, and that they should not proceed if they are in fact
interacting with a legal entity.

For more information and high-level requirements, please refer to
[Technical Specification 9](./technical-specifications/ts9-wallet-to-wallet-interactions.md)
and [Topic 30](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2319-topic-30---interaction-between-wallet-units).
The next section describes a Wallet-to-Wallet transaction flow on a high level.

##### 6.6.4.2 General transaction flow

The following transaction flow will be used as the basis for Wallet-to-Wallet interactions:

1. The two EUDI Wallet Users meet in physical proximity and agree (out of band
of the EUDI Wallet ecosystem), that one (the Holder) should present specific
attributes from a PID or attestation to the other (the Verifier).
2. Both Users select a dedicated 'Wallet-to-Wallet mode' in their respective
Wallet Unit and are asked to specify their role (Holder or Verifier).
3. The Holder Wallet Unit gives the Holder an option to suggest to the Verifier
which PID or attestation, and which attributes, the Verifier should request. This suggestion is called a presentation offer.
4. A handshake protocol (called device engagement in ISO/IEC 18013-5) is
performed and a data connection is established between the two devices as
specified ISO/IEC 18013-5. This protocol also sends the presentation offer to
the Verifier, if the User specified such an offer.
5. The Verifier now must specify to the Verifier Wallet Unit what attributes
should be included in the presentation request:
   - If the Holder specified a presentation offer in step 3, the Verifier Wallet
   Unit displays the offer to the Verifier. The Verifier selects all or a subset
   of the offered attributes, but is not allowed to add additional attributes.
   - If there is no presentation offer in the handshake, the Verifier Wallet
   Unit assists the Verifier in creating a presentation request from scratch, by
   allowing the Verifier to select attributes from a pre-defined list populated
   by the Wallet Provider.
6. The Verifier Wallet Unit sends the presentation request to the Holder Wallet Unit.
7. The Holder Wallet Unit checks if the presentation request matches the
presentation offer created in step 3 (if any), and aborts the transaction in
case the request contains attributes that were not present in the offer. The
Holder Wallet Unit informs the Holder about the reason for aborting. If no
presentation offer was offer was sent in step 4, then this check is omitted.
8. The Holder Wallet Unit prompts the Holder for consent to present the
requested attributes to the Verifier.
9. If the Holder approves the presentation, then a presentation is sent to the
Verifier Wallet Unit.
10. The Verifier Wallet Unit verifies the received presentation in the same way
a Relying Party Instance does, and presents the received attributes to the
Verifier.
11. The Verifier makes a decision relevant to the use case, out of band of the
EUDI Wallet ecosystem, but based (potentially among other factors) on the data
presented by the Holder via their Wallet Units.

Notes:

- Step 2 ensures that both parties actively accept that a local data connection
towards a natural person Wallet Unit should be established. For the Holder this
is very important, because many (if not all) of the verifications usually done on
a presentation request from a Relying Party will not be performed when a Wallet
Unit acts as a Holder Wallet Unit; see the note to step 6 below. For the
Verifier, this is necessary as well, since the functionality offered by a
Verifier Wallet Unit is completely different then when acting a 'normal' Wallet
Unit.
- In step 3, if the Holder wishes to let the Verifier specify the requested
information, the presentation offer is left empty. However, the use of a
presentation offer is recommended, as this increases the chance of success of
the use case.
- Step 4 establishes a local data connection. [ISO/IEC 18013-5] requires that an
mdoc reader(i.e., a Verifier Wallet Unit) must support a QR code and NFC for
device engagement, and BLE and NFC for data retrieval. A Holder Wallet Unit then
chooses to use either a QR code or NFC for device engagement, and either BLE or
NFC for data retrieval. The requirements regarding supported technologies are
therefore more stringent for a Verifier Wallet than for a Holder Wallet Unit.
For the precise requirements, please refer to [ISO/IEC 18013-5]. This may mean
that, depending on the device it's installed on and the technologies chosen by
the Holder, a Wallet Unit may not be able to act as a Verifier. For example, if
a Holder Wallet Unit uses only NFC for device engagement, then a Wallet Unit on
a device that does not have NFC will be not be able to act as a Verifier towards
that Holder Wallet Unit. [Technical Specification 9](./technical-specifications/ts9-wallet-to-wallet-interactions.md)
discusses ways to solve this challenge.
- In step 5, if the offered attributes do not fulfil the needs of the Verifier
for the use case, the Verifier may decide to stop the transaction and return to
step 1 to communicate (out of band) to the Holder which attributes the Holder
should offer.
- In step 5, if there is no presentation offer, the Verifier Wallet Unit will
present the Verifier with a list of 'frequently used' attributes to include in
the presentation request. Conceivably, the Verifier Wallet Unit may limit the
number of attributes in the list by asking the Verifier a set of predefined
questions about the purpose of the use case. However, there is no guarantee that
the Holder Wallet Unit contains these attributes.
- A user-friendly User interface is important in steps 3 and 5 (when Users select what
attributes to offer cq. request).
- In step 6, a presentation request from a Verifier Wallet Unit does not contain
an access certificate (see [Section 6.6.3.2](#6632-wallet-unit-authenticates-the-relying-party-instance))
or a registration certificate (see [Section 6.6.3.3](#6633-wallet-unit-allows-user-to-verify-that-relying-party-does-not-request-more-attributes-than-it-registered)).
The Holder therefore cannot be certain about the Verifier's identity, nor is
there any check regarding the Verifier's reasonable need to request User
attributes. This is because Verifiers are Users and are not required to
register as a Relying Party. Additionally, because there is no access or
registration certificate in the presentation request, the Holder Wallet Unit is
not able to evaluate an embedded disclosure policy, if existing, see [Section 6.6.3.4](#6634-wallet-unit-evaluates-embedded-disclosure-policy-if-present).
- In step 9, the Verifier Wallet Unit verifies the authenticity of the presented
PID or attestation as specified in [Section 6.6.3.6](#6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation).
This implies that the Verifier Wallet Unit needs to obtain the trust anchors of
the relevant PID Provider or Attestation Provider from the respective Trusted
List or LoTE. Additionally, the Verifier Wallet Unit also verifies the revocation status
of the presented PID or attestation as specified in [Section 6.6.3.8](#6637-relying-party-verifies-that-the-pid-or-attestation-is-not-revoked).
- Only steps 2 to 10 are done within the Wallet Units. Steps 1 and 11 allow for
additional actions to be taken and information to be exchanged between Holder
and Verifier out of band.

#### 6.6.5 PID or attestation presentation to an intermediary

[Section 3.11.3](#3113-intermediaries) introduced intermediaries, which are a special category of Relying Party. An intermediary interacts with a Wallet Unit to request User attributes on behalf of another (intermediated) Relying Party. The current section explains the interactions between the intermediated Relying Party, the intermediary, and the Wallet Unit in the course of such an interaction.

1. The intermediary registers once as a Relying Party with a Registrar (see
[Section 3.17](#317-registrars)) and obtains one or more access certificate(s) (see
[Section 3.18](#318-access-certificate-authorities)) bearing its own name and
Relying Party identifier. These access certificates are not different from an
access certificate issued to a 'normal' Relying Party, since an intermediary is,
as a matter of legal fact, a Relying Party. In addition, the intermediary
may receive a registration certificate (see [Section 3.19](#319-providers-of-registration-certificates)),
if the Registrar issues such certificates. However, this registration
certificate will not be used in intermediated transactions.
1. Next, the intermediary separately registers each of the intermediated Relying
Parties that uses its services. This includes registering the attributes the
intermediated Relying Party wants to request for each of its intended uses. Note
that each intermediated Relying Party is registered in the Member State where it
is established. This implies that it is possible for an intermediary to register
an intermediated Relying Party with a Registrar different from the Registrar
where it is registered itself. To prove that the intermediated Relying Party is
indeed using the services of the intermediary, the intermediary provides
evidence to the Registrar, for example a contract. The Registrar evaluates the
evidence, and, if all is correct, registers the fact that the intermediated
Relying Party is using the services of the intermediary. If the Registrar (via a
Provider of registration certificates) issues registration certificates, the
intermediary receives one or more registration certificates for the
intermediated Relying Party. These certificates contain an attribute stating
that the intermediated Relying Party is using the services of the intermediary.
1. When asked by an intermediated Relying Party, the intermediary will request a
presentation of attributes from a Wallet Unit, using one of the flows described
in [Section 4.4](#44-data-presentation-flows). For this, the intermediary will
use their own access certificate (point 1. above) and the registration
certificate of the intermediated Relying Party if available (point 2. above).
The intermediary also adds the following information directly in the
presentation request:
  
    - The user-friendly name and the unique identifier of the intermediated
    Relying Party,
    - The URL of the Registrar of the intermediated Relying Party,
    - The user-friendly description and unique identifier of the intended use of
    the intermediated Relying Party.

   The Wallet Unit displays the name of both the intermediary and the
   intermediated Relying Party to the User when asking for User approval to
   present the requested attributes.
1. If the User has indicated that they want to verify the information registered
about the Relying Party, and the Wallet Unit sees that the Relying Party uses
the services of an intermediary (either in the registration certificate or
because the information about the intermediated Relying Party in the
request is different from the information in the access certificate), it verifies that this Relying Party indeed uses the services of this
intermediary. If the registration certificate is available, it does so by
verifying that the name and the identifier of the intermediary listed in the
registration certificate are identical to the name and identifier in the access
certificate. If no registration certificate is available, the Wallet Unit
contacts the Registrar of the intermediated Relying Party, indicated in the
request, to do this verification online. If this verification was not
successful, or the Wallet Unit was not able to retrieve the information
registered about the Relying Party, the Wallet Unit informs the User.
1. When a Wallet Unit presents a PID or attestation to the intermediary, the
intermediary carries out the verifications described in [Section 6.6.3](#663-pid-or-attestation-presentation-to-a-relying-party), if the intermediary has agreed to do
so with the intermediated Relying Party. This means it may verify the authenticity of the PID or attestation, its revocation
status, device binding (if expected), and User binding, as well as any combined
presentation of attributes, if applicable. Also, the intermediary may need to verify the
authenticity of the Wallet Unit and its revocation status. Note that a Relying
Party is not obliged to carry out all of these verifications. Therefore, the
intermediary and any Relying Party using its services must agree on what
verifications the intermediary will carry out.
1. If these verifications are successful, the intermediary forwards the User
attributes it obtained from the Wallet Unit to the intermediated Relying Party.
There must be an interface between an intermediary and a Relying Party, over
which the intermediated Relying Party can request the intermediary to request
some User attributes from a Wallet Unit and that the intermediary uses to send
back the attribute values presented by the Wallet Unit. However, specifying this
interface or the (security) requirements with which it needs to comply, is out
of scope of the ARF. In particular, it is not required that the User attributes
are end-to-end encrypted between the Wallet Unit and the intermediated Relying
Party, such that an intermediary would not be able to see them.
1. The intermediary deletes any PIDs or attestations it obtained from the Wallet
Unit, including any User attributes, immediately after it has sent the User
attributes to the Relying Party. If the intermediary does not send any User
attributes to the Relying Party, for example because one of the verifications in
the previous step failed, the intermediary deletes the PIDs or attestations
immediately after it has completed all necessary verifications.

Note that this approach implies that an intermediated Relying Party using the
services of an intermediary will not need an access certificate.

For high-level requirements on intermediaries, see [Topic 52](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2330-topic-52-relying-party-intermediaries).

#### 6.6.6 PID or attestation management

##### 6.6.6.1 Overview

Starting from the issuance of a PID or attestation, the PID or attestation is
managed by the User and the PID Provider or Attestation Provider. Management is performed until the PID or attestation is deleted by the User (see [Section 6.6.7](#667-pid-or-attestation-deletion)) or the Wallet Instance is uninstalled by the User (see [Section 6.5](#655-wallet-instance-uninstallation)). Management includes at least the following processes:

1. Re-issuance of a PID or attestation when necessary.
2. Deletion of an unusable PID or attestation, typically after it has been
replaced in a re-issuance process.
3. Revocation a the PID or attestation when necessary.

These processes are discussed in the next subsections.

##### 6.6.6.2 PID or attestation re-issuance

###### 6.6.6.2.1 Introduction

Re-issuance means the replacement of a PID or attestation that already exists in
a Wallet Unit by a PID or attestation having the same attestation type.
Re-issuance is always performed by the same PID Provider or Attestation Provider
that issued the existing PID or attestation, and it is initiated by the Wallet
Unit. The value of the attributes in the new attestation will typically be the
same as in the original attestation. However, this is not required; the PID
Provider or Attestation Provider may change one or more attribute values.
Re-issuance is only applied within the administrative validity period of a
document. As an example, a mobile driving licence (mDL) will typically be issued
in the form of attestations which have a technical validity period shorter than
the administrative validity period of the licence itself. Re-issuance is used
for obtaining fresh attestations as needed during the administrative validity
period, to ensure that the User can always present a valid mDL. When the
administrative validity period ends, there will be an administrative process for
obtaining a new driving licence, which is however out of scope of this document.

Note that, in general, if the original PID or attestation was issued in a batch,
then the PID Provider or Attestation Provider will re-issue that PID or
attestation in a batch as well.

There may be different reasons for re-issuing a PID or attestation, for example:

- The current PID(s) or attestation(s) are near the end of their
 technical validity period, or the Wallet Unit is running out of once-only
 attestations. A short technical validity period or a requirement that an attestation can be presented only once are used to mitigate the risk of Relying Party linkability.
 For more information, see [Section 7.4.3.5](#7435-risks-and-mitigation-measures-related-to-user-privacy).
- The value of one or more of the attributes in the PID or attestation
 has changed.
- The security architecture of the Wallet Solution uses PIDs and/or
 attestations that are issued just-in-time, at the moment that PID or
 attestation is being requested by a Relying Party. This is sometimes
 called synchronous issuing.

These reasons are discussed in the next subsections. Re-issuance is discussed in
more detail in the [Discussion Paper for Topic B](././discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md).

###### 6.6.6.2.2 Re-issuance to limit Relying Party linkability

As specified in [ISO/IEC 18013-5] or [SD-JWT VC], each PID or
attestation contains metadata indicating its technical validity period.
Determining the length of the technical validity period is the responsibility of
the PID Provider or the Attestation Provider. The
technical validity period chosen by the PID Provider or Attestation Provider will
depend on several factors, primarily the security architecture of the
Wallet Solution and the strategy chosen to mitigate Relying Party
linkability, see [Section 7.4.3.5](#7435-risks-and-mitigation-measures-related-to-user-privacy).

Given the above factors, it can generally be assumed that the technical validity
period of a PID or attestations will be much shorter than their lifetime,
meaning the period of time that a User wants to keep that PID or attestation in
their Wallet Unit. That implies that new PIDs and attestations will need to be
re-issued periodically, to replace the ones that are reaching end of their
technical validity.

A similar reason for re-issuing PIDs and attestations occurs when the
PID Provider or Attestation Provider uses once-only attestations (see [Section 7.4.3.5](#7435-risks-and-mitigation-measures-related-to-user-privacy)),
which can be presented only once to a Relying Party. In that case, the Wallet
Unit, or rather the User, will regularly need new PIDs or attestations to avoid
running out.

Re-issuance of PIDs or attestations for these reasons is a purely technical
matter. To the maximum extent possible, the User does not notice that a PID or
attestation has been re-issued, nor do they have to take any action to ensure
that re-issuance happens in time. These conditions are very different from a
first-time issuance of a PID or attestation, where the User must take the
initiative to request the PID or attestation, and is potentially involved in the
process in other ways as well.

This implies, among other, that no User authentication takes place during
re-issuance of an existing PID or attestation. Nevertheless, a Wallet Unit may offer
the User the option to receive a notification of re-issuance.

In the absence of User authentication, and to prevent that a re-issued PID or
attestation ends up at the wrong User, the PID Provider or Attestation Provider
ensures that a re-issued PID or attestation is issued to same Wallet
Unit as the PID or attestation it replaces. This can be done by
the use of device-bound refresh tokens, see [OpenID4VCI].

Finally, since the User is not involved, it is the Wallet Unit itself that triggers the
re-issuance of PIDs and attestations when necessary.

###### 6.6.6.2.3 Re-issuance because of a change of attribute values

During the lifetime of a PID or attestation, the value of some of the attributes
may change. For example, at the date of birth of the User, an age attestation
attribute (i.e., an attribute indicating whether the User has reached a certain
age) may have to be changed from value False to value True. In another example,
the User of a mobile driving licence may have passed the examination for a
different vehicle category. In this case, the PID Provider or Attestation
Provider re-issues the PID or attestation with the correct attribute
values, and revokes the existing attestation.

Re-issuance of a PID or attestation for this reason will have an impact on the
User, because they will notice that their attribute values have been changed.
Therefore, in this case Users will be informed when re-issuance happens.
Additionally, an Attestation Provider may state in their terms of conditions
that re-issuance of an attestation may be used.

###### 6.6.6.2.4 Re-issuance when using synchronous issuing

A third reason for re-issuing a PID or attestation is where the PID Provider or
Attestation Provider uses synchronous issuing in their security architecture. In
such an architecture, the Wallet Unit requests the re-issuance of a new PID or
attestation after it has received a request for that PID or attestation from a
Relying Party. Such a PID or attestation is very short-lived and is used only
once.

The conditions on User awareness and authentication discussed in [Section 6.6.6.2.2](#6662-pid-or-attestation-re-issuance)
are also valid for a synchronous re-issuance process.

##### 6.6.6.3 Deletion of unusable PIDs or attestations

Some time after it is issued, a PID or attestation will become unusable, in the
sense that the User cannot present it any longer to a Relying Party. For
example, a PID or attestation expires, or a once-only PID or attestation (see
[Section 7.4.3.5](#7435-risks-and-mitigation-measures-related-to-user-privacy))
has been presented to a Relying Party already. Typically (but not always), such a PID
or attestation will already have been replaced in a re-issuance process as
described in [Section 6.6.6.2.2](#6662-pid-or-attestation-re-issuance).

Wallet Providers need to decide what to do with unusable PIDs or attestations.
Non-device-bound attestation can be simply deleted, but for PIDs and
device-bound attestations this is more complicated, as the Wallet Provider needs
to manage the associated private keys in the WSCA/WSCD or keystore of the Wallet
Unit. Typically, the amount of storage space available in a WSCA/WSCD or
keystore is limited, and Wallet Providers will want to delete these keys to
prevent an accumulation of unused private keys. Deletion of cryptographic assets
in the WSCA/WSCD in particular is a cryptographic key operation and cannot be
done without User authentication by the WSCA/WSCD; see [Section 6.5.3.3](#6533-wallet-unit-requests-user-to-set-up-two-user-authentication-mechanisms).
At the same time, for usability reasons the User should not be involved in such
'cleaning up' processes, just like the User does not have to take any action for
re-issuance processes ([Section 6.6.6.2.2](#66622-re-issuance-to-limit-relying-party-linkability)).

The recommended solution for this challenge is to ensure that, whenever the
WSCA/WSCD successfully authenticates the User, the Wallet Unit checks if there
are any PIDs or device-bound attestations that cannot be presented any longer to
Relying Parties. The Wallet Unit then requests the WSCA/WSCD to destroy all
cryptographic key material in the WSCA/WSCD related to these PIDs or
attestations. Thus, the Wallet Unit takes advantage of the fact that the User
authenticates for another purpose, for example because they want to present a
PID, to also carry out any necessary key deletion operations. See also [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management)
in Annex 2.

##### 6.6.6.4 PID or attestation revocation

PID or attestation management includes ensuring that PIDs and attestations can
be revoked if necessary. Revocation of PIDs and attestations is discussed in
[Topic 7](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a235-topic-7---attestation-revocation-and-revocation-checking).
The User can request the PID Provider or Attestation Provider to revoke the PID
or attestation at least in case of loss or theft. The PID Provider or
Attestation Provider can also decide itself to revoke a PID or attestation, for example
in case the Wallet Unit on which the PID or attestation is residing is revoked;
see [Section 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit), or for any other valid reason outside the scope of the EUDI Wallet ecosystem.

In addition to revoking a PID or attestation, a PID Provider or Attestation Provider can revoke the certificate that it used for signing the PID or attestation, or any intermediate certificate between that signing certificate and the corresponding trust anchor. In all of these cases, a Relying Party that performs revocation checking will not accept the PID or attestation.

#### 6.6.7 PID or attestation deletion

In case the User no longer wants to retain a specific PID or attestation in
their Wallet Unit, the User can delete it. If the PID Provider or Attestation
Provider issued a batch of multiple PIDs or attestations that have the same
content and are valid, the Wallet Unit deletes them all. Deleting a PID or a
device-bound attestation also means that the WSCA/WSCD or keystore destroys the
cryptographic key material associated with that PID or attestation. Before
deleting critical assets of a PID, the WSCA/WSCD included in the Wallet Unit
will authenticate the User.

If it supports the Digital Credentials API, see [Section 4.4.3](#443-remote-presentation-transaction-flows),
the Wallet Unit also discloses the fact that it no longer contains the PID or
attestation to the Digital Credentials API framework.

For high-level requirements on this topic, see [Topic 51](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2329-topic-51---pid-or-attestation-deletion).
