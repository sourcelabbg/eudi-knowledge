---
name: "arf-wallet-lifecycle-mgmt"
description: "Use when implementing Wallet Unit management and uninstallation. Covers: Wallet Unit revocation, migrating PIDs and attestations to a different Wallet Solution, and Wallet Instance uninstallation."
sections:
  - "6.5.4 Wallet Unit management"
  - "6.5.4.1 Introduction"
  - "6.5.4.2 Wallet Unit revocation"
  - "6.5.4.3 Migrating the PIDs and attestations in a Wallet Unit to a different Wallet Solution"
  - "6.5.5 Wallet Instance uninstallation"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3462 -->

#### 6.5.4 Wallet Unit management

##### 6.5.4.1 Introduction

Starting from Wallet Unit activation and until the Wallet Instance is
uninstalled by the User, a Wallet Unit is managed by the User and the Wallet
Provider. The Wallet Provider is responsible at least to:

- update the Wallet Unit by installing new versions of the Wallet Solution on
the User's device as necessary;
- update the KAs and WIAs in the Wallet Unit as necessary; see [Sections 6.5.3.4][6534-wallet-provider-issues-one-or-more-key-attestations-to-the-wallet-unit] and [6.5.3.5][6535-wallet-provider-issues-one-or-more-wias-to-the-wallet-unit].
- revoke the Wallet Unit when needed; see [Section 6.5.4.2][6542-wallet-unit-revocation].
- ensure that the Wallet Provider cannot access the contents of
the Wallet Unit, in particular to learn the value of any User attestations or
attributes, as well as the contents of the transaction log kept by the Wallet
Unit.
- support procedures for migrating the PIDs and attestations it contains to a different
Wallet Solution. See [Section 6.5.4.3][6543-migrating-the-pids-and-attestations-in-a-wallet-unit-to-a-different-wallet-solution]

To allow Wallet Unit management, the following trust relations are established:

1. When contacting the Wallet Provider, for instance to request the revocation
of the Wallet Unit, the User authenticates the Wallet Provider. This means the
User is sure that they are visiting the website or the User portal of the
genuine Wallet Provider who is responsible for the User's Wallet Unit, and not a
spoofed website or portal. This risk can be partly mitigated by using standard
mechanisms such as TLS server authentication. However, in addition the User will
need to be vigilant as well, just as with any website on the internet.
1. When contacted by a User, the Wallet Provider authenticates the User. This
means that the Wallet Provider is sure that the User is indeed the User that was
associated with the Wallet Unit during activation. For this, the Wallet Provider
uses the authentication methods established in the User's account during
activation, see [Section 6.5.3][653-wallet-unit-activation].
1. When the Wallet Unit and the Wallet Provider set up a communication channel,
the Wallet Unit authenticates the Wallet Provider, meaning that the Wallet Unit
is sure that it is dealing with the genuine Wallet Provider. Similarly, the
Wallet Provider authenticates the Wallet Unit. This means that the Wallet
Provider is sure that the EUDI Wallet Instance is indeed a true instance of
their Wallet Solution, and not a fake app. This will be ensured by the Wallet
Provider. The ARF does not specify how these trust relationships can be
satisfied.
1. When contacted by a PID Provider to request Wallet Unit revocation, the
Wallet Provider authenticates the PID Provider. [Section 6.6.2.2][6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider]
below describes how a Wallet Unit can do this during PID issuance; a Wallet
Provider can use the same mechanism.

For high-level requirements regarding Wallet Instance management, see [Topic 40][topic-40],
section C.

##### 6.5.4.2 Wallet Unit revocation

The Wallet Provider will revoke the Wallet Unit at least in the following circumstances:

- If the User requests the Wallet Provider to revoke the Wallet Unit,
for example in case of loss or theft of the User's device.
- If the Wallet Unit contains a PID, and the PID Provider requests the Wallet
Provider to revoke the Wallet Unit because the natural person using the Wallet
Unit has died. To identify the Wallet Unit that is to be revoked, the PID
Provider uses a Wallet Instance identifier provided by the Wallet Unit in the
WIA during PID issuance; see
[Topic 9][topic-9].
Note: This identifier is the URI and index to the Attestation Status List for WIAs;
see [Topic 7][topic-7].
- If the security of the Wallet Unit is breached or compromised.
- If the Wallet Solution is suspended (optionally) or when it is withdrawn
(mandatorily), see [Section 4.6.3][463-wallet-solution].
- If the Wallet Provider is invalidated by its Member State and (consequently) its status in the Wallet Provider LoTE is changed to Invalid. See [Section 6.2.3][623-wallet-provider-invalidation]

Regarding the detection of a security breach or compromise in an individual
Wallet Unit, the Wallet Provider can use analysis mechanisms that allow
continuous detection of changes in signals relevant to the security posture of
the Wallet Instances it has deployed. These signals are discussed in [Section
6.5.3.2.3][65323-data-collection-for-fraud-or-risk-signal-monitoring]. The
Wallet Provider can potentially use a 4-level security posture framework as
introduced in the table below.

| Level | Posture status | Key indicators & checks | Wallet Provider policy response |
| ----- | -------------- | ----------------------- | ------------------------------- |
| **Level 4** | **Critical** | Confirmed Root/Jailbreak, Active Debugger/Emulator Detected, Private Key Compromised, Critical OS Vulnerability (unpatched) exploited, Wallet Instance integrity check failed (tampering detected), Use of a compromised WSCD-protected private key detected (**see also Note 1**). | Revoke Wallet Instance; revoke corresponding WSCD(s)/keystore(s). Force reinstallation of Wallet Instance on a vulnerability-free device before re-issuing KAs and WIAs. |
| **Level 3** | **High Risk** | High-risk, unpatched OS version detected, Failed biometric attempts exceeding high threshold, Unavailability of a local WSCA/WSCD due to repeated connection error or other errors. | Revoke Wallet Instance; revoke corresponding WSCD(s)/keystore(s). Require step-up authentication (e.g., PIN re-entry), or force re-activation of the Wallet Unit before re-issuing KAs and WIAs. |
| **Level 2** | **Moderate Risk** | Minor integrity checks failed (e.g., non-critical file modification), Wallet Instance running in background with high resource usage, Failed PIN attempts (low threshold). | **Allow use, but limit scope** (e.g., restrict high-value presentations), force User re-authentication after inactivity. |
| **Level 1** | **Low Risk** | Successful device attestation, Wallet Instance integrity check passed, Current OS patch level. | **Full functionality** allowed, including presentation of high-value attestations (PID/QEAA). |

The Wallet Provider revokes a Wallet Unit by setting all indices of WIAs issued to the corresponding Wallet Instance in the relevant status list. In addition, depending on the cause, the Wallet Provider revokes a corresponding WSCD or
keystore(s) by setting all indices of KAs describing that WSCA/WSCD or keystore in the relevant status list:

- If the Wallet Provider must revoke the entire Wallet Unit (for example by
request of the User or a PID Provider, or because there is a security breach of
the Wallet Instance or the OS of the User's device), then the Wallet Provider
revokes the Wallet Instance.
- If there is a security breach of a (type of) WSCD, then the Wallet Provider
revokes that WSCD. If only a single WSCD is breached, the Wallet Provider also revokes the Wallet Instance using it. If a type of WSCD is breached, the Wallet Provider also revokes all Wallet Instances using a WSCD of that type.
- If there is a security breach of a (type of) keystore, then the Wallet Provider revokes that keystore. The Wallet Provider also revokes the Wallet Instance(s) using that (type of) keystore, unless the Wallet Provider creates a risk analysis showing that not revoking these does not lead to unacceptable risks to the User, PID Providers and Attestation
Providers, Relying Parties, or the Wallet Provider itself. If the Wallet
Provider does not revoke the Wallet Instance(s), only the attestations bound to the
revoked (type of) keystore will be impacted. Other functionalities of the Wallet Unit,
including the presentation of a PID, will remain available to the User.

See [Section 4.6.4][464-wallet-unit] for the full state diagram of the Wallet
Unit. See
[Section 6.6.2.5][6625-pid-provider-or-attestation-provider-verifies-that-wallet-unit-is-not-revoked]
and sections referenced there for explanations of how PID Providers, Attestation
Providers, and Relying Parties deal with Wallet Unit revocation. See
[Topic 38][topic-38]
for high-level requirements on Wallet Unit revocation.

##### 6.5.4.3 Migrating the PIDs and attestations in a Wallet Unit to a different Wallet Solution

Article 5a 4 (g) of the [European Digital Identity Regulation] ensures the
User's rights to data portability. Data portability means that a User can
migrate to a different Wallet Solution. The User installs an instance of the new
Wallet Solution, and then wants to restore the PIDs and attestations in their
existing Wallet Unit to their new Wallet Unit. This should be possible with as
minimal an effort as possible, and independent of whether the User still has
access to their existing Wallet Unit.

This section introduces a Migration Object in each Wallet Unit. This object is a
list of PIDs and attestations contained in the Wallet Unit, together with the
information needed to request (re-)issuance of that PID or attestation. In
addition, the Migration Object also contains the transaction log kept by the
Wallet Unit, see [Section 6.6.3.13][66313-wallet-unit-enables-the-user-to-report-suspicious-requests-by-a-relying-party-and-to-request-a-relying-party-to-erase-personal-data].
The Migration Object does not contain any private keys of PIDs or device-bound
attestations. In most security architectures for a Wallet Solution described in
[Section 4.5][45-wscd-architecture-types], this is
impossible at least for PIDs, since the WSCA/WSCD that contains the PID private
keys does not allow their extraction under any circumstances. An exception may
be architectures in which PID private keys are managed in a remote HSM and the
migration is to a new Wallet Unit of the same Wallet Provider. However, in such
cases, restoring functionality of the PIDs in a new Wallet Unit does not
necessitate that private keys are exported to another HSM. Rather, it
implies the User must be able to authenticate towards the existing HSM from the
new Wallet Unit, and be recognised as an existing User. For attestations bound
to a keystore (rather than a WSCA/WSCD), the properties of the keystore
determine if it's possible to export the attestation private keys to a location
of the User's choosing. Most keystores will not allow this.

The fact that the Migration Object does not contain private keys means that PIDs
and device-bound attestations cannot be backed up and restored from the object
in such a way that they are usable in a new Wallet Unit without involvement of
the PID Provider or Attestation Provider. Instead, the User must ask the
respective PID Provider(s) or Attestation Provider(s) to issue the PID(s) or
device-bound attestation(s) existing on the User's old Wallet Unit once again to
the new Wallet Unit. The only function of the Migration Object is to simplify
this process by listing the PIDs and attestations present in the existing Wallet
Unit, together with the information needed by the new Wallet Unit to start the
issuance process. For PIDs and device-bound attestations, the Migration Object
does not contain attribute values or attribute identifiers, as that data is
considered sensitive and is not useful anyway because of the limitations
explained above. Instead, the object contains a list of attestation types and
the related Attestation Providers.

For a non-device-bound attestation, there are no private keys stored in a
WSCA/WSCD or keystore and hence it is in principle possible to back up such an
attestation and restore it in a different Wallet Unit without involvement of the
Attestation Provider. For non-device-bound attestations, the Migration Object
therefore either contains the same data as for device-bound attestations, or it
contains all data including attribute identifiers.

The Migration Object is stored in such a way that its confidentiality is ensured
and that it can be used only by the User.

See [Topic 34][topic-34]
for high-level requirements regarding migration.

The migration functionality of a Wallet Unit also enables backup and restore.
Backup and restore is needed in case the User has lost access to their current
Wallet Unit, for example in case of loss, theft, or breakdown. It is also needed
if the User wants to start using another Wallet Unit, for example because they
have bought a new device, need to factory-reset their existing device, or want
to migrate to another Wallet Solution. In all of these cases, the User wants to
restore the PIDs and attestations in their existing Wallet Unit on their new
Wallet Unit, with as minimal an effort as possible.

The [European Digital Identity Regulation] does not contain a requirement
mandating backup and restore functionality in the Wallet. However, Wallet
Providers will implement backup and restore functionality nevertheless,
because it will be expected by Users. In fact, the requirements in [Topic 34][topic-34]
also ensure the possibility of backup and restore.

---

#### 6.5.5 Wallet Instance uninstallation

No trust relationships are required for Wallet Instance uninstallation; anybody
able to access the device of the User will be able to do this.

If the User uninstalls the Wallet Instance while it still contains PID(s) or attestation(s), the corresponding private keys will remain present in the respective WSCA/WSCD or keystore. This is because deletion of these private keys would require the Wallet Unit to authenticate the User, which is impossible if the Wallet Unit is being deleted by the device OS.

To partly solve this challenge, the Wallet Unit enables the User to 'factory reset' the Wallet Unit, which causes the deletion of all attestations, the log, and all other personal data, settings, and configurations from the Wallet Unit. If the User resets the Wallet Unit, the Wallet Instance request the associated WSCA/WSCD and keystore(s) to delete all cryptographic assets related to the Wallet Unit and to all PIDs and device-bound attestations on the Wallet Unit, if the WSCA/WSCD and keystore(s) are connected to the User device. The User can use this option, for instance, in preparation to the planned uninstallation of the Wallet Instance.

Notes:

- The Wallet Unit does not necessarily inform the Wallet Provider about the factory reset.
- It may happen there is no connection to the WSCA/WSCD or to a keystore at the moment the User resets the Wallet Unit. For instance, in case the WSCA/WSCD is an external smart card and the User does not present that card to the User device. Another example occurs when the WSCA/WSCD is a remote HSM and the User device is offline at that moment. In such cases, the cryptographic assets will  remain present in the WSCA/WSCD or in the keystore, even though they will never be used again. If needed, it is up to the Wallet Provider to define how the Wallet Unit should handle such situations. For example, an HSM manager could address such cases by deciding to delete cryptographic keys in the HSM that are too old or haven't been used for too long, while being aware of the risks in doing so.

If the User resets the Wallet Unit, the Wallet Unit also discloses the fact that it no longer stores any previously disclosed PID(s) or attestation(s) to the [W3C Digital Credentials API] framework.
