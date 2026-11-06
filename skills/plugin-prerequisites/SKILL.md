---
name: plugin-prerequisites
description: Everything to set up before building or submitting a ChatGPT plugin or Claude connector, so a submission isn't blocked for days at the end - accounts and plans, identity verification, a domain with HTTPS, privacy and terms pages that name the publisher, a support mailbox that receives mail, a reviewer test account with no verification codes, icons and a demo video. Use when someone is starting an MCP app, asks what they need before submitting, or a portal rejects them for a missing account, page, email or login.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# Prerequisites for both stores

Most delays in a first submission are not code. They are an account that needs verifying, a
legal page that doesn't name anyone, or a support address that bounces. Check these first; most
take minutes to start and days to finish, so start the slow ones (identity verification, a
company) on day one.

Work through the checklist in `references/checklist.md` with the person. For each item: check it
yourself where you can (DNS, HTTPS, a page's text), mark it done, or say exactly what they must do.

## The slow ones: start today

- **OpenAI publisher identity.** The ChatGPT directory shows the *verified* identity as the
  developer name, and the package's `developerName` must match it. Verify on
  platform.openai.com as an individual (fast) or a business (needs a registered company). An
  individual can move to a company later.
- **A registered business, if they want a company name on the listing.** Weeks in many
  countries. Don't let it block the first listing.
- **Claude submission needs a paid Claude plan** on the account that submits (Pro or Max for a
  personal account). A free account can test a custom connector but can't submit.

## The ones people forget

- **A support mailbox that actually receives mail.** Check the domain has MX records
  (`dig MX example.com`). A `support@` address on a domain with no MX bounces, and both stores
  ask for one.
- **Privacy policy and terms that name the publisher** (the verified person or company), say what
  data the app reads and keeps, and give a contact. OpenAI reviews these pages.
- **If the app sells anything**, local law may require more on those pages (for example, India's
  e-commerce rules want the seller's name, address and a grievance officer). Plugins themselves
  must not sell in ChatGPT; checkout stays on your site.
- **A reviewer account.** Both stores' reviewers must sign in "with no further configuration":
  no SMS, email or authenticator codes, and no account creation. That usually means an email
  and password login for one dedicated account, allowed only for that account, already filled
  with realistic data and with any usage limits lifted. Google-only sign-in is not enough. See
  `plugin-oauth` for how to add it safely.
- **The MCP server on your own domain with HTTPS** (for example `https://api.example.com/mcp`).
  OpenAI verifies the domain with a file at `/.well-known/openai-apps-challenge` on that host.
- **Plans for testing.** Testing a custom MCP server inside ChatGPT needs an account that can add
  custom MCP servers (chatgpt.com/plugins → Add → Add custom MCP server). Claude: Settings →
  Connectors → Add custom connector.

## Assets to prepare while waiting

- Square icon, 512×512 PNG, readable small; a light and a dark composer icon for ChatGPT.
- Brand colours: ChatGPT checks contrast. The dark brand colour needs at least 2:1 against
  `#212121` (a dark navy fails at about 1:1); use the light colour against white the same way.
- A 3–5 minute demo video for ChatGPT's review (shot list in `submit-to-chatgpt`), uploaded
  unlisted. Record it after the server is deployed and every test case passes.
- Five test prompts that should work and three that should be refused, written from what the
  app really does. Both reviews use them.
