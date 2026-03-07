---
name: "hlr-11-pseudonyms"
description: "Use when working with EUDI high-level requirements for 'Pseudonyms'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.8 Topic 11 - Pseudonyms"
  - "A. HLRs related to Use Cases A and B <!-- omit from toc -->"
  - "B. HLRs related to Relying Parties <!-- omit from toc -->"
  - "C. HLRs related to privacy <!-- omit from toc -->"
  - "D. HLRs related to interoperability <!-- omit from toc -->"
  - "E. HLRs related to scope rate-limited pseudonyms <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~1900 -->

#### A.2.3.8 Topic 11 - Pseudonyms

##### A. HLRs related to Use Cases A and B <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PA_01 | A Wallet Unit SHALL enable a User to generate a Pseudonym and register it at a Relying Party. *Note: For an attested pseudonym, pseudonym generation takes place by requesting the issuance of a pseudonym attestation. Pseudonym registration takes place by presenting the attestation.* |
| PA_02 | A Wallet Unit SHALL enable a User to authenticate with a Pseudonym towards a Relying Party if the Wallet Unit was used previously to register the Pseudonym for the same Relying Party |
| PA_03 | A Wallet Unit SHALL be able to perform the actions specified in the above two requirements independently of whether the interaction with the Relying Party is initiated on the same device hosting the Wallet Instance or on a device different from the one hosting the Wallet Instance. |
| PA_04 | A Wallet Unit SHALL enable the User to use multiple different Pseudonyms at a given Relying Party, unless it is explicitly designed as a scope rate-limited attestation. |
| PA_05 | A Wallet Unit SHOULD enable a User to freely choose a User alias for each Pseudonym registered at a Relying Party. Setting an alias SHOULD be optional for the User. The User SHOULD be able to change the alias for any Pseudonym. |
| PA_06 | A Wallet Unit SHALL enable a User to choose which Pseudonym to authenticate with towards a Relying Party, if multiple Pseudonyms are registered for this Relying Party. The Wallet Unit SHOULD present the User with the aliases of the applicable Pseudonyms, if assigned, when making this choice. |
| PA_07 | A Wallet Unit SHALL enable a User to delete a Pseudonym. |
| PA_08 | A Wallet Unit SHALL enable the User to manage Pseudonyms within the Wallet Unit in a user-friendly and transparent manner. |
| PA_08a | A Wallet Unit SHALL log Pseudonym registration and presentation transactions as specified in [Topic 19](./annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency). |
| PA_09 | A Wallet Unit SHALL enable the User to see all existing pseudonyms, including the associated Relying Party (if any). |

##### B. HLRs related to Relying Parties <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PA_10 | A Relying Party SHALL be able to verify that a User is registering a Pseudonym using a non-revoked Wallet Unit. |
| PA_11 | A Relying Party SHALL be able to verify that a User is authenticating with a Pseudonym using a non-revoked Wallet Unit. |
| PA_12 | If Wallet Unit is used to register a Pseudonym at a Relying Party in combination with a PID or attestation being presented to the same Relying Party, then this Relying Party SHALL be able to verify that the same User performed both actions. |
| PA_13 | The Relying Party SHALL be able to validate that the pseudonym presented to them belongs to the User presenting it. |

##### C. HLRs related to privacy <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PA_14 | A Wallet Unit SHALL store the information necessary for authenticating with a Pseudonym in either a WSCA/WSCD or in a keystore. |
| PA_15 | A Relying Party SHALL NOT be able to derive the User's true identity, or any data identifying the User, from the Pseudonym value received by the Relying Party. |
| PA_16 | A Wallet Unit SHALL NOT reveal the same Pseudonym to different Relying Parties, unless the User explicitly chooses otherwise. |
| PA_17 | It SHALL NOT be possible to correlate Pseudonyms based on their values nor on other metadata sent by the Wallet Unit during registration and authentication, meaning that colluding Relying Parties SHALL NOT able to conclude that different Pseudonyms belong to the same User. |
| PA_18 | The Wallet Unit SHALL ensure that Pseudonyms contain sufficient entropy to make the chance of colliding Pseudonyms (meaning two Users having the same Pseudonym value for the same Relying Party) negligible. |
| PA_19 | A Wallet Unit SHALL NOT share the User's optionally assigned Pseudonym aliases with any Relying Party. |
| PA_20 | The Wallet Unit SHALL verify the identity of a Relying Party when a User registers a Pseudonym or authenticates with a Pseudonym. If the profile or extension of [W3C WebAuthn] meant in PA_21 does not enable the Wallet Unit to do this, the Wallet Unit SHALL trust the WebAuthn Client (i.e., the browser) to verify the Relying Party identity.  *Note: [W3C WebAuthn] currently does not offer a way for an Authenticator (i.e., the Wallet Unit) to authenticate a Relying Party. Instead, the Client (i.e., the browser) will authenticate the Relying Party, using TLS.* |

##### D. HLRs related to interoperability <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PA_21 | The Commission SHALL create or reference a technical specification containing a profile or extension of the [W3C WebAuthn] specification compliant with the HLRs specified in this Topic. This specification SHALL contain all details necessary for Wallet Units and Relying Parties to generate, register, and use Pseudonyms. |
| PA_22 | Wallet Providers MAY ensure that their Wallet Solution supports the HLRs defined for this topic by letting their Wallet Units perform the role of a WebAuthn authenticator following the [W3C WebAuthn] specification and the technical specification referenced in referenced in PA_21. |

##### E. HLRs related to scope rate-limited pseudonyms <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PA_23 | A protocol enabling scope rate-limited pseudonyms SHALL rely solely on algorithms included in the [ECCG Agreed Cryptographic Mechanisms v2.0](https://certification.enisa.europa.eu/document/download/a845662b-aee0-484e-9191-890c4cfa7aaa_en?filename=ECCG%20Agreed%20Cryptographic%20Mechanisms%20version%202.pdf). |
| PA_24 | A protocol enabling scope rate-limited pseudonyms SHALL enable a Wallet Unit to allow a User to generate a scope rate-limited pseudonym, register this by a Relying Party, and prove that this is within the rate and scope restrictions determined by the Relying Party. |
| PA_25 | A protocol enabling scope rate-limited pseudonyms SHALL allow a Relying Party, when a User presents a scope rate-limited pseudonym, to verify that the rate is not exceeded for this User. |
| PA_26 | A protocol enabling scope rate-limited pseudonyms SHALL allow a Relying Party to choose the scope and rate when requesting a scope rate-limited pseudonym from a User. |
| PA_27 | A protocol enabling scope rate-limited pseudonyms SHALL NOT allow any entity or collusion of entities not including the User, to link scope rate-limited pseudonyms of the same User when used across several different Relying Parties. This SHALL hold even if the scope and rate are identical across the different Relying Parties and both for registration and authentication of the scope rate-limited pseudonym |
| PA_28 | A protocol enabling scope rate-limited pseudonyms SHALL ensure that if the rate is larger than 1, a User's different pseudonyms SHALL be unlinkable for the same scope. This SHALL hold against any entity or collusion of entities, not including the User. Further, such protocol SHALL ensure that during registration or authentication with such a pseudonym, it SHALL NOT be possible for the Relying Party to deduce any information about how many pseudonyms the User has already registered (except that it does not exceed the predetermined rate). |
| PA_29 | A protocol enabling scope rate-limited pseudonyms SHALL ensure that no entity or collusion of entities, not including a User, is able to authenticate or register with a scope rate-limited pseudonym of this User. |
| PA_30 | A Wallet Unit SHALL store cryptographic material necessary for authenticating as a scope rate-limited pseudonyms in either a WSCA/WSCD or in a keystore. |
| PA_31 | A User's scope rate limited pseudonyms for a particular scope and rate SHALL be persistent over time even if they start using another Wallet Unit. |
