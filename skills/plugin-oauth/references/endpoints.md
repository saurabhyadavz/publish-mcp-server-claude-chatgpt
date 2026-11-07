# OAuth endpoints reference

## /.well-known/oauth-protected-resource (on the MCP host)

```json
{
  "resource": "https://api.example.com/mcp",
  "authorization_servers": ["https://api.example.com"],
  "scopes_supported": ["data:read", "data:write", "spend"],
  "bearer_methods_supported": ["header"]
}
```

## /.well-known/oauth-authorization-server

```json
{
  "issuer": "https://api.example.com",
  "authorization_endpoint": "https://api.example.com/authorize",
  "token_endpoint": "https://api.example.com/token",
  "registration_endpoint": "https://api.example.com/register",
  "revocation_endpoint": "https://api.example.com/revoke",
  "scopes_supported": ["data:read", "data:write", "spend"],
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "token_endpoint_auth_methods_supported": ["none", "client_secret_post", "client_secret_basic"],
  "client_id_metadata_document_supported": true,
  "authorization_response_iss_parameter_supported": true
}
```

## The ChatGPT package must repeat two of these

ChatGPT's `mcp.json` (see `plugin-package`) needs `authorizationUrl` and `tokenUrl` next to the
client mode, even though discovery provides them. Generate them from the same constants your
server uses for its metadata, and test that they match.

```json
"auth": {
  "type": "oauth",
  "client": { "mode": "cimd" },
  "authorizationUrl": "https://api.example.com/authorize",
  "tokenUrl": "https://api.example.com/token",
  "baseScopes": ["data:read", "data:write"]
}
```

## CIMD document checks (what you fetch from the client_id URL)

- `client_id` equals the URL you fetched
- `redirect_uris`: non-empty; each on the document's own host, a known app host, or loopback
- `token_endpoint_auth_method` is `none` (public client) unless you verify keys
- `grant_types` includes `authorization_code`
- Cache ~1 hour; serve the last good copy for a day if the fetch fails

## Tests worth having

- A token for another user's resource is refused (no cross-account reads).
- A token minted for a different `resource` is refused.
- A refresh token used twice outside the grace window revokes the chain.
- The reviewer password sign-in is refused for any account but the allowlisted id, and for an
  address on the owner/admin list, and repeated wrong passwords are slowed or blocked.
- The consent page ignores synthetic clicks, won't load in a frame, and refuses an Allow POST
  without the session's CSRF token.
- A CIMD `client_id` on an unknown host is refused without being fetched.
