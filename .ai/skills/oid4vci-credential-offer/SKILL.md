---
name: "oid4vci-credential-offer"
description: "Use when implementing credential offer flows (issuer-initiated issuance). Covers: credential_offer parameter, credential_offer_uri, grants object, authorization_code and pre-authorized_code grant types."
sections:
  - "6. Token Endpoint"
  - "6.1. Token Request"
  - "6.2. Successful Token Response"
  - "6.3. Token Error Response"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~2853 -->

## 6. Token Endpoint
The Token Endpoint issues an Access Token and, optionally, a Refresh Token in exchange for the Authorization Code that Client obtained in a successful Authorization Response. It is used in the same manner as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]. Implementers SHOULD follow the best current practices for OAuth 2.0 Security given in [[BCP240](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#BCP240)].


### 6.1. Token Request
The Token Request is made as defined in Section 4.1.3 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The following are the extension parameters to the Token Request used in the Pre-Authorized Code Flow defined in [Section 3.5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#pre-authz-code-flow):

- 
            `pre-authorized_code`: The code representing the authorization to obtain Credentials of a certain type. This parameter MUST be present if the `grant_type` is `urn:ietf:params:oauth:grant-type:pre-authorized_code`.

          - 
            `tx_code`: OPTIONAL. String value containing a Transaction Code value itself. This value MUST be present if a `tx_code` object was present in the Credential Offer (including if the object was empty). This parameter MUST only be used if the `grant_type` is `urn:ietf:params:oauth:grant-type:pre-authorized_code`.

        
Requirements around how the Wallet identifies and, if applicable, authenticates itself with the Authorization Server in the Token Request depend on the Client type defined in Section 2.1 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)] and the Client authentication method indicated in the `token_endpoint_auth_method` Client metadata (as defined in [[RFC7591](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC7591)]). The requirements specified in Sections 4.1.3 and 3.2.1 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)] MUST be followed.
For the Pre-Authorized Code Grant Type, authentication of the Client is OPTIONAL, as described in Section 3.2.1 of OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], and, consequently, the `client_id` parameter is only needed when a form of Client Authentication that relies on this parameter is used.
If the Token Request contains an `authorization_details` parameter (as defined by [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)]) of type `openid_credential` and the Credential Issuer's metadata contains an `authorization_servers` parameter, the `authorization_details` object MUST contain the Credential Issuer's identifier in the `locations` element.
If the Token Request contains a scope value related to Credential issuance and the Credential Issuer's metadata contains an `authorization_servers` parameter, it is RECOMMENDED to use a `resource` parameter [[RFC8707](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC8707)] whose value is the Credential Issuer's identifier value to allow the Authorization Server to differentiate Credential Issuers.
When the Pre-Authorized Grant Type is used, it is RECOMMENDED that the Credential Issuer issues an Access Token valid only for the Credentials indicated in the Credential Offer (see [Section 4.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer)). The Wallet SHOULD obtain a separate Access Token if it wants to request issuance of any Credentials that were not included in the Credential Offer, but were discoverable from the Credential Issuer's `credential_configurations_supported` metadata parameter.
Additional Token Request parameters MAY be defined and used,
as described in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The Authorization Server MUST ignore any unrecognized parameters.
Below is a non-normative example of a Token Request in an Authorization Code Flow:

```
POST /token HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=SplxlOBeZQQYbYS6WxSbIA
&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
&redirect_uri=https%3A%2F%2Fwallet.example.org%2Fcb
&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer
&client_assertion=eyJhbGciOiJSU...
```


#### 6.1.1. Request Credential Issuance using authorization_details Parameter
Credential Issuers MAY support requesting authorization to issue a Credential using the `authorization_details` parameter. This is particularly useful if the Credential Issuer offered multiple Credential Configurations in the Credential Offer of a Pre-Authorized Code Flow.
The Wallet can use `authorization_details` in the Token Request to request a specific Credential Configuration in both the Authorization Code Flow and the Pre-Authorized Code Flow. The value of the `authorization_details` parameter is defined in [Section 5.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-details).
Below is a non-normative example of a Token Request in a Pre-Authorized Code Flow (without Client Authentication):

```
POST /token HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:pre-authorized_code
&pre-authorized_code=SplxlOBeZQQYbYS6WxSbIA
&tx_code=493536
&authorization_details=%5B%7B%22type%22%3A%20%22openid_credential%22%2C%20%22
    credential_configuration_id%22%3A%20%22UniversityDegreeCredential%22%7D%5D
```

The Wallet may send the `authorization_details` parameter in the Token Request even when the parameter has been previously sent in the [Authorization Request](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-authz-request) as described in Section 6.1 of [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)]. It allows the AS to make a decision based on whether the Wallet is asking for more or less access than the previous request. With respect to `authorization_details` items using the `credential_configuration_id` introduced in this specification, it is RECOMMENDED that the AS would accept a request from the Wallet containing a subset of `credential_configuration_id` parameters received in the original [Authorization Request](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-authz-request) and issue a token for the reduced set.


### 6.2. Successful Token Response
Token Responses are made as defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The Authorization Server might decide to authorize issuance of multiple instances for each Credential requested in the Authorization Request. Each Credential instance is described using the same entry in the `credential_configurations_supported` Credential Issuer metadata, but contains different claim values or different subset of claims within the claims set identified by the `credential_configuration_id`.
In addition to the response parameters defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], the Authorization Server MAY return the following parameters:

- 
            `authorization_details`: REQUIRED when the `authorization_details` parameter, as defined in [Section 5.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-details), is used in either the [Authorization Request](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-authz-request) or [Token Request](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#token-request). OPTIONAL when `scope` parameter was used to request issuance of a Credential of a certain Credential Configuration. It is a non-empty array of objects, as defined in Section 7 of [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)]. In addition to the parameters defined in [Section 5.1.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#authorization-details), this specification defines the following parameter to be used with the authorization details type `openid_credential` in the Token Response:

- 
                `credential_identifiers`: REQUIRED. A non-empty array of strings, each uniquely identifying a Credential Dataset that can be issued using the Access Token returned in this response. Each of these Credential Datasets corresponds to the Credential Configuration referenced in the `credential_configuration_id` parameter. The Wallet MUST use these identifiers together with an Access Token in subsequent Credential Requests. See [Section 3.3.4](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#identifying_credential) for the summary of the options how requested Credential(s) are identified throughout the Issuance flow.

            

        
Additional Token Response parameters MAY be defined and used,
as described in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The Wallet MUST ignore any unrecognized parameters in the Token Response.
An included `authorization_details` parameter MAY also have additional data fields defined and used
when the `type` value is `openid_credential`.
The Wallet MUST ignore any unrecognized data fields in the `authorization_details` present in the Token Response.
Below is a non-normative example of a Token Response when the `authorization_details` parameter was used to request issuance of a certain Credential type:

```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp..sHQ",
  "token_type": "Bearer",
  "expires_in": 86400,
  "authorization_details": [
    {
      "type": "openid_credential",
      "credential_configuration_id": "UniversityDegreeCredential",
      "credential_identifiers": [
        "CivilEngineeringDegree-2023",
        "ElectricalEngineeringDegree-2023"
      ]
    }
  ]
}
```


### 6.3. Token Error Response
If the Token Request is invalid or unauthorized, the Authorization Server constructs the error response as defined as in Section 5.2 of OAuth 2.0 [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
The following additional clarifications are provided for some of the error codes already defined in [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]:
`invalid_request`:

- The Authorization Server does not expect a Transaction Code in the Pre-Authorized Code Flow but the Client provides a Transaction Code.

          - The Authorization Server expects a Transaction Code in the Pre-Authorized Code Flow but the Client does not provide a Transaction Code.

        
`invalid_grant`:

- The Authorization Server expects a Transaction Code in the Pre-Authorized Code Flow but the Client provides the wrong Transaction Code.

          - The End-User provides the wrong Pre-Authorized Code or the Pre-Authorized Code has expired.

        
`invalid_client`:

- The Client tried to send a Token Request with a Pre-Authorized Code without a Client ID but the Authorization Server does not support anonymous access.

        
Below is a non-normative example of a Token Error Response:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Cache-Control: no-store

{
  "error": "invalid_request"
}
```
