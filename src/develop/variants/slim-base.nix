let
	bootstrap = import <nixpkgs> {};
	pinned-pkgs = import (bootstrap.fetchFromGitHub {
		owner = "NixOS";
		repo = "nixpkgs";
		# branch@date: master@2021-02-23
		rev = "11cd34cd592f917bab5f42e2b378ab329dee3bcf";
		sha256 = "sha256:1mgga54np22csagzaxfjq5hrgyv8y4igrl3f6z24fb39rvvx236w";
	}) { system = "x86_64-linux"; };
in
{
  pkgs ? pinned-pkgs }:
with pkgs;
dockerTools.buildImage rec {
	name = "slim-base";
	tag = "latest";
    contents = pkgs.hello;

    config.Cmd = [ "/bin/hello" ];
}
