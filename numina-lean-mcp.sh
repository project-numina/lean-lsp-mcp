#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

exec uvx --with-editable "$PROJECT_DIR" python -m lean_lsp_mcp.server 2>> "$PROJECT_DIR/mcp_lean_lsp.log"
