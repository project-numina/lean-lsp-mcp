#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOG_NAME="${MCP_LOG_NAME:-mcp_lean_lsp}"
LOG_DIR="${MCP_LOG_DIR:-$PROJECT_DIR}"

# check if log_dir exists
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

#exec uvx --with-editable "$PROJECT_DIR" python -m lean_lsp_mcp.server 2>> "$PROJECT_DIR/mcp_lean_lsp.log"
exec uvx --with-editable "$PROJECT_DIR" python -m lean_lsp_mcp.server 2>> "$LOG_DIR/$LOG_NAME.log"
