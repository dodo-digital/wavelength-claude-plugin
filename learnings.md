# Plugin MCP Learnings

## Status: MCP NOT SHOWING

Plugin v1.3.3 installs, shows skills and hooks, but MCP server does not appear.

---

## Current Structure (v1.3.3)

### .claude-plugin/plugin.json
```json
{
  "name": "wavelength-equity",
  "version": "1.3.3",
  "mcpServers": {
    "wavelength": {
      "type": "http",
      "url": "https://wavelength-mcp.vercel.app/api/mcp"
    }
  }
}
```

### .mcp.json (root level, flat format)
```json
{
  "wavelength": {
    "type": "http",
    "url": "https://wavelength-mcp.vercel.app/api/mcp"
  }
}
```

### .claude-plugin/marketplace.json
```json
{
  "name": "wavelength",
  "plugins": [{ "name": "wavelength-equity", "source": "./" }]
}
```

### installed_plugins.json entry
```json
"wavelength-equity@wavelength": [{
  "scope": "user",
  "installPath": "~/.claude/plugins/cache/wavelength/wavelength-equity/1.3.3",
  "version": "1.3.3",
  "gitCommitSha": "6fdae8b..."
}]
```

---

## Working Plugin References

### Compound Engineering (inline mcpServers — WORKS)
- Marketplace: `every-marketplace`
- scope: `project` (projectPath: react-native-boilerplate)
- plugin.json has inline `mcpServers` — NO .mcp.json file
- NO marketplace.json in .claude-plugin/
- Context7 MCP tools show up in all projects

```json
{
  "name": "compound-engineering",
  "version": "2.9.3",
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

### Linear (external_plugins, .mcp.json — WORKS)
- Lives in: `marketplaces/claude-plugins-official/external_plugins/linear/`
- plugin.json has NO mcpServers field
- .mcp.json is flat format (server names at root, no wrapper)

```json
// plugin.json
{ "name": "linear", "description": "..." }

// .mcp.json
{ "linear": { "type": "http", "url": "https://mcp.linear.app/mcp" } }
```

### Context7 (external_plugins, .mcp.json — WORKS)
- Same pattern as Linear
- plugin.json has NO mcpServers field
- .mcp.json is flat with stdio server (npx command)

---

## Key Differences Between Working and Broken

| Factor | Compound Eng | Linear/Context7 | Wavelength |
|--------|-------------|-----------------|------------|
| Marketplace type | every-marketplace (multi-plugin) | claude-plugins-official (external_plugins/) | wavelength (self-hosted single-plugin) |
| mcpServers in plugin.json | Yes (inline) | No | Yes (inline) — added in v1.3.3 |
| .mcp.json file | No | Yes (flat) | Yes (flat) — fixed in v1.3.3 |
| marketplace.json | Not present | Not present | Present in .claude-plugin/ |
| Install scope | project | (built-in/official) | user |
| Plugin source in marketplace | subdirectory path | subdirectory path | `"./"` (self-referencing) |

## Hypotheses

1. **Self-referencing marketplace**: The `"source": "./"` in marketplace.json means the plugin IS the marketplace. Official external plugins live UNDER a marketplace. Maybe the plugin loader doesn't look for mcpServers in self-referencing plugins.

2. **External plugins are special**: Linear/Context7 are in `external_plugins/` which may be a dedicated path that auto-loads .mcp.json. Regular marketplace plugins may not get this treatment.

3. **Marketplace type matters**: Maybe only plugins from specific marketplace types (official, every-marketplace) get MCP loading. Self-hosted marketplaces might not support it.

4. **Missing registration step**: There might be an additional step to register MCP servers for marketplace plugins that we're not doing.

## What We've Tried
- v1.3.0: No mcpServers field at all → no MCP
- v1.3.1: Inline mcpServers object → no MCP (at the time, URL was wrong)
- v1.3.2: File reference `"mcpServers": "./.mcp.json"` with wrapped format → no MCP
- v1.3.3: Inline mcpServers (matching Compound Engineering) + flat .mcp.json → no MCP
