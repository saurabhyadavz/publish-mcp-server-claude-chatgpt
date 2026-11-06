# Pre-build checklist

Tick each line or write what's missing. "Check" means the agent can verify it itself.

## Accounts
- [ ] OpenAI platform account; identity verification started (individual or business)
- [ ] Decided: individual name or company name on the ChatGPT listing (must match verification)
- [ ] Paid Claude plan on the account that will submit to Claude's directory
- [ ] A ChatGPT account that can add custom MCP servers, for testing
- [ ] GitHub account, if a Claude plugin bundle or a public skills repo will be published

## Domain and server
- [ ] Domain owned; MCP server will run at `https://<host>/mcp` (check: `curl -I`)
- [ ] HTTPS certificate valid (check)
- [ ] Health endpoint that shows the deployed version, so you can tell when a deploy is live
- [ ] Firewall or bot protection allows the stores' servers (Anthropic publishes its egress
      ranges; a "bot fight" mode can block tool calls)

## Pages (check each loads and says the right thing)
- [ ] Website home page
- [ ] Privacy policy: names the publisher, lists what the app reads, keeps and for how long
- [ ] Terms of service: names the publisher
- [ ] Support page or contact page
- [ ] Developer/docs page for the MCP server (Claude asks for a documentation URL)
- [ ] If selling: seller name, address and complaints contact as local law requires

## Email
- [ ] `support@<domain>` receives mail (check: `dig MX <domain>` returns records)
- [ ] SPF/DKIM set if the app sends mail

## Reviewer access
- [ ] One reviewer account, email + password, no codes, no sign-up step
- [ ] Password login allowed only for that account (by its user id), not for everyone
- [ ] Account filled with realistic data for every test case; limits lifted
- [ ] Written steps a stranger can follow to sign in from each store

## Assets
- [ ] 512×512 icon; light and dark composer icons
- [ ] Brand colours with ≥2:1 contrast (dark vs `#212121`, light vs white)
- [ ] Five good test prompts, three refused ones, with the tools each good one should call
- [ ] Demo video plan (record after deploy)
