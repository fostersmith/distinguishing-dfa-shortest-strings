{ pkgs ? (import <nixpkgs> {}).pkgs }:
with pkgs;
let
  pythonPackages = python314Packages;
in
mkShellNoCC {
  packages = [
    pythonPackages.python
    pythonPackages.matplotlib
  ];
}
