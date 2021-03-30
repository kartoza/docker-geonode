#!/usr/bin/env bash

echo "Executing bootstrap hook: $PWD"

# We use relative symlinks
ln -sf "build/.gitignore" "${PROJECT_ROOT}/.gitignore"
ln -sf "build/.envrc" "${PROJECT_ROOT}/.envrc"
ln -sf "build/.env" "${PROJECT_ROOT}/.env"
ln -sf "build/Makefile" "${PROJECT_ROOT}/Makefile"
ln -sf "build/default.nix" "${PROJECT_ROOT}/default.nix"
ln -sf "build/shell.nix" "${PROJECT_ROOT}/shell.nix"