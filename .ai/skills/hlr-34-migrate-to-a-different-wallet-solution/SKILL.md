---
name: "hlr-34-migrate-to-a-different-wallet-solution"
description: "Use when working with EUDI high-level requirements for 'Migrate to a different Wallet Solution'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.21 Topic 34 - Migrate to a different Wallet Solution"
  - "A. Back-up requirements <!-- omit from toc -->"
  - "B. Restore Requirements <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~1098 -->

#### A.2.3.21 Topic 34 - Migrate to a different Wallet Solution

##### A. Back-up requirements <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Mig_01 | A Wallet Unit SHALL include and keep up-to-date a Migration Object, containing the following information: - The contents of the log for all transactions executed through the Wallet Unit, as listed in requirement DASH_02. - A list of PIDs and attestations (except Wallet Unit Attestations and Wallet Instance Attestations) present in the Wallet Unit, according to the requirements in this Topic. |
| Mig_02 | The Migration Object SHALL comply with all requirements in [Technical Specification 10](../../technical-specifications/ts10-data-portability-and-download-(export).md). |
| Mig_03 | For each PID or device-bound attestation that is issued to it, a Wallet Unit SHALL add to the Migration Object all data necessary to request issuance of that PID or attestation once again. This SHALL include at least the attestation type and the PID Provider or Attestation Provider that issued the PID or attestation, as well as their service supply points. However, the Migration Object SHALL NOT contain attribute identifiers or attribute values, and SHALL NOT contain any private keys of the PID or device-bound attestation. |
| Mig_03a | For each non-device-bound attestation that is issued to it, a Wallet Unit SHALL add to the Migration Object one of the following: either all data necessary to request issuance of that attestation once again, as listed in Mig_03, or all data necessary to transfer the attestation to a new device without involvement of the Attestation Provider, including attribute identifiers and attribute values. The Wallet Unit SHALL enable the User to indicate if they want to store attribute identifiers and values in the Migration Object. |
| Mig_03b | If the User deletes a PID or attestation from their Wallet Unit, the Wallet Unit SHALL delete the corresponding entry from the Migration Object. |
| Mig_04 | The Wallet Unit SHALL store the Migration Object in an external storage or remote storage location of the User's choice, from among the storage options supported by the Wallet Unit, in such a way that the User can still retrieve the object from a new Wallet Unit in case the existing Wallet Unit becomes unavailable. *Note: a) It is up to the Wallet Provider to decide which external storage options or remote storage locations the Wallet Unit supports for storing the Migration Object. b) The new Wallet Unit may be either an instance of the same Wallet Solution as the old one, or an instance of a different Wallet Solution.* |
| Mig_05 | The Wallet Unit SHALL store the Migration Object in such a way that its confidentiality, integrity, and authenticity is protected and that it is protected against use by others than the User. *Note: This could be done, for example, by using password-based cryptography to encrypt the object.* |

##### B. Restore Requirements <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| Mig_06 | Directly after installation of a new Wallet Instance, the Wallet Instance SHALL enable the User to import a Migration Object from an external storage or remote storage location indicated by the User, from among the storage options supported by the Wallet Unit. |
| Mig_07 | When importing a Migration Object, for each PID and device-bound attestation listed in the Migration Object, the Wallet Unit SHALL enable the User to select that PID or attestation. When a PID or device-bound attestation is selected, the Wallet Unit SHALL request the respective PID Provider or Attestation Provider to re-issue that PID or attestation. If the User selects a PID, the PID SHALL be the first to be restored. |
| Mig_07a | When importing a Migration Object, for each non-device-bound attestation listed in the Migration Object, the Wallet Unit SHALL enable the User to select that attestation. When an attestation is selected, the Wallet Unit SHALL, depending on whether the Migration Object contains attribute identifiers and attribute values (see Mig_03a), either restore the attestation or request the respective Attestation Provider to re-issue it. |
| Mig_07b | When importing a Migration Object, the Wallet Unit SHALL ask the User whether they want to restore the log from the Migration Object. When the User agrees, the Wallet Unit SHALL restore the log, and SHALL append future transactions to this log according to the requirements in [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency). |
| Mig_08 | Empty |
| Mig_09 | Empty |
| Mig_10 | Empty |
| Mig_11 | The processes and interfaces used for issuance of a PID or attestation as part of a migration process SHALL be the same as those used for a 'normal' issuance process, as specified in [Topic 10](./annex-2.02-high-level-requirements-by-topic.md#a237-topic-10---issuing-a-pid-or-attestation-to-a-wallet-unit). |
| Mig_12 | Empty |
| Mig_13 | Empty |
| Mig_14 | Empty |
| Mig_15 | Empty |
| Mig_16 | Empty |
