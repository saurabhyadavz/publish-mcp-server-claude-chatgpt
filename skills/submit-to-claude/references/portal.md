# Claude connector portal fields (November 2026)

Generate this file from your listing source so each part can be pasted into its step.

```
## 1. Connection
- Universal URL: https://api.example.com/mcp

## 2. Tools (synced from the server; each has a title and all four hints)
- get_x (Title): reads
- mark_y (Title): spends a credit (apps ask first)

## 3. Listing
- Name: My App
- One-liner (85/200, card shows ~90): ...
- Categories: up to 5, closest matches in the dropdown (e.g. Learning, Courses & lessons, Education, Writing)
- Documentation: https://example.com/developers/mcp
- Privacy policy: https://example.com/privacy
- Support: support@example.com · https://example.com/contact
- Icon: 512 px PNG
- URL slug (permanent once published): my-app

### Description (n/2000)
...

## 4. Use cases (≥3)
- **Title**: "prompt" what Claude does.
- Before connecting: ...
- Reads or writes: ...

## 5. Company
- Name and website · contact for review updates

## 6. Authentication
- OAuth; CIMD (or DCR); return address https://claude.ai/api/mcp/auth_callback allowed

## 7. Data handling
- The API: our own, first-party
- Personal health data: no · Sponsored content: no
- What is read and kept: ...

## 8. Test & launch
Test account: reviewer@example.com (password in the credentials field only)
1. In Claude, connect <App> (https://api.example.com/mcp). Claude opens <App>'s sign-in page.
2. Click "App reviewers: sign in with email".
3. Enter the email and the password from the credentials field. No codes are asked for.
4. Click Allow.
5. In a new chat with <App> on, try the prompts below.

## 9. Compliance
Seven acknowledgements; note anything unusual (money movement, generated media, data kept).

## Allowed link URIs
- https://example.com

## Carousel screenshots
3-5 PNGs ≥1000 px wide, cropped to the card, prompt given separately.
```
