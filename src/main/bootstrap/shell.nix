{ pkgs ? import <nixpkgs> {} }:
let
	local-shell = if builtins.pathExists ./local-shell.nix then (import ./local-shell.nix {
			inherit pkgs;
		}) else null;
	bootstrap-python-lib-path = builtins.toString ./python;
in
with pkgs;
mkShell {
	inputsFrom = [ (import ./default.nix {}) ] ++ lib.optionals (! isNull local-shell) [ local-shell ];
}
