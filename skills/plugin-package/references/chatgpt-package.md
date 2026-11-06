# ChatGPT plugin package reference

Sources: developers.openai.com/plugins/deploy/submission, /plugins/build/plugins, /plugins/reference
(read November 2026). Field names are case-sensitive.

## plugin.json

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-app", "version": "1.0.0", "description": "…",
  "author": {"name": "…", "email": "support@example.com", "url": "https://example.com"},
  "homepage": "https://example.com", "license": "LicenseRef-My-App", "keywords": ["…"],
  "extensions": {"com.openai": {
    "interface": {
      "displayName": "My App",                 // ≤ 30
      "shortDescription": "…",                 // ≤ 30
      "longDescription": "…",                  // ≤ 4000
      "developerName": "…",                    // = verified identity, ≤ 80
      "category": "Education & Research",
      "capabilities": ["…"],                   // ≤ 20 × 120
      "websiteURL": "https://…", "supportURL": "https://…",
      "privacyPolicyURL": "https://…", "termsOfServiceURL": "https://…",
      "defaultPrompt": ["…", "…", "…"],        // ≤ 3 × 128
      "brandColor": "#07163D",                 // ≥ 2:1 vs white
      "brandColorDark": "#4F62F2",             // ≥ 2:1 vs #212121
      "composerIcon": "./assets/icon.png", "composerIconDark": "./assets/icon-dark.png", "logo": "./assets/logo.png"
    },
    "onboardingSkill": "./skills/get-started/SKILL.md",
    "review": {
      "test_cases": {
        "positive": [{"description": "…", "prompt": "…", "tools_triggered": "tool_a, tool_b", "expected_behavior": "…"}],
        "negative": [{"description": "…", "prompt": "…"}]
      },
      "demo_recording_url": "https://youtu.be/…",   // required to submit; omit until you have it
      "commerce": false,
      "commerce_description": "No purchases in the plugin."
    },
    "publication": {"countries": [], "release_notes": "…"}
  }}
}
```

Five positive and three negative cases at submission (uploads accept fewer). Positive
`description` ≤ 4000. Optional per case: `file_attachment_urls` (list), `expected_output_url`.

## mcp.json

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {"my-app": {
    "type": "streamable-http",
    "url": "https://api.example.com/mcp",
    "extensions": {"com.openai": {"auth": {
      "type": "oauth",
      "client": {"mode": "cimd"},
      "authorizationUrl": "https://api.example.com/authorize",
      "tokenUrl": "https://api.example.com/token",
      "baseScopes": ["data:read"]
    }}}
  }}
}
```

Auth keys: `type` (`oauth`, `mixed`, `none`, `api_key`), `client.mode` (`provided` with
`clientId`, `dcr`, or `cimd`), `authorizationUrl`, `tokenUrl`, `registrationUrl`,
`authorizationServerBase`, `resource`, `baseScopes`, `defaultScopes`, OIDC fields.

## Things the ZIP must not contain

Lifecycle hooks, `.app.json` apps, secrets. Keep the ZIP's files at its root (zip the folder's
contents, not the folder).
