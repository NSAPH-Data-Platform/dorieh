#!/bin/sh
# Point git at the tracked hooks directory so every clone gets the same hooks.
cd "$(git rev-parse --show-toplevel)" || exit 1
git config core.hooksPath .githooks
echo "Git hooks enabled (core.hooksPath = .githooks)"
