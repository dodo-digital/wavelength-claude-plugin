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

# --- ZeroBounce (email validation) ---
echo "--- ZeroBounce ---"
echo "Used for email validation before Reply.io upload."
echo "Get your API key at: https://www.zerobounce.net/members/api"
echo ""
read -rp "ZeroBounce API key (or press Enter to skip): " ZB_KEY

if [[ -n "$ZB_KEY" ]]; then
  # Check if npm package is installed
  if ! command -v zerobounce-mcp &>/dev/null; then
    echo "Installing @zerobounce/mcp..."
    npm install -g @zerobounce/mcp
  fi
  claude mcp add zerobounce -- zerobounce-mcp --api-key="$ZB_KEY"
  echo "✓ ZeroBounce MCP added"
else
  echo "⏭ Skipped ZeroBounce"
fi

echo ""

# --- Clearout (email validation) ---
echo "--- Clearout ---"
echo "Second email validation source. NOT YET AVAILABLE as a standalone MCP."
echo "Clearout has a REST API (https://docs.clearout.io/api-overview.html)."
echo "A custom MCP will be built for this — skipping for now."
echo "⏭ Skipped Clearout (custom MCP needed)"

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
echo "  - Clearout (email validation)"
echo "  - OneDrive (file storage — or configure community MCP manually)"
