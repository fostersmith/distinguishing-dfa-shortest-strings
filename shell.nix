{ pkgs ? (import <nixpkgs> {}).pkgs }:
with pkgs;
let
  pythonPackages = python314Packages;
in
mkShell {
  packages = [
    pythonPackages.python
    pythonPackages.pip
    pythonPackages.matplotlib
  ];
  shellHook = ''
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  '';
}
