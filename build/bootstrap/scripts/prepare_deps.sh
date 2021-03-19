#!/usr/bin/env bash

# This script is used to install minimal dependency manager and environment manager

# Check nix exists

if [[ -z "$(command -v nix)" ]]; then
    echo "Nix don't exists."
    echo "Attempting self install nix."
    sh <(curl -L https://nixos.org/nix/install) --daemon
else
    echo "Nix exists."
fi

# Check direnv exists

# In the bootstrap phase, do everything natively because we haven't
# set up dependency manager and environment manager
# build basic dependency and setup direnv
nix-build --no-out-link
nix-env -iA nixpkgs.direnv

# Direnv should be the very first entry point that let us hook into nix-shell
# This means that putting the hook script inside nix-shell is not ideal for this.
# We hook direnv natively to host.

# check if we already been hooked to direnv

# hook direnv in zsh

if cat ~/.zshrc | grep direnv; then
    echo "Direnv hook exists in zsh"
else
    echo "Hooking direnv to zsh"
    echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
fi 

# hook direnv in bash
if cat ~/.bashrc | grep direnv; then
    echo "Direnv hook exists in bash"
else
    echo "Hooking direnv to bash"
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
fi

# direnv is hooked but not available in this script yet at the moment.
eval "$(direnv hook bash)"
direnv allow
