with import <nixpkgs> {}; {
    gccEnv = stdenvNoCC.mkDerivation {
        name = "npm-environment";
        buildInputs = with pkgs; [
            nodejs
            sqlite
        ];
    };
}
