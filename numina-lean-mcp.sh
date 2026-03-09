#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOG_NAME="${MCP_LOG_NAME:-mcp_lean_lsp}"
LOG_DIR="${MCP_LOG_DIR:-$PROJECT_DIR}"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# -----------------------------------------------------------------------
# Isolation: when LEAN_PROJECT_PATH is set and has a .lake directory,
# create an isolated copy so multiple MCP processes don't conflict.
#
# - Config files (lakefile.toml, lean-toolchain, etc.) are copied
# - Source dirs/files are symlinked back to the original (zero overhead)
# - .lake/packages is symlinked (shared, ~7GB)
# - .lake/build is copied (isolated per session, ~100-200MB)
# -----------------------------------------------------------------------
if [ -n "$LEAN_PROJECT_PATH" ] && [ -d "$LEAN_PROJECT_PATH/.lake" ]; then
    SESSION_DIR="/tmp/lean-mcp-session-$$"
    mkdir -p "$SESSION_DIR/.lake"

    # Copy config files that lake needs to be real files
    for f in lakefile.toml lakefile.lean lean-toolchain lake-manifest.json; do
        [ -f "$LEAN_PROJECT_PATH/$f" ] && cp "$LEAN_PROJECT_PATH/$f" "$SESSION_DIR/"
    done

    # Symlink everything else (source dirs, .lean files, .git, etc.)
    for item in "$LEAN_PROJECT_PATH"/*; do
        name=$(basename "$item")
        case "$name" in
            .lake|lakefile.toml|lakefile.lean|lean-toolchain|lake-manifest.json) continue ;;
        esac
        [ ! -e "$SESSION_DIR/$name" ] && ln -s "$item" "$SESSION_DIR/$name"
    done
    # Hidden files (.gitignore, .git, etc.)
    for item in "$LEAN_PROJECT_PATH"/.*; do
        name=$(basename "$item")
        case "$name" in
            .|..|.lake) continue ;;
        esac
        [ ! -e "$SESSION_DIR/$name" ] && ln -s "$item" "$SESSION_DIR/$name"
    done

    # .lake/packages: symlink (shared, read-only)
    [ -d "$LEAN_PROJECT_PATH/.lake/packages" ] && \
        ln -s "$LEAN_PROJECT_PATH/.lake/packages" "$SESSION_DIR/.lake/packages"

    # .lake/build: copy (isolated per session)
    if [ -d "$LEAN_PROJECT_PATH/.lake/build" ]; then
        cp -a "$LEAN_PROJECT_PATH/.lake/build" "$SESSION_DIR/.lake/build"
    else
        mkdir -p "$SESSION_DIR/.lake/build"
    fi

    # Clean up on exit
    cleanup() { rm -rf "$SESSION_DIR"; }
    trap cleanup EXIT INT TERM

    export LEAN_PROJECT_PATH="$SESSION_DIR"
fi

exec uvx --with-editable "$PROJECT_DIR" python -m lean_lsp_mcp.server 2>> "$LOG_DIR/$LOG_NAME.log"
