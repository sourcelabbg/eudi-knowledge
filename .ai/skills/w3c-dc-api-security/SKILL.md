---
name: "w3c-dc-api-security"
description: "Use when reviewing W3C Digital Credentials API security and privacy. Covers: credential protocol security, cross-device security, quishing, data integrity, XSS/CSRF protection, session security, privacy considerations, and accessibility."
sections:
  - "Security Considerations"
  - "Credential Protocols"
  - "Cross-device Protocols"
  - "Quishing"
  - "Data Integrity"
  - "Authentication"
  - "Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF)"
  - "Session Security"
  - "Privacy Considerations"
  - "Design Considerations and Alternatives"
  - "Spectrum of Privacy"
  - "Exchange Protocol and Credential Format"
  - "Unnecessary Requests for Credentials"
  - "Fingerprinting and Data Leakage"
  - "User Permission and Transparency"
  - "Accessibility Considerations"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~6659 -->

## Security Considerations
      
        
          This section is a work in progress as this document evolves.
        
        
          The documents listed below outline initial security considerations
          for Digital Credentials, both broadly and for presentation on the
          web. Their contents will be integrated into this document gradually.
        
        
          - 
            
            TAG Security and Privacy Considerations Questionnaire (WIP)
          
          - 
            
            Threat Model for Decentralized Identities
          
        
      
      
### Credential Protocols
        
          Explain that while the API provides security at the browser API
          level, that security for the underlying credential issuance or
          presentation protocol is a separate concern and that developers need
          to understand that layer of the stack to get a total picture of the
          protections that are in place during any given transaction.
        
      
      
### Cross-device Protocols
        
          Explain that cross-device issuance or presentation uses a separate
          protocol that has its own security characteristics.
        
      
      
### Quishing
        
          Explain that the API is designed to avoid the problem of quishing
          (phishing via QR Codes) and other QR Code and non-browser API-based
          attacks and to be aware of exposure of QR Codes during digital
          credential interactions.
        
      
      
### Data Integrity
        
          Explain that the API does not provide data integrity on the digital
          credential requests or responses and that responsibility is up to the
          underlying protocol used for the request or response.
        
      
      
### Authentication
        
          Explain that authentication (such as a PIN code to unlock) to a
          particular app, such as a digital wallet, that responds to an API
          request is crucial in high-risk use cases.
        
      
      
### Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF)
        
          Explain what attacks are possible via XSS and CSRF, if any.
        
      
      
### Session Security
        
          Explain that once a secure session is established at a website using
          credentials exchanged over this API, that the subsequent security is
          no longer a function of the credential used or this API and is up to
          the session management utilized on the website.

---

## Privacy Considerations
      
        
          This section is a work in progress as this document evolves.
        
      
      
        The Digital Credentials API integrates into a complex ecosystem with
        multiple technology layers and various participants (including but not
        limited to Verifiers, Holders and Issuers), each of which have to
        consider different aspects of user privacy. This specification does not
        attempt to exhaustively list all considerations for the different
        participants. We would like to refer these parties to a variety of
        other resources that explore the digital credentials threat model more
        holistically:
      
      
        - [[[credential-considerations]]]
        
        - [[[threat-model-decentralized-identities]]]
        
        - 
          VC Data Model
          Privacy Considerations
        
        - ...
        
      
      
        Instead, these considerations focus on the Digital Credentials API
        itself, and describe how user agents can satisfy their user agent duties in an
        implementation of the API, taking into account the relevant privacy
        properties of the ecosystem it interacts with.
      
      
        The privacy considerations for digital credentials are not static. They
        will evolve over time as the ecosystem matures, and may be informed by
        the behavior of other actors in the ecosystem, improvements in other
        layers of the stack, new threats to user privacy, as well as changing
        societal norms and regulations.
      
      
        It is expected that the various groups involved in the design and
        implementation of the Digital Credentials API actively monitor the
        evolving privacy landscape and participate in the corresponding
        evolution of the API.
      
      
### Design Considerations and Alternatives
        
          The Digital Credentials API is designed to mediate requests for
          digital credentials from websites, being agnostic to the credential
          format and the information contained in it, as well as the protocol
          used to exchange it (within the bounds on the protocol registry
          inclusion criteria). This and other key design choices are derived
          from the goal of providing a more secure and private credential
          exchange experience for users than the existing alternatives (e.g.,
          [[custom-schemes]]), that is still compatible with common exchange
          protocols for ease of adoption.
        
        
          The API provides the connection interface between [=verifiers=] and
          [=holders=], i.e. the means by which a [=digital credential/exchange
          protocol|credential exchange protocol=] is initiated and the user
          switches to the [=holder=] application to select a credential.
          Solutions that have been used for this purpose in the past include QR
          codes and custom URL schemes. As documented in
          [[[presenting-credentials-on-the-web]]] and [[[custom-schemes]]],
          those solutions have security, privacy, and accessibility concerns.
        
        
          With adoption of digital credential technology being driven by
          ecosystem demand and regulatory mandates, the Web platform offers an
          alternative to the aforementioned less-desirable technologies that is
          easy to use for developers, is compatible with existing credential
          exchange protocols and, most importantly, has better user privacy,
          security, and accessibility properties than these alternatives.
        
        
          The Digital Credentials API offers the user agent the ability to
          intermediate on behalf of the user (e.g. in the form of a
          [=credential chooser=]) to contextualize requests and prevent immediate exposure to
          holder applications. It also enforces certain minimum
          requirements on supported protocols, such as response encryption.
        
        
          The Digital Credentials API is not intended to inhibit the
          development of other standardized solutions that enhance user
          privacy. For example, an API could be standardized that more strictly
          enforces unlinkability for specific purposes such as age
          verification. Higher-level, designed-for-purpose APIs often enable
          purpose
          limitation, ease of explanation to the user, and privacy and
          security protections from user agents.
        
      
      
### Spectrum of Privacy
        
          The Digital Credentials API serves a variety of use cases with
          different grades of data disclosure and individual users with
          different preferences depending on the context that they are in.
          Notably, the privacy properties of a credential exchange mediated by
          this API could be mandated by the legal and regulatory environment of
          an individual user.
        
        
          This means that some users may not want, or be allowed, to use the
          most privacy-preserving means of exchanging credential information.
          Nonetheless, user agents need to serve users with an experience that
          is private by default and protect them from harm.
        
        
          Because of this spectrum of preferences and use cases, it may be
          difficult for a user agent to discern whether a user means to expose
          their personal information or is being tricked into doing so. It is
          thus the user agent's responsibility to ensure that every user
          understands what data they are sharing and who will participate in
          the exchange of information, before the exchange begins.
        
      
      
### Exchange Protocol and Credential Format
        
          Because the Digital Credentials API sits at the center of an exchange
          that involves multiple independent parties, the exchange protocol and
          credential format used by these parties for exchanging user
          information are crucial to the user agent's goal of protecting user
          privacy.
        
        
          The protocol registry for the Digital Credentials API is designed to
          ensure that, among other requirements, supported protocols facilitate
          specific privacy-enhancing capabilities. Protocols are required to
          undergo privacy review by the W3C's Privacy Working Group.
        
#### Exchange Protocol Considerations for User Privacy
        
##### Selective disclosure
        
          Selective
          disclosure is a fundamental technique for data minimization that
          allows holders to share the minimum required information that is
          requested by a verifier. Protocols are expected to facilitate
          selective disclosure by allowing the verifier to specify the exact
          claims needed.
        
##### Unlinkable presentations
        
          Unlinkability
          is a property that ensures that, if a user presents attributes from a
          credential multiple times, verifiers cannot link these separate
          presentations to conclude they concern the same user
          (verifier-verifier linkability), or that verifiers can not collude
          with issuers to report the exchange of a credential from a wallet to
          the issuer (verifier-issuer linkability). The former is a property
          that can be maintained by the wallet and issuer, e.g. through issuing
          fresh credentials for individual verifiers.
        
        
          While the latter is achievable, e.g. through Zero-Knowledge Proofs,
          design choices of the API such as encrypted responses make it
          impossible for a user agent to prove that verifier-issuer
          unlinkability was achieved in practice. Nonetheless, protocols are
          requested to limit linkability wherever possible.
        
        
          Note that unlinkability is exclusively a consideration for attributes
          that can not be linked to a specific user identity. Inherently
          linkable attributes such as names, driver's license numbers or phone
          numbers do not benefit from unlinkability.
        
        
          Through the Digital Credentials API, the user agent can help
          verifiers and wallets exchange unlinkable attributes, but, because of
          response encryption, it can not guarantee that no linkable
          information is passed between verifiers and wallets. It is
          recommended that user agents account for this fact in their user
          permission experience.
        
        
          Which level of unlinkability is the goal for this API? Can we
          normatively enforce support for any particular unlinkability features
          as part of the protocol registry inclusion criteria?
        
##### "Phone home" mechanisms
        
          "Phoning
          home" refers to scenarios where the presentation or verification
          of a digital credential causes a notification or communication back
          to the issuer or another central entity, which can lead to tracking
          and profiling of individuals.
        
        
          Similar to unlinkability, it is impossible for user agents to ensure
          that an issuer isn't actively involved in the creation or validation
          of credential presentations after a user has given permission to
          proceed with a credential request. From that point on, the wallet
          application owns this decision. While some wallets can be considered
          user agents, it is generally recommended that the user agent
          implementing the Digital Credentials API designs its permission
          experience to prevent exposure of a request to the
          wallet application before user confirmation (keeping in mind
          [considerations for integrating
          multiple cooperating user agents](https://w3c-fedid.github.io/digital-credentials/#multiple-user-agents)).
        
        
          Protocols are required to support mechanisms that allow issuers,
          wallets and verifiers avoid or reduce the dependence on "phone home"
          mechanisms.
        
        
          Which level of unlinkability is the goal for this API? To what degree
          can the spec mandate restrictions to issuer involvement?
        
##### Unlinkable revocation
        
          A common instance of issuer involvement in a credential exchange is
          for credential revocation checks. This is particularly challenging
          when presentations are intended to be verifier-issuer unlinkable.
          When credential presentations are made unlinkable through the use of
          e.g. Zero-Knowledge Proofs, the credential formats used in protocols
          are expected to support offline revocation methods such as Cryptographic
          Accumulators. It is further expected that protocol design and
          specification discourages the involvement of verifiers for the
          purpose of revocation where possible.
        
        
          We should discuss whether unlinkable revocation techniques are
          practical enough to be required normatively.
        
##### Support for user transparency, permission and consent
        
          User understanding and participation are non-negotiable properties of
          a credential exchange. The protocol is expected to help all involved
          parties enable user participation by providing the information vital
          for informed permission and/or consent.
        
##### Support for verifier authorization
        
          Verifier authorization refers to the process by which a verifier
          proves its identity and demonstrates that it is legitimately entitled
          to request specific attributes or credentials. This is particularly
          useful when exchanging sensitive data, such as from government-issued
          credentials. Verifier authorization can limit unnecessary or abusive
          credential requests, and ensure that a verifier's access is
          restricted to the specific credential attributes it registered for.
        
        
          Checking verifier authorization is usually handled by the wallet, but
          user agents could find the presence of such a scheme helpful in
          preventing API abuse and designing a well-informed user permission
          experience.
        
        
          Should we require protocols to include provisions that allow user
          agents to understand verifier authorization?
        
##### Encrypting credential responses
        
          To prevent exposure of user information to other parties in
          "transit", for example browser extensions loaded on verifier pages,
          and to encourage secure storage of user credentials by the verifier,
          protocols are required to support and mandate encrypted responses in
          a credential exchange.
        
        
      
      
### Unnecessary Requests for Credentials
        
          Unnecessary credential requests are a key privacy risk to the entire
          digital credentials ecosystem. They could manifest in different ways
          and from different motivations:
        
        
          - Intentional abuse of the API to learn sensitive information about
          the user for the purpose of fraud, tracking, or sale of the data. For
          example, a site could trick a user into sharing their passport
          information through misleading content. This can lead to identity
          theft and financial loss, and severe loss of control and/or leakage
          of personal information.
          
          - Unnecessary requests for credentials without the explicit intent
          of user harm, such as an online store requesting users to sign up
          with their driver's license instead of generic email & passkey or
          federated credentials. This can lead to exclusion of
          users without the ability or willingness to share such a credential
          with the site, a deterioration of the prompt experience on the web,
          and an increase in the risk of accidental data leakage.
          
          - Requests for an excessive amount of information for valid
          purposes against the principle of data minimization. A common example
          is collection of a user's entire national identity document for age
          verification instead of relying on selective disclosure and age
          predicates.
          
        
        
          One challenge here is determining what constitutes "valid" purposes
          and which requests are therefore "unnecessary", and requires
          participation from all parties involved in the credential exchange.
        
        
          - Ideally, verifiers would self-regulate their requests for
          credentials. However, from a user agent's perspective, verifiers are
          potential attackers, and might not consider the user's best interest
          in their designs. The Digital Credentials API needs to operate from
          an assumption that all verifiers might have incentives that motivate
          unnecessary requests and abuse, and protect users accordingly.
          
          - User agents are responsible for protecting their users against
          dangerous content and permission requests on the Web and could
          intervene on their behalf, proactively rejecting requests or
          requiring pre-authorization. To support this, the Digital Credentials
          API requires credential requests to not be encrypted.
          
          - Issuers and lawmakers might decide to restrict use of
          (particularly government-issued) credentials to specific verifiers
          with purpose attestations. Wallets might be expected to enforce these
          restrictions by law or policy.
          
          - The ultimate decision of whether or not to share their personal
          information lies with the user, which is why the API requires the
          user agent to present a credential picker to the user, and other
          parties might additionally require confirmation or consent.
          
        
        
          For a more detailed exploration of how to determine and address
          unnecessary usage, it makes sense to consider goverment-issued
          credentials and other credentials separately, as they potentially
          differ in the sensitivity of their data and the potential harms from
          misuse as well as legal & regulatory considerations.
        
        
          A key component of risk mitigation and ensuring user control that
          applies to both types of credentials is the user agent's ability to
          inspect the credential request metadata and make decisions or UI
          presentation based on it. The DC API ensures this user agent access
          to the exchange through requirements placed on protocols to transmit
          requests unencrypted and to include relevant information.
        
#### Government-issued credentials
        
          Government-issued
          digital credentials include travel documents, personal licenses,
          proof of welfare and public health programs, vehicle registrations,
          and other documents issued by government authorities, or other
          documents representing this information. These documents are highly
          sensitive, as they can contain permanent, irrevocable, unique
          identifiers that are central to a person's individual identity and
          ability to interact with vital public services.
        
##### Risk of theft and leakage of government credentials
        
          The high value of these credentials to users and attackers means
          there is a significant risk of theft, and significant potential harm
          from leakage to unauthorized third parties. This includes the request
          of government identity for the purpose of tracking and
          personalization.
        
##### Risk of proliferation of requests for government credentials
        
          A major concern with increased availability of government credentials
          online is Jevon's Paradox,
          i.e., the chance of increasing demand for credentials through lower
          friction of access. This effect is not inherently caused by the
          Digital Credentials API, and rather the overall increasing adoption
          of digital credentials across the ecosystem, which, however, would
          likely see additional momentum from user agent implementation of the
          Digital Credentials API. As such, the effect needs to be considered
          by user agents implementing the API, as it might result in harmful
          outcomes for users:
        
        
          - Increased risk of information leakage, and ultimately a less
          trusted user experience on the Web. When a large number of services
          access and store government-issued credentials in an insecure manner
          (i.e. not maintaining encryption or failing to safeguard private
          keys), the chance of data leaks and unauthorized access increases as
          well. Even seemingly non-identifying information like birthdates and
          postal codes, when combined, can statistically identify an
          individual.
          
          - Prompt fatigue and a loss in trust by users when they are
          prompted by a large number of websites to share personal information.
          
          - Increased potential for surveillance and restrictions on
          pseudonymous use of online services. Collusion between verifiers and
          issuers, or other parties, might result in the ability to closely
          monitor a user's activity on the Web and take adverse action against
          this individual. Even when no action is taken, the possibility of
          surveillance alone can cause anxiety, discomfort, and behavioral
          changes such as inhibition and self-censorship, impacting individual
          autonomy and freedom of expression.
          
          - 
            Exclusion
            and discrimination of individuals who cannot, or do not want
            to, provide these credentials, prohibiting them from participation
            in services that would previously not require government-issued
            credentials, such as forums and social media platforms on the Web.
          
        
##### Mitigating unnecessary requests for government credentials
        
          The outlined risks of government-issued digital credentials present a
          challenge that cannot be solved by a single participant in the
          ecosystem, and will require a broader policy discussion within
          individual soverign nations about the risks and benefits of accessing
          online services through real-world credentials.
        
        
          It is desirable that a government that issues digital credentials
          also enact laws and regulations that clearly define how and for what
          purposes those credentials are able to be used. All parties involved
          in the exchange, whether they are legally obliged to do so or not,
          are advised to support any government verifier authentication
          schemes, if they exist. The support for (and integration of) verifier
          authentication schemes such as 
          EUDI access and registration certificates can mitigate risks of
          proliferation of unnecessary credential requests. However, the
          presence of such schemes is not guaranteed, which significantly
          increases the risk in a credential exchange.
        
        
          There are other practical steps that user agents implementing the
          Digital Credentials API can take to reduce risk, increase user
          understanding, and prevent certain types of harm:
        
        
          - Only support protocols that support selective disclosure and
          other techniques of data minimization can reduce the impact and
          likelihood of information leakage, and provide better context to
          users in permission and consent flows.
          
          - Support for protocols that allow unlinkability mechanisms such as
          Zero-Knowledge Proofs can prevent verifier-based surveillance and
          potential discrimination, by hiding the issuer.
          
          - Offering useful context and a clearly understandable permission
          flow will help users make better decisions on whether or not to
          accept a credential exchange, which can reduce the viability of
          exchange requests that are made without a concrete user need.
          
        
        
          It is further critical that user agents design a permission
          experience that accounts for the lack of these mitigations, e.g., the
          exchange of personal information from government credentials without
          any verifier authentication scheme. It is recommended that a higher
          level of friction and clear user messaging that highlights the
          involved risk be applied to these types of exchanges.
        
#### Non-government-issued credentials
        
          Non-government-issued credentials include all other digital
          documents, certificates, and attestations that are not
          government-issued and don't represent government-issued documents.
          This could include proof of employment, (non-government) education
          credentials, or cinema tickets. Notably, their exchange is likely
          less restricted by laws and regulations. While these documents often
          don't exhibit the same risks as government-issued credentials, they
          could also contain identifiable or sensitive information.
        
##### Risk of theft and leakage of non-government credentials
        
          The impact and viability of credential theft and leakage of
          non-government credentials is largely based on the content of each
          individual credential type. In general, it could lead to loss of
          control and exposure of sensitive private information, as well as
          impersonation and data theft, which can increase the likelihood of
          further attacks on the affected individual.
        
##### Risk of proliferation of requests for government credentials
        
          The flexibility and lack of regulation of non-government credentials
          carries potential for abuse for the purpose of cross-site tracking
          and linking identities through long-lived identifiers, such as email
          address or phone number. Verifiers participating in a tracking scheme
          based on digital credentials could create user incentives to accept
          sharing identifier credentials across many sites ("loyalty cards" for
          the Web), without fully understanding the implications on their
          privacy.
        
        
          Even users unwilling to share their information in such a scheme
          could be affected by prompt fatigue and potentially risk exclusion
          from using these services.
        
##### Mitigating unnecessary requests for non-government credentials
        
          For non-government-issued credentials, it is recommended that the
          user agent understand the requested credential format and its privacy
          attributes, and build a risk framework that informs the context that
          is shown to the user, as well as the amount of friction that is
          appropriate for each credential type. Protocols and formats involved
          in the exchange of these credentials are generally expected to
          support features such as selective disclosure and unlinkability, but
          these features might not always be appropriate or necessary in the
          exchange of information, especially when it concerns low-risk
          credentials such as cinema tickets.
        
        
          A user agent that recognizes the type of credential being requested
          is encouraged to customize its permission experience to best suit the
          requested credential and help users understand the consequences of
          sharing it.
        
        
          User agents can not be expected to understand all credential
          requests. A user agent that does not recognize the type of credential
          being requested is advised to significantly increase user friction in
          their permission experience, and very clearly communicate the risks
          of sharing unknown credentials with websites to the user. Note that
          this could require integration between different user agents to apply
          appropriate levels of friction and transparency. For example, a
          browser might delegate knowledge about credential requests to the
          operating system, which might require wallets to register known
          credential types and reject an exchange request for an unknown
          credential type.
        
        
          The need to provide users with appropriate transparency conflicts
          with the desire to enable the ecosystem to develop new credential
          formats without explicit user agent buy-in.
        
        
          Is it a good idea for the group to maintain a registry of request
          types and/or credential
          types?
        
##### Reporting abuse
        
          Consider an interoperable abuse reporting system for verifiers making
          unnecessary and abusive requests.
        
      
      
### Fingerprinting and Data Leakage
#### Browser fingerprinting
        
          While the API ensures that no user data is ever shared without a
          permission prompt, the longevity and uniqueness of real world
          identifiers that are likely to be returned by the Digital Credentials
          API make it a potential target for trackers and fingerprinters.
        
        
          Even with selective disclosure, attackers might combine data from a
          digital credential (such as the user's age, or the credential issuer,
          timestamps, see [[[#leaking-incidental-data]]]) to reidentify and/or
          fingerprint users.
        
        
          This attack might be harder for third-party attackers (such as
          scripts embedded on the verifier's pages, but not actively
          collaborating with them for the purpose of tracking) because response
          encryption is mandatory and responses should be decrypted on the
          verifier's server. The verifier could thus ensure not to reflect back
          decrypted information back to client-side JavaScript. Not all
          verifiers will choose to do so, however.
        
#### Leaking incidental data with credential presentations
        
          To ensure authenticity of a credential, its presentation to verifiers
          generally includes more information than the content the verifier is
          requesting access to. It will usually contain at least a signature of
          the issuer and the wallet, and potentially other metadata.
        
        
          This additional information could be used to reidentify and
          fingerprint users, which is especially relevant when an otherwise
          unlinkable presentation is made.
        
        
          While the Digital Credentials API does not control the content of a
          credential response, user agents can help protect users against this
          type of tracking through clearly highlighting which information
          likely gets shared with the verifier beyond what was requested, and,
          more broadly, by identifying and blocking fingerprinting through the
          API by verifiers.
        
#### Revealing device properties through protocol availability
        
          The Digital Credentials API exposes information about which
          credential exchange protocols are supported by the user agent through
          {{DigitalCredential/userAgentAllowsProtocol()}}. It mitigates browser
          fingerprinting and revealing information about the user's device
          configuration through not customizing its response based on e.g.
          which wallet applications are installed on a user's device. The
          returned information is thus, at best, equivalent to a user agent
          version.
        
#### Avoiding leaks of credential availability
        
          The Digital Credentials API does not enable sites to learn whether a
          credential is available without first going through a user permission flow.
          Revealing the presence of credentials would be a risk to user
          privacy, as the presence of a credential is personal information that
          the user might not have preferred to share with the site, and, in
          combination with other signals, could be used to identify the user
          without their permission. It is also a risk to free expression, as
          websites might increasingly start to demand the presentation of these
          credentials from the user in order to access services, excluding
          individuals who are unwilling to present credentials.
        
      
      
### User Permission and Transparency
        
        
          The Digital Credentials API enables the sharing of highly personal,
          sensitive, and at-risk user information with websites via
          credentials, potentially granting the ability to track users online
          and offline, through permanent, unique, irrevocable, cross-context
          identifiers. It also reveals parts of the user's browsing activity as
          well as their intent to identify to specific websites and/or wallets.
          One crucial responsibility of the user agent in a credential request
          is to gather permission from the user to proceed with the exchange of
          information.
        
        
          Important context details that are needed for a user to make an
          informed decision about proceeding with a credential exchange include
          the following:
        
        
          - The origin of the verifier that requests the credential.
          
          - The information that is being requested, or that would be
          revealed by responding to the request.
          
          - Whether presenting this information will enable tracking.
          
          - Which wallet(s) can be used to fulfill the credential request.
          
          - Which credential would be used to share the requested
          information.
          
        
        
          It is advised that user agents in their implementation ensure that
          the details listed are fully disclosed to the user before an exchange
          of any user-related information occurs.
        
        
          Should these be normative in the spec?
        
        
          Should the API be designed so the site can provide in-context
          explanations?
        
#### Handling multiple credential requests
        
          We need to describe concerns, tradeoffs and possible mitigations of
          handling multiple requests and responses for credential presentation.
        
#### Integrating Multiple User Agents
        
          Depending on the technical architecture of a user's system, it is
          likely that the definition of a "user agent" will include multiple
          cooperating layers of the software stack, such as a browser and the
          operating system. The greatest priority for these layers has to be a
          safe and well-informed user permission experience. As such,
          integration can be vital for user safety. Some layers may hold
          information that is inaccessible by other layers, such as the
          availability of a user's credentials. Overprompting or prompting
          without sufficient context could lead to (exploitable) confusion and
          prompt blindness.
        
        
          For this reason, user agents prompting for permission are encouraged
          to integrate software layers for an ideal user experience, if they
          consider it safe to do so. This could happen, for example, if a
          browser trusts the API contract of an operating system to show an
          appropriate prompt, and thus does not show a prompt itself.
        
#### Permission Prior to Wallet Selection
        
          As part of the user permission flow, the user agent needs to ensure
          that users retain the power to choose whether to forward a credential
          request to a wallet, and which wallet to select. This is due to the
          information disclosure that happens as part of the request, and the
          ability of wallets to retain or share this information at the time of
          the request.
        
#### Permission vs. Consent
        
          The permission mediated by the user agent is not consent, which has
          specific legal definitions which can vary among different legal and
          regulatory environments and may need to be collected by the digital
          wallet before sharing information with the verifier, or by the
          verifier itself before initiating the request. With frameworks and
          regulations for obtaining consent still being developed, this API
          aims to enable the exchange of the necessary information, which could
          include the following:
        
        
          - The privacy policy of the verifier receiving the credential.
          
          - The purpose for which the verifier is requesting the information.
          
          - What the information will be used for.
          
          - How the information will be shared or retained.
          
          - Any evaluations and attestations of this information, if
          available.
          
          - Assertions of the verifier's legimitacy and registration for
          accessing the credential, such as 
            EUDI access and registration certificates.
          
        
        
          As more of this information becomes available in a structured format,
          we expect user agents and this specification to leverage it to
          improve the user permission experience as well.

---

## Accessibility Considerations
      
        This section is a work in progress as this document evolves.
