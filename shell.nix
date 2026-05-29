{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    pip
    numpy
    pandas
    openpyxl
    opencv4
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    echo "Ambiente Nix carregado com Python, Pip, OpenCV, Pandas e Numpy."
  '';
}
