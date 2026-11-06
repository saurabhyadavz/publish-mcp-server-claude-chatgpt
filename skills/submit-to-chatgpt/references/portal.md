# platform.openai.com/plugins, screen by screen (November 2026)

## Plugins list
"Upload new or existing plugin (Compress your plugin folder into a .zip file before uploading)".
Steps shown: Create your plugin with Codex (Plugin Creator / prepare-plugin-submission skill),
Upload your plugin ZIP, Complete automated checks, Submit for review, Publish your plugin.

## A plugin's page
Header: icon, name, short description; **MCP configuration** (e.g. "Configuration incomplete"),
**Review status** (e.g. "Needs attention"), **Publication** ("Not published").
Tabs: **Metadata & Skills** (version dropdown "1.0.0 · Draft", "…", **Upload new version**,
**Delete**) and **MCPs**.

## MCPs tab
Server card: MCP URL, Authentication (Authorized), MCP key, Domain verification badge;
buttons **Reconnect**, **Rescan**, download. Sections: Server instructions, Tools (each with
availability and "last checked"). **Findings** panel with All / Blocking tabs and Copy findings.

## Connect MCP server panel
Tags: "Domain verification required", "Authorized". Fields: MCP Server URL, Authentication,
OAuth redirect URI, Uploaded MCP settings (the ZIP's mcp.json as JSON), then the domain
challenge and the Connect button below.

## Review information panel
"Required information missing in …" lists the incomplete steps. Steps: Countries and
translations · Reviewer credentials · Test cases · Negative test cases · Supporting content.
Read-only fields come from the ZIP ("To change read-only information, update your plugin ZIP
and upload it again"). Buttons: Back, Save details, Next.

## Upload errors seen, and the fix
| Message | Fix |
|---|---|
| Invalid Codex compatibility overlay: …tools_triggered: Input should be a valid string | join tool names with ", " |
| Update the MCP authentication settings. Declare both authorizationUrl and tokenUrl for OAuth. | add both under extensions.com.openai.auth |
| Dark brand color must have at least 2:1 contrast against #212121. | a lighter dark-mode colour |
| Demo recording URL is required. | paste the video link in Supporting content |
| This new tool definition needs further review before it can be published. | none: manual review |
