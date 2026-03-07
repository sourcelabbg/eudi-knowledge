---
name: "oid4vp-authorization-request"
description: "Use when constructing or validating an OpenID4VP authorization request. Covers: request parameters (presentation_definition, dcql_query, nonce, response_type, response_mode, response_uri, client_id), client_id prefixes (pre-registered, redirect_uri, did, verifier_attestation, x509_san_dns, x509_san_uri), request_uri with GET and POST methods, JAR (RFC9101), Verifier Info and Proof of Possession."
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~9100(LARGE) -->

## 4. Scope
OpenID for Verifiable Presentations extends existing OAuth 2.0 mechanisms in the following ways:Â¶

A new query language, the Digital Credentials Query Language (DCQL), is defined to enable requesting Presentations in an easier and more flexible way. See Section 6 for more details.Â¶

        A new dcql_query Authorization Request parameter is defined to request Presentation of Credentials in the JSON-encoded DCQL format. See Section 5 for more details.Â¶

        A new vp_token response parameter is defined to return Presentations with or without Holder Binding to the Verifier in either Authorization or Token Response depending on the Response Type. See Section 8 for more details.Â¶

        New Response Types vp_token and vp_token id_token are defined to request Credentials to be returned in the Authorization Response (standalone or along with a Self-Issued ID Token [SIOPv2]). See Section 8 for more details.Â¶

        A new OAuth 2.0 Response Mode direct_post is defined to support sending the response across devices, or when the size of the response exceeds the redirect URL character size limitation. See Section 8.2 for more details.Â¶

        The format parameter is used throughout the protocol in order to enable customization according to the specific needs of a particular Credential format. Examples in Appendix B are given for Credential formats as specified in [VC_DATA], [ISO.18013-5], and [I-D.ietf-oauth-sd-jwt-vc].Â¶

        The concept of a Client Identifier Prefix to enable deployments of this specification to use different mechanisms to obtain and validate metadata of the Verifier beyond the scope of [RFC6749].Â¶

        A mechanism specifying the use of OpenID4VP with the Digital Credentials API (see Appendix A).Â¶

      
Presentation of Credentials using OpenID for Verifiable Presentations can be combined with the End-User authentication using [SIOPv2], and the issuance of OAuth 2.0 Access Tokens.Â¶

---

## 5. Authorization Request
The Authorization Request follows the definition given in [RFC6749] taking into account the recommendations given in [RFC9700] where applicable.Â¶
The Verifier MAY send an Authorization Request as a Request Object either by value or by reference, as defined in the JWT-Secured Authorization Request (JAR) [RFC9101]. Verifiers MUST include the typ Header Parameter in Request Objects with the value oauth-authz-req+jwt, as defined in [RFC9101]. Wallets MUST NOT process Request Objects where the typ Header Parameter is not present or does not have the value oauth-authz-req+jwt.Â¶
The client_id claim is required as defined below and would be redundant with a possible iss claim in the Request Object which is commonly used in JAR. To avoid breaking existing JAR implementations, the iss claim MAY be present in the Request Object. However, if it is present, the Wallet MUST ignore it.Â¶
This specification defines a new mechanism for the cases when the Wallet wants to provide to the Verifier details about its technical capabilities to
allow the Verifier to generate a request that matches the technical capabilities of that Wallet.
To enable this, the Authorization Request can contain a request_uri_method parameter with the value post
that signals to the Wallet that it can make an HTTP POST request to the Verifier's request_uri
endpoint with information about its capabilities as defined in Section 5.10. The Wallet MAY continue with JAR
when it receives request_uri_method parameter with the value post but does not support this feature.Â¶
The Verifier articulates requirements of the Credential(s) that are requested using the dcql_query parameter. Wallet implementations MUST process the DCQL query and select candidate Credential(s) using the evaluation process described in Section 6.4Â¶
The Verifier communicates a Client Identifier Prefix that indicates how the Wallet is supposed to interpret the Client Identifier and associated data in the process of Client identification, authentication, and authorization as a prefix in the client_id parameter. This enables deployments of this specification to use different mechanisms to obtain and validate Client metadata beyond the scope of [RFC6749]. A certain Client Identifier Prefix sets the requirements whether the Verifier needs to sign the Authorization Request as a means of authentication and/or pass additional parameters and require the Wallet to process them.Â¶
Depending on the Client Identifier Prefix, the Verifier can communicate a JSON object with its metadata using the client_metadata parameter which contains name/value pairs.Â¶
Additional request parameters, other than those defined in this section, MAY be defined and used, as described in [RFC6749].
The Wallet MUST ignore any unrecognized parameters, other than the transaction_data parameter.
One exception to this rule is the transaction_data parameter. Wallets that do not support this parameter MUST reject requests that contain it.Â¶


### 5.1. New Parameters
This specification defines the following new request parameters:Â¶

          
dcql_query:
          
            A JSON object containing a DCQL query as defined in Section 6.Â¶
Either a dcql_query or a scope parameter representing a DCQL Query MUST be present in the Authorization Request, but not both.Â¶
In the context of an authorization request according to [RFC6749], parameters containing objects are transferred as JSON-serialized strings (using the application/x-www-form-urlencoded format as usual for request parameters).Â¶

          

client_metadata:
          
            OPTIONAL. A JSON object containing the Verifier metadata values. It MUST be UTF-8 encoded. The following metadata parameters MAY be used:Â¶


                jwks: OPTIONAL. A JSON Web Key Set, as defined in [RFC7591], that contains one or more public keys, such as those used by the Wallet as an input to a key agreement that may be used for encryption of the Authorization Response (see Section 8.3), or where the Wallet will require the public key of the Verifier to generate a Verifiable Presentation. This allows the Verifier to pass ephemeral keys specific to this Authorization Request. Public keys included in this parameter MUST NOT be used to verify the signature of signed Authorization Requests. Each JWK in the set MUST have a kid (Key ID) parameter that uniquely identifies the key within the context of the request.Â¶

              
                encrypted_response_enc_values_supported: OPTIONAL. Non-empty array of strings, where each string is a JWE [RFC7516] enc algorithm that can be used as the content encryption algorithm for encrypting the Response. When a response_mode requiring encryption of the Response (such as dc_api.jwt or direct_post.jwt) is specified, this MUST be present for anything other than the default single value of A128GCM. Otherwise, this SHOULD be absent.Â¶

              
                vp_formats_supported: REQUIRED when not available to the Wallet via another mechanism. As defined in Section 11.1.Â¶

            
Authoritative data the Wallet is able to obtain about the Client from other sources, for example those from an OpenID Federation Entity Statement, take precedence over the values passed in client_metadata.Â¶
Other metadata parameters MUST be ignored unless a profile of this specification explicitly defines them as usable in the client_metadata parameter.Â¶

          

request_uri_method:
          
            OPTIONAL. A string determining the HTTP method to be used when the request_uri parameter is included in the same request. Two case-sensitive valid values are defined in this specification: get and post. If request_uri_method value is get, the Wallet MUST send the request to retrieve the Request Object using the HTTP GET method, i.e., as defined in [RFC9101]. If request_uri_method value is post, a supporting Wallet MUST send the request using the HTTP POST method as detailed in Section 5.10. If the request_uri_method parameter is not present, the Wallet MUST process the request_uri parameter as defined in [RFC9101]. Wallets not supporting the post method will send a GET request to the Request URI (default behavior as defined in [RFC9101]). request_uri_method parameter MUST NOT be present if a request_uri parameter is not present.Â¶
If the Verifier set the request_uri_method parameter value to post and there is no other means to convey its capabilities to the Wallet, it SHOULD add the client_metadata parameter to the Authorization Request.
This enables the Wallet to assess the Verifier's capabilities, allowing it to transmit only the relevant capabilities through the wallet_metadata parameter in the Request URI POST request.Â¶

          

transaction_data:
          
            OPTIONAL. Non-empty array of strings, where each string is a base64url-encoded JSON object that contains a typed parameter set with details about the transaction that the Verifier is requesting the End-User to authorize. See Section 8.4 for details. The Wallet MUST return an error if a request contains even one unrecognized transaction data type or transaction data not conforming to the respective type definition. In addition to the parameters determined by the type of transaction data, each transaction_data object consists of the following parameters defined by this specification:Â¶


                type: REQUIRED. String that identifies the type of transaction data. This value determines parameters that can be included in the transaction_data object. The specific values are out of scope for this specification. It is RECOMMENDED to use collision-resistant names for type values.Â¶

              
                credential_ids: REQUIRED. Non-empty array of strings each referencing a Credential requested by the Verifier that can be used to authorize this transaction. The string matches the id field in the DCQL Credential Query. If there is more than one element in the array, the Wallet MUST use only one of the referenced Credentials for transaction authorization.Â¶

            
Each document specifying details of a transaction data type defines what Credential(s) can be used to authorize those transactions. Those Credential(s) can be issued specifically for the transaction authorization use case or re-use existing Credential(s) used for user identification. A mechanism for Credential Issuers to express that a particular Credential can be used for authorization of transaction data is out of scope for this specification.Â¶
The following is a non-normative example of a transaction data content, after base64url decoding one of the strings in the transaction_data parameter:Â¶

```
{
  "type": "example_type",
  "credential_ids": [ "id_card_credential" ],
  // other transaction data type specific parameters
}

```Â¶


          

verifier_info:
          
            OPTIONAL. A non-empty array of attestations about the Verifier relevant to the Credential Request. These attestations MAY include Verifier metadata, policies, trust status, or authorizations. Attestations are intended to support authorization decisions, inform Wallet policy enforcement, or enrich the End-User consent dialog. Each object has the following structure:Â¶


                format: REQUIRED. A string that identifies the format of the attestation and how it is encoded. Ecosystems SHOULD use collision-resistant identifiers. Further processing of the attestation is determined by the type of the attestation, which is specified in a format-specific way.Â¶

              
                data: REQUIRED. An object or string containing an attestation (e.g. a JWT). The payload structure is defined on a per format level. It is at the discretion of the Wallet whether it uses the information from verifier_info. Factors that influence such Wallet's decision include, but are not limited to, trust framework the Wallet supports, specific policies defined by the Issuers or ecosystem, and profiles of this specification. If the Wallet uses information from verifier_info, the Wallet MUST validate the signature and ensure binding.Â¶

              
                credential_ids: OPTIONAL. A non-empty array of strings each referencing a Credential requested by the Verifier for which the attestation is relevant. Each string matches the id field in a DCQL Credential Query. If omitted, the attestation is relevant to all requested Credentials.Â¶

            
See Section 5.11 for more details.Â¶
The following is a non-normative example of an attested object:Â¶

```
{
  "format": "jwt",
  "data": "eyJhbGciOiJFUzI1...EF0RBtvPClL71TWHlIQ",
  "credential_ids": [ "id_card" ]
}

```Â¶


        


### 5.2. Existing Parameters
The following additional considerations are given for pre-existing Authorization Request parameters:Â¶

          
nonce:
          REQUIRED. A case-sensitive String representing a value to securely bind Verifiable Presentation(s) provided by the Wallet to the particular transaction. The Verifier MUST create a fresh, cryptographically random number with sufficient entropy for every Authorization Request, store it with its current session, and pass it in the nonce Authorization Request Parameter to the Wallet. See Section 14.1 for details. Values MUST only contain ASCII URL safe characters (uppercase and lowercase letters, decimal digits, hyphen, period, underscore, and tilde).Â¶

          

scope:
          OPTIONAL. Defined in [RFC6749]. The Wallet MAY allow Verifiers to request Presentations by utilizing a pre-defined scope value. See Section 5.5 for more details.Â¶

          

response_mode:
          REQUIRED. Defined in [OAuth.Responses]. This parameter can be used (through the new Response Mode direct_post) to ask the Wallet to send the response to the Verifier via an HTTPS connection (see Section 8.2 for more details). It can also be used to request that the resulting response be encrypted (see Section 8.3 for more details).Â¶

          

client_id:
          REQUIRED. Defined in [RFC6749]. This specification defines additional requirements to enable the use of Client Identifier Prefixes as described in Section 5.9. The Client Identifier can be created by parties other than the Wallet and it is considered unique within the context of the Wallet when used in combination with the Client Identifier Prefix.Â¶

          

state:
          REQUIRED under the conditions defined in Section 5.3. Otherwise, state is OPTIONAL. state values MUST only contain ASCII URL safe characters (uppercase and lowercase letters, decimal digits, hyphen, period, underscore, and tilde).Â¶

        


### 5.3. Requesting Presentations without Holder Binding Proofs
The primary use case of this specification is to request and present Verifiable
Presentations, i.e., Presentations that contain a cryptographic Holder Binding proof.Â¶
However, there are use cases where the Verifier wants to request presentation of
Credentials without a proof of cryptographic Holder Binding. Examples for such use cases include
low-security Credentials that do not support Holder Binding (e.g., a cinema
ticket), Credentials that are bound to a biometric trait, or Credentials that
are bound to claims (e.g., a diploma). In some cases, Credentials may support
Holder Binding, but the Verifier may not require it for the Presentation.Â¶
A Verifier that requests and accepts a Presentation of a Credential without a
proof of Holder Binding accepts that the presented Credential may have been
replayed. Section 14.1 contains additional considerations for this case.Â¶
To request a Credential without proof of Holder Binding, the Verifier uses the require_cryptographic_holder_binding parameter in the DCQL request as defined in Section 6 and
Appendix B.Â¶
In this protocol, the nonce parameter serves to securely link the request and
response and as a replay protection in the Holder Binding proof. Without the key
binding proof, nonce is not returned in the response. To maintain the binding
between request and response, the Verifier MUSTÂ¶

include a state parameter as defined in Section 4.1.1 of [RFC6749] in the
Authorization Request,Â¶

          ensure that the value is a cryptographically strong pseudo-random number with
at least 128 bits of entropy,Â¶

          ensure that the value is chosen fresh for each Authorization Request,Â¶

          store it in the Verifier's session state, andÂ¶

          check that the same state value is returned in the Authorization Response,Â¶

        
if at least one Presentation without Holder Binding is requested and unless the
Digital Credentials API is used. The Digital Credentials API uses internal
mechanisms to maintain the binding.Â¶
When using Response Mode direct_post, also see
Section 14.3.Â¶


### 5.4. Examples
The Verifier MAY send an Authorization Request using either of these 3 options:Â¶

Passing as URL with encoded parametersÂ¶

          Passing a request object as valueÂ¶

          Passing a request object by referenceÂ¶

        
The second and third options are defined in the JWT-Secured Authorization Request (JAR) [RFC9101].Â¶
The following is a non-normative example of an Authorization Request with URL-encoded parameters:Â¶

```
GET /authorize?
  response_type=vp_token
  &client_id=redirect_uri%3Ahttps%3A%2F%2Fclient.example.org%2Fcb
  &redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
  &dcql_query=...
  &transaction_data=...
  &nonce=n-0S6_WzA2Mj HTTP/1.1

```Â¶

The following is a non-normative example of an Authorization Request with a Request Object passed by value:Â¶

```
GET /authorize?
  client_id=redirect_uri%3Ahttps%3A%2F%2Fclient.example.org%2Fcb
  &request=eyJrd...

```Â¶

Where the contents of the request query parameter consist of a base64url-encoded and signed (in the example with RS256 algorithm) Request Object. The decoded payload is:Â¶

```
{
  "iss": "redirect_uri:https://client.example.org/cb",
  "aud": "https://self-issued.me/v2",
  "response_type": "vp_token",
  "client_id": "redirect_uri:https://client.example.org/cb",
  "redirect_uri": "https//client.example.org/cb",
  "dcql_query": {
    "credentials": [
      {
        "id": "some_identity_credential",
        "format": "dc+sd-jwt",
        "meta": {
          "vct_values": [ "https://credentials.example.com/identity_credential" ]
        },
        "claims": [
            {"path": ["last_name"]},
            {"path": ["first_name"]}
        ]
      }
    ]
  },
  "nonce": "n-0S6_WzA2Mj"
}

```Â¶

The following is a non-normative example of an Authorization Request with a request object passed by reference:Â¶

```
GET /authorize?
  client_id=x509_san_dns%3Aclient.example.org
  &request_uri=https%3A%2F%2Fclient.example.org%2Frequest%2Fvapof4ql2i7m41m68uep
  &request_uri_method=post HTTP/1.1

```Â¶

To retrieve the actual request, the Wallet might send the following non-normative example HTTP request to the request_uri:Â¶

```
POST /request/vapof4ql2i7m41m68uep HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

wallet_metadata=%7B%22vp_formats_supported%22%3A%7B%22dc%2Bsd-jwt%22%3A%7B%22sd-jwt_alg
_values%22%3A%20%5B%22ES256%22%5D%2C%22kb-jwt_alg_values%22%3A%20%5B%22ES256%22%5D%7D%7
D%7D&
wallet_nonce=qPmxiNFCR3QTm19POc8u

```Â¶


### 5.5. Using scope Parameter to Request Presentations
Wallets MAY support requesting Presentations using OAuth 2.0 scope values.Â¶
Such a scope parameter value MUST be an alias for a well-defined DCQL query. Since multiple scope values can be used at the same time, the identifiers for Credentials (see Section 6.1) and claims (see Section 6.3) within the DCQL queries associated with scope values MUST be unique. This ensures that there are no collisions between the identifiers used in the DCQL queries and that the Verifier can unambiguously identify the requested Credentials in the response.Â¶
The specific scope values, and the mapping between a certain scope value and the respective
DCQL query, are out of scope of this specification.Â¶
Possible options include normative text in a separate specification defining scope values along with a description of their
semantics or machine-readable definitions in the Wallet's server metadata, mapping a scope value to an equivalent
DCQL request.Â¶
It is RECOMMENDED to use collision-resistant scopes values.Â¶
The following is a non-normative example of an Authorization Request using the example scope value com.example.IDCardCredential_presentation:Â¶

```
GET /authorize?
  response_type=vp_token
  &client_id=https%3A%2F%2Fclient.example.org%2Fcb
  &redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
  &scope=com.example.healthCardCredential_presentation
  &nonce=n-0S6_WzA2Mj HTTP/1.1

```Â¶


### 5.6. Response Type vp_token
This specification defines the Response Type vp_token.Â¶

          
vp_token:
          When supplied as the response_type parameter in an Authorization Request, a successful response MUST include the vp_token parameter. The Wallet SHOULD NOT return an OAuth 2.0 Authorization Code, Access Token, or Access Token Type in a successful response to the grant request. The default Response Mode for this Response Type is fragment, i.e., the Authorization Response parameters are encoded in the fragment added to the redirect_uri when redirecting back to the Verifier. The Response Type vp_token can be used with other Response Modes as defined in [OAuth.Responses]. Both successful and error responses SHOULD be returned using the supplied Response Mode, or if none is supplied, using the default Response Mode.Â¶

        

See Section 8 on how the response_type value determines the response used to return a VP Token.Â¶


### 5.7. Passing Authorization Request Across Devices
There are use-cases when the Authorization Request is being displayed on a device different from a device on which the requested Credential is stored. In those cases, an Authorization Request can be passed across devices by being rendered as a QR Code.Â¶
The usage of the Response Mode direct_post (see Section 8.2) in conjunction with request_uri is RECOMMENDED, since Authorization Request size might be large and might not fit in a QR code.Â¶


### 5.8. aud of a Request Object
When the Verifier is sending a Request Object as defined in [RFC9101], the aud claim value depends on whether the recipient of the request can be identified by the Verifier or not:Â¶

the aud claim MUST be equal to the iss (issuer) claim value, when Dynamic Discovery is performed.Â¶

          the aud claim MUST be "https://self-issued.me/v2", when Static Discovery metadata is used.Â¶

        
Note: "https://self-issued.me/v2" is a symbolic string and can be used as an aud claim value even when this specification is used standalone, without SIOPv2.Â¶


### 5.9. Client Identifier Prefix and Verifier Metadata Management
This specification defines the concept of a Client Identifier Prefix that dictates how the Wallet needs to interpret the Client Identifier and associated data in the process of Client identification, authentication, and authorization.
The Client Identifier Prefix enables deployments of this specification to use different mechanisms to obtain and validate metadata of the Verifier beyond the scope of [RFC6749]. The term Client Identifier Prefix is used since the Verifier is acting as an OAuth 2.0 Client.Â¶
The Client Identifier Prefix is a string that MAY be communicated by the Verifier in a prefix within the client_id parameter in the Authorization Request. A fallback to pre-registered Clients as in [RFC6749] remains in place as a default mechanism in case no Client Identifier Prefix was provided. A certain Client Identifier Prefix may require the Verifier to sign the Authorization Request as a means of authentication and/or pass additional parameters and require the Wallet to process them.Â¶


#### 5.9.1. Syntax
In the client_id Authorization Request parameter and other places where the Client Identifier is used, the Client Identifier Prefixes are prefixed to the usual Client Identifier, separated by a : (colon) character:Â¶

```
<client_id_prefix>:<orig_client_id>

```Â¶

Here, <client_id_prefix> is the Client Identifier Prefix and <orig_client_id> is an identifier for the Client within the namespace of that prefix. See Section 5.9.3 for Client Identifier Prefixes defined by this specification.Â¶
Wallets MUST use the presence of a : (colon) character and the content preceding it to determine whether a Client Identifier Prefix is used. If a : character is present and the content preceding it is a recognized and supported Client Identifier Prefix value, the Wallet MUST interpret the Client Identifier according to the given Client Identifier Prefix. The Client Identifier Prefix is defined as the string before the (first) : character. Note that implementations should not assume that the presence of a : character implies that the entire value can be processed as a valid URI. Instead, the specific processing rules defined for the specified Client Identifier Prefix (see Section 5.9.3) should be used to parse the client_id value.Â¶
For example, an Authorization Request might contain client_id=verifier_attestation:example-client to indicate that the verifier_attestation Client Identifier Prefix is to be used and that within this prefix, the Verifier can be identified by the string example-client. The presentation would contain the full verifier_attestation:example-client string as the audience (intended receiver) and the same full string would be used as the Client Identifier anywhere in the OAuth flow.Â¶
Note that the Verifier needs to determine which Client Identifier Prefixes the Wallet supports prior to sending the Authorization Request in order to choose a supported prefix.Â¶
Depending on the Client Identifier Prefix, the Verifier can communicate a JSON object with its metadata using the client_metadata parameter which contains name/value pairs.Â¶


#### 5.9.2. Fallback
If a : character is not present in the Client Identifier, the Wallet MUST treat the Client Identifier as referencing a pre-registered client. This is equivalent to the [RFC6749] default behavior, i.e., the Client Identifier needs to be known to the Wallet in advance of the Authorization Request. The Verifier metadata is obtained using [RFC7591] or through out-of-band mechanisms.Â¶
For example, if an Authorization Request contains client_id=example-client, the Wallet would interpret the Client Identifier as referring to a pre-registered client.Â¶
If a : character is present in the Client Identifier but the value preceding it is not a recognized and supported Client Identifier Prefix value, the Wallet can treat the Client Identifier as referring to a pre-registered client or it may refuse the request.Â¶
From this definition, it follows that pre-registered clients MUST NOT contain a : character preceded immediately by a supported Client Identifier Prefix value in the first part of their Client Identifier.Â¶


#### 5.9.3. Defined Client Identifier Prefixes
This specification defines the following Client Identifier Prefixes, followed by the examples where applicable.Â¶
In case of using OpenID4VP over DC API, as defined in Appendix A, it is at the discretion of the Wallet whether it validates the signature on the Request Object following the processing rules defined by a relevant Client Identifier Prefix. Factors that influence the Wallet's decision include, but are not limited to, the trust framework the Wallet supports, the specific policies defined by the Issuers or ecosystem, and profiles of this specification.Â¶


              redirect_uri: This prefix value indicates that the original Client Identifier part (without the prefix redirect_uri:) is the Verifier's Redirect URI (or Response URI when Response Mode direct_post is used). The Verifier MAY omit the redirect_uri Authorization Request parameter (or response_uri when Response Mode direct_post is used). All Verifier metadata parameters MUST be passed using the client_metadata parameter defined in Section 5.1. An example Client Identifier value is redirect_uri:https://client.example.org/cb. Requests using the redirect_uri Client Identifier Prefix cannot be signed because there is no method for the Wallet to obtain a trusted key for verification. Therefore, implementations requiring signed requests cannot use the redirect_uri Client Identifier Prefix.Â¶
The following is a non-normative example of an unsigned request with the redirect_uri Client Identifier Prefix:Â¶

```
HTTP/1.1 302 Found
Location: https://wallet.example.org/universal-link?
  response_type=vp_token
  &client_id=redirect_uri%3Ahttps%3A%2F%2Fclient.example.org%2Fcb
  &redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
  &dcql_query=...
  &nonce=n-0S6_WzA2Mj
  &client_metadata=%7B%22vp_formats_supported%22%3A%7B%22dc%2Bsd-jwt%22%3A%7B%22sd-jwt_
  alg_values%22%3A%20%5B%22ES256%22%5D%2C%22kb-jwt_alg_values%22%3A%20%5B%22ES256%22%5D
  %7D%7D%7D

```Â¶


            
              openid_federation: This prefix value indicates that the original Client Identifier (the part without the prefix openid_federation:) is an Entity Identifier defined in OpenID Federation [OpenID.Federation]. Processing rules given in [OpenID.Federation] MUST be followed. The Authorization Request MAY also contain a trust_chain parameter. The final Verifier metadata is obtained from the Trust Chain after applying the policies, according to [OpenID.Federation]. The client_metadata parameter, if present in the Authorization Request, MUST be ignored when this Client Identifier Prefix is used. Example Client Identifier: openid_federation:https://federation-verifier.example.com.Â¶

            
              decentralized_identifier: This prefix value indicates that the original Client Identifier (the part without the prefix decentralized_identifier:) is a Decentralized Identifier as defined in [DID-Core]. The request MUST be signed with a private key associated with the DID. A public key to verify the signature MUST be obtained from the verificationMethod property of a DID Document. Since DID Document may include multiple public keys, a particular public key used to sign the request in question MUST be identified by the kid in the JOSE Header. To obtain the DID Document, the Wallet MUST use DID Resolution defined by the DID method used by the Verifier. All Verifier metadata other than the public key MUST be obtained from the client_metadata parameter as defined in Section 5.1. Example Client Identifier: decentralized_identifier:did:example:123.Â¶
The following is a non-normative example of a header and a body of a signed Request Object when the Client Identifier Prefix is decentralized_identifier:Â¶
HeaderÂ¶

```
{
  "typ": "oauth-authz-req+jwt",
  "alg": "RS256",
  "kid": "did:example:123#1"
}

```Â¶

BodyÂ¶

```
{
  "client_id": "decentralized_identifier:did:example:123",
  "response_type": "vp_token",
  "redirect_uri": "https://client.example.org/callback",
  "nonce": "n-0S6_WzA2Mj",
  "dcql_query": { ... },
  "client_metadata": {
    "vp_formats_supported": {
      "dc+sd-jwt": {
        "sd-jwt_alg_values": ["ES256", "ES384"],
        "kb-jwt_alg_values": ["ES256", "ES384"]
      }
    }
  }
}

```Â¶


            
              verifier_attestation: This Client Identifier Prefix allows the Verifier to authenticate using a JWT that is bound to a certain public key as defined in Section 12. When the Client Identifier Prefix is verifier_attestation, the original Client Identifier (the part without the verifier_attestation: prefix) MUST equal the sub claim value in the Verifier attestation JWT. The request MUST be signed with the private key corresponding to the public key in the cnf claim in the Verifier attestation JWT. This serves as proof of possession of this key. The Verifier attestation JWT MUST be added to the jwt JOSE Header of the request object (see Section 12). The Wallet MUST validate the signature on the Verifier attestation JWT. The iss claim value of the Verifier Attestation JWT MUST identify a party the Wallet trusts for issuing Verifier Attestation JWTs. If the Wallet cannot establish trust, it MUST refuse the request. If the issuer of the Verifier Attestation JWT adds a redirect_uris claim to the attestation, the Wallet MUST ensure the redirect_uri request parameter value exactly matches one of the redirect_uris claim entries. All Verifier metadata other than the public key MUST be obtained from the client_metadata parameter. Example Client Identifier: verifier_attestation:verifier.example.Â¶

            
              x509_san_dns: When the Client Identifier Prefix is x509_san_dns, the original Client Identifier (the part after the x509_san_dns: prefix) MUST be a DNS name and match a dNSName Subject Alternative Name (SAN) [RFC5280] entry in the leaf certificate passed with the request. The request MUST be signed with the private key corresponding to the public key in the leaf X.509 certificate of the certificate chain added to the request in the x5c JOSE header [RFC7515] of the signed request object. The Wallet MUST validate the signature and the trust chain of the X.509 certificate. All Verifier metadata other than the public key MUST be obtained from the client_metadata parameter. The following requirement applies unless the interaction is using the DC API as defined in Appendix A: If the Wallet can establish trust in the Client Identifier authenticated through the certificate, e.g. because the Client Identifier is contained in a list of trusted Client Identifiers, it may allow the client to freely choose the redirect_uri value. If not, the FQDN of the redirect_uri value MUST match the Client Identifier without the prefix x509_san_dns:. Example Client Identifier: x509_san_dns:client.example.org.Â¶

            
              x509_hash: When the Client Identifier Prefix is x509_hash, the original Client Identifier (the part without the x509_hash: prefix) MUST be a hash and match the hash of the leaf certificate passed with the request. The request MUST be signed with the private key corresponding to the public key in the leaf X.509 certificate of the certificate chain added to the request in the x5c JOSE header parameter [RFC7515] of the signed request object. The value of x509_hash is the base64url-encoded value of the SHA-256 hash of the DER-encoded X.509 certificate. The Wallet MUST validate the signature and the trust chain of the X.509 leaf certificate. All Verifier metadata other than the public key MUST be obtained from the client_metadata parameter. Example Client Identifier: x509_hash:Uvo3HtuIxuhC92rShpgqcT3YXwrqRxWEviRiA0OZszkÂ¶

            
              origin: This reserved Client Identifier Prefix is defined in Appendix A.2. The Wallet MUST NOT accept this Client Identifier Prefix in requests. In OpenID4VP over the Digital Credentials API, the audience of the Credential Presentation is always the origin value prefixed by origin:, for example origin:https://verifier.example.com/.Â¶

          
To use the Client Identifier Prefixes openid_federation, decentralized_identifier, verifier_attestation, x509_san_dns and x509_hash, Verifiers MUST be capable of securely storing private key material. This might require changes to the technical design of native apps as such apps are typically public clients.Â¶
Other specifications can define further Client Identifier Prefixes. It is RECOMMENDED to use collision-resistant names for such values.Â¶


### 5.10. Request URI Method post
This request is handled by the Request URI endpoint of the Verifier.Â¶
The request MUST use the HTTP POST method with the https scheme, and the content type application/x-www-form-urlencoded and the Accept header set to application/oauth-authz-req+jwt. The names and values in the body MUST be encoded using UTF-8.Â¶
The following parameters are defined to be included in the request to the Request URI Endpoint:Â¶

          
wallet_metadata:
          OPTIONAL. A string containing a JSON object containing metadata parameters as defined in Section 10.Â¶

          

wallet_nonce:
          OPTIONAL. A string value used to mitigate replay attacks of the Authorization Request. When received, the Verifier MUST use it as the wallet_nonce value in the signed authorization request object. Value can be a base64url-encoded, fresh, cryptographically random number with sufficient entropy.Â¶

        

If the Wallet requires the Verifier to encrypt the Request Object, it SHOULD use the jwks parameter within the wallet_metadata parameter to pass public encryption keys. If the Wallet requires an encrypted Authorization Response, it SHOULD specify supported encryption algorithms using the authorization_encryption_alg_values_supported and authorization_encryption_enc_values_supported parameters.Â¶
Additionally, if the Client Identifier Prefix permits signed Request Objects, the Wallet SHOULD list supported cryptographic algorithms for securing the Request Object through the request_object_signing_alg_values_supported parameter. Conversely, the Wallet MUST NOT include this parameter if the Client Identifier Prefix precludes signed Request Objects.Â¶
Additional parameters MAY be defined and used in the request to the Request URI Endpoint.
The Verifier MUST ignore any unrecognized parameters.Â¶
The following is a non-normative example of a request:Â¶

```
POST /request HTTP/1.1
Host: client.example.org
Content-Type: application/x-www-form-urlencoded

wallet_metadata=%7B%22vp_formats_supported%22%3A%7B%22dc%2Bsd-jwt%22%3A%7B%22sd-jwt_a
lg_values%22%3A%20%5B%22ES256%22%5D%2C%22kb-jwt_alg_values%22%3A%20%5B%22ES256%22%5D%
7D%7D%7D&
wallet_nonce=qPmxiNFCR3QTm19POc8u

```Â¶


#### 5.10.1. Request URI Response
The Request URI response MUST be an HTTP response with the content type application/oauth-authz-req+jwt and the body being a signed, optionally encrypted, request object as defined in [RFC9101]. The request object MUST fulfill the requirements as defined in Section 5.Â¶
The following is a non-normative example of a payload for a request object:Â¶

```
{
  "client_id": "x509_san_dns:client.example.org",
  "response_uri": "https://client.example.org/post",
  "response_type": "vp_token",
  "response_mode": "direct_post",
  "dcql_query": {...},
  "nonce": "n-0S6_WzA2Mj",
  "wallet_nonce": "qPmxiNFCR3QTm19POc8u",
  "state" : "eyJhb...6-sVA"
}

```Â¶

The Wallet MUST process the request as defined in [RFC9101]. Additionally, if the Wallet passed a wallet_nonce in the POST request, the Wallet MUST validate whether the request object contains the respective nonce value in a wallet_nonce claim. If it does not, the Wallet MUST terminate request processing.Â¶
The Wallet MUST extract the set of Authorization Request parameters from the Request Object. The Wallet MUST only use the parameters in this Request Object, even if the same parameter was provided in an Authorization Request query parameter. The Client Identifier value in the client_id Authorization Request parameter and the Request Object client_id claim value MUST be identical, including the Client Identifier Prefix. If any of these conditions are not met, the Wallet MUST terminate request processing.Â¶
The Wallet then validates the request as specified in OAuth 2.0 [RFC6749].Â¶


#### 5.10.2. Request URI Error Response
If the Verifier responds with any HTTP error response, the Wallet MUST terminate the process.Â¶


### 5.11. Verifier Info
Verifier Info parameter allows the Verifier to provide additional context or metadata as part of the Authorization Request attested by a trusted third party. These inputs can support a variety of use cases, such as helping the Wallet apply policy decisions, validating eligibility, or presenting more meaningful information to the End-User during consent.Â¶
Each Verifier Info object contains a type identifier, associated data and optionally references to Credential identifiers. The format and semantics of these attestations are defined by ecosystems or profiles.Â¶
For example, a Verifier might include:Â¶

A registration certificate issued by a trusted authority, to prove that the Verifier has publicly registered its intent to request certain credentials.Â¶

          A policy statement, such as a signed document describing acceptable use, retention periods, or access rights.Â¶

          The confirmation of a role of the Verifier in a certain domain, e.g. the Verifier might be a certified payment service provider under the EU's Payment Service Directive 2.Â¶

        
The Verifier Info parameter is optional. Wallets MAY use them to make authorization decisions or to enhance the user experience, but they SHOULD ignore any unrecognized or unsupported Verifier Info types.Â¶


#### 5.11.1. Proof of Possession
This specification supports two models for proof of possession:Â¶


              claim-bound attestations: The attestation is not signed by the Verifier, but bound to it. The exact binding mechanism is defined by the type of the definition. For example for JWTs, the sub claim is including the distinguished name of the Certificate that was used to sign the request. The binding may also include the client_id parameter.Â¶

            
              key-bound attestations: The attestation's proof of possession is signed by the Verifier with a key contained or related to the attestation. To bind the signature to the presentation request, the respective signature object should include the nonce and client_id request parameters. The attestation and the proof of possession have to be passed in the attachment.Â¶

          
The Wallet MUST validate such proofs if defined by the profile and ignore or reject attachments that fail validation.Â¶
