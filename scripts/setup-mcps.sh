#!/usr/bin/env bash
# Setup MCP servers for the Wavelength Claude Code plugin.
# Run this once after cloning the repo.
#
# Usage:
#   ./scripts/setup-mcps.sh
#
# You'll be prompted for API keys. Keys are stored in your local
# Claude config (~/.claude.json), never committed to the repo.

set -euo pipefail

echo "=== Wavelength Plugin — MCP Setup ==="
echo ""

# --- Wavelength MCP (email validation) ---
echo "--- Wavelength MCP ---"
echo "Hosted email validation server (Clearout + ZeroBounce)."
echo "API keys are server-side — you only need your personal token."
echo "Get your token from Dino."
echo ""
read -rp "WL_MCP_TOKEN (or press Enter to skip): " WL_TOKEN

if [[ -n "$WL_TOKEN" ]]; then
  # Detect shell profile
  if [[ -f "$HOME/.zshrc" ]]; then
    PROFILE="$HOME/.zshrc"
  elif [[ -f "$HOME/.bashrc" ]]; then
    PROFILE="$HOME/.bashrc"
  else
    PROFILE="$HOME/.profile"
  fi

  # Append export if not already present
  if ! grep -q 'WL_MCP_TOKEN' "$PROFILE" 2>/dev/null; then
    echo "" >> "$PROFILE"
    echo "# Wavelength MCP token (email validation)" >> "$PROFILE"
    echo "export WL_MCP_TOKEN=\"$WL_TOKEN\"" >> "$PROFILE"
    echo "✓ WL_MCP_TOKEN added to $PROFILE"
  else
    echo "⚠ WL_MCP_TOKEN already exists in $PROFILE — not overwriting"
  fi

  # Export for current session
  export WL_MCP_TOKEN="$WL_TOKEN"
  echo "✓ Wavelength MCP configured (token set for this session)"
  echo "  Restart Claude Code to connect via .mcp.json"
else
  echo "⏭ Skipped Wavelength MCP"
fi

echo ""

# --- Reply.io (outreach) ---
echo "--- Reply.io ---"
echo "The official Reply.io MCP only supports search (limited)."
echo "A custom MCP will be built to support contact upload and campaign management."
echo "⏭ Skipped Reply.io (custom MCP needed)"

echo ""

# --- OneDrive (file storage) ---
echo "--- OneDrive ---"
echo "Used for saving output CSVs. Requires Azure app registration."
echo "Community MCP: https://github.com/ftaricano/mcp-onedrive-sharepoint"
echo "Setup requires MICROSOFT_CLIENT_ID and MICROSOFT_TENANT_ID."
echo "⏭ Skipped OneDrive (requires Azure app setup — configure manually)"

echo ""

# --- HubSpot (CRM — optional) ---
echo "--- HubSpot ---"
echo "Optional. Grata syncs directly to HubSpot, so this is not required"
echo "for the company-processor workflow. Add later if needed for other skills."
echo "Official MCP: https://developers.hubspot.com/mcp"
echo "⏭ Skipped HubSpot (optional — add manually if needed)"

echo ""
echo "=== Setup complete ==="
echo ""
echo "MCPs configured. Run 'claude mcp list' to verify."
echo ""
echo "Still needed (custom MCPs to be built):"
echo "  - Reply.io (contact upload, campaign management)"
echo "  - OneDrive (file storage — or configure community MCP manually)"
