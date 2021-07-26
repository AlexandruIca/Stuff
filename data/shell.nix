with import <nixpkgs> {}; {
    pythonEnv = stdenvNoCC.mkDerivation {
        name = "python-environment";
        buildInputs = with pkgs; [
            python39
        ];
        shellHooks = ''source ~/.bashrc'';
    };
}
