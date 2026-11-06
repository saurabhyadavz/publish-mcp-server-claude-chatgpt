# Tool design reference

## A good tool definition (Python, MCP SDK style)

```python
@mcp.tool(
    name="get_marked_answer",
    title="A marked answer",
    description=("One marked answer: the mark and every mark lost with its reason, the parts met "
                 "and missed, and the closest reference answer beside it."),
    annotations=ToolAnnotations(title="A marked answer", readOnlyHint=True, destructiveHint=False,
                                idempotentHint=True, openWorldHint=False),
    structured_output=True,
)
def get_marked_answer(upload_id: Annotated[str, Field(description="the copy's id, as list_my_copies returns it")],
                      label: Annotated[str, Field(description="the answer's label, e.g. '1' or '2a'")]) -> MarkedAnswer:
    ...
```

## Annotation cheat sheet

| Tool kind | readOnly | destructive | idempotent | openWorld |
|---|---|---|---|---|
| Read the user's own data | true | false | true | false |
| Save / bookmark (same call twice = same state) | false | false | true | false |
| Start something new each call (a quiz) | false | false | false | false |
| Spends credits or money | false | **true** | false | false |
| Calls the public internet on the user's behalf | depends | depends | depends | **true** |

## A registry audit test

```python
import re
def test_every_tool_meets_both_stores(tools):            # tools = the server's tools/list
    for t in tools:
        assert re.fullmatch(r"[a-z]+(_[a-z]+)+", t.name) and len(t.name) <= 64, t.name
        a = t.annotations
        assert t.title and a.title, t.name
        assert None not in (a.read_only_hint, a.destructive_hint, a.idempotent_hint, a.open_world_hint), t.name
        assert t.output_schema and t.output_schema.get("properties"), t.name
        for banned in (r"\buse this\b", r"\bstart here\b"):
            assert not re.search(banned, t.description, re.I), (t.name, banned)
```

## Snapshot the tool list

Keep `tests/snapshots/tools.json` (name, title, description, annotations, input and output
schemas) and fail CI when it changes without the snapshot being updated. Reviews re-scan your
tools; an accidental description change can trigger a new review finding.

## Server instructions template

```
<App> does <one sentence>. Facts and numbers come only from its tools; never estimate them.
For "<common request>", call <tool_a> first, then <tool_b>.
When the user asks for <thing a built-in feature could also do>, use <your_tool>; never write
<that thing> of your own instead.
Speak plainly; say which items are the user's own and which are reference material.
```

## Measuring result size on real data

Run each list tool against a copy of production data (read-only) with the largest limit it
allows, and assert `len(json.dumps(result)) < 20000`. Seeded test rows are much smaller than real
ones; a field that adds 300 characters per item is invisible in tests and fatal on real data.
