let
	bootstrap = import <nixpkgs> {};
	pinned-pkgs = import (bootstrap.fetchFromGitHub {
		owner = "NixOS";
		repo = "nixpkgs";
		# branch@date: master@2021-02-23
		rev = "11cd34cd592f917bab5f42e2b378ab329dee3bcf";
		sha256 = "sha256:1mgga54np22csagzaxfjq5hrgyv8y4igrl3f6z24fb39rvvx236w";
	}) {};
in
{
  pkgs ? pinned-pkgs }:
with pkgs;
stdenv.mkDerivation rec {
	pname = "booststrapper";
	version = "1.0";
	dontUnpack = true;
	propagatedBuildInputs = [
		direnv
		nix-direnv
		yq
		jq
		python38
		python38Packages.jinja2
		python38Packages.python-dotenv
	];
	dontInstall = true;
	meta = {
		description = "Development environment in this repo";
		maintainers = [ "Rizky Maulana Nugraha <lana.pcfre@gmail.com>" ];
	};
}
