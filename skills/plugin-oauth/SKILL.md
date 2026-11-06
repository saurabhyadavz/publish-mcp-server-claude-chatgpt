---
name: plugin-oauth
description: Add OAuth 2.1 sign-in to a remote MCP server so ChatGPT, Claude and other MCP clients can link a user's account - discovery documents, PKCE S256, Client ID Metadata Documents (CIMD) for ChatGPT and Claude plus Dynamic Client Registration (DCR) for everyone else, redirect allowlists, the iss parameter, refresh-token rotation, scopes, a consent page, and a reviewer email-and-password sign-in with no verification codes. Use when building or debugging MCP authentication, when a store says auth settings are incomplete, when linking an account bounces back to the sign-in page, or when a reviewer can't log in.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# OAuth for an MCP server in both stores

The MCP authorization spec is OAuth 2.1 with PKCE, where your MCP server is the protected
resource and some authorization server (yours or a provider's) issues tokens. ChatGPT and Claude
both discover everything from metadata, register themselves, send the user to your sign-in page,
and come back with a code. Endpoint shapes and payloads: `references/endpoints.md`.

## What to serve

1. **Protected resource metadata** (RFC 9728) at
   `https://api.example.com/.well-known/oauth-protected-resource`: the resource (`…/mcp`), the
   authorization server, the scopes.
2. **Authorization server metadata** (RFC 8414) at `/.well-known/oauth-authorization-server`:
   `authorization_endpoint`, `token_endpoint`, `registration_endpoint`, `revocation_endpoint`,
   `code_challenge_methods_supported: ["S256"]`, `client_id_metadata_document_supported: true`,
   `authorization_response_iss_parameter_supported: true`, `scopes_supported`.
3. **401 on `/mcp` without a valid token**, with `WWW-Authenticate: Bearer resource_metadata="…"`.
   A token with too few scopes gets 403 `insufficient_scope` naming the scope it needs.

## Registering clients: support both ways

- **CIMD** (ChatGPT, Claude, Claude Code): the `client_id` is an https URL on the app's own domain
  (for example `https://claude.ai/oauth/...`, `https://chatgpt.com/oauth/.../client.json`). Fetch
  it, check that its `client_id` equals its own URL, that its redirect URIs are on its own host
  or loopback, and that it uses `token_endpoint_auth_method: none`. Allow only known hosts and
  cache the document for about an hour.
- **DCR** (Cursor, Inspector, others): accept `POST /register`, rate-limit it, and allow redirect
  URIs only on known app hosts, loopback, or app schemes you trust.

Known return addresses: Claude uses `https://claude.ai/api/mcp/auth_callback`; ChatGPT shows its
`https://chatgpt.com/connector/oauth/<id>` in the portal's connect panel.

## The flow, and the details reviews check

- PKCE S256 required; reject `plain`.
- Bind every token to your MCP URL (the `resource` parameter, RFC 8707) and check it on use.
- Send `iss` on every authorization response (RFC 9207), success and error.
- Short-lived access tokens; refresh tokens that rotate, with a short reuse grace so a retried
  refresh doesn't log the user out.
- Ask for the fewest scopes at link time; ask for the sensitive one (spending credits) only
  when a tool first needs it.
- The consent page names the app (from its metadata), says whether it's a verified host, lists
  each permission in plain words, and has Allow and Cancel. Accept only real clicks
  (`event.isTrusted`) so an extension or script can't allow on the user's behalf.

## The reviewer login

Both stores' reviewers need to sign in with an email and password and no codes. Do it without
weakening real users' sign-in:

- One reviewer account in your identity provider with email/password enabled.
- Your server accepts a password sign-in **only** for that account's user id (an allowlist in
  config), never for an address that belongs to a real user, and pins the stored email so the
  token can't claim another address.
- Show the form only on the consent page, behind a small "App reviewers: sign in with email" link.
- Lift the account's usage limits and fill it with data for every test case.

## Debugging "it sends me back to the sign-in page"

Work from logs and analytics before theorising. Seen in practice:

- A trailing character in the pasted server URL ("…/mcp." → 404 at discovery).
- Another open tab of your web app signing the user out the moment the new sign-in lands
  (an auth listener that treats its first "no user yet" callback as a sign-out). Only a change
  from a signed-in user to nobody should end a session, and a tab should only adopt a token for
  the session's own person.
- Bot protection blocking the store's servers. Allow their published IP ranges for `/mcp` and
  the OAuth endpoints.
- A client-side fix that hasn't reached tabs opened before the deploy: reload them.
