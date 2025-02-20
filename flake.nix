{
  description =
    "Generic flake for Python API projects using uv2nix (dev shell only)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

  };

  outputs = { nixpkgs, uv2nix, pyproject-nix, pyproject-build-systems, ... }:
    let
      inherit (nixpkgs) lib;
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      python = pkgs.python312Full;
      ppacks = pkgs.python312Packages;
      hacks = pkgs.callPackage pyproject-nix.build.hacks { };

      # Load the project’s workspace (using the current directory as root)
      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      # Create an overlay from your pyproject metadata
      overlay = workspace.mkPyprojectOverlay {
        sourcePreference =
          "wheel"; # Prefer binary wheels for better reproducibility
      };

      # when using "wheel" as package source, most libraries will work fine, very few need overrides.
      pyprojectOverrides = _final: _prev: {
        pyqt6 = hacks.nixpkgsPrebuilt {
          from = ppacks.pyqt6;
          prev = _prev.pyqt6.overrideAttrs (old: {
            passthru = old.passthru // {
              dependencies =
                lib.filterAttrs (name: _: !lib.hasSuffix "-qt6" name)
                old.passthru.dependencies;
            };
          });
        };
      };

      # Compose the Python package set by merging necessary overlays
      pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
        inherit python;
      }).overrideScope (lib.composeManyExtensions [
        pyproject-build-systems.overlays.default
        overlay
        pyprojectOverrides
      ]);

      # Create a virtual environment containing all dependencies (development mode includes optional deps)
      virtualenv =
        (pythonSet.mkVirtualEnv "dev-env" workspace.deps.all).overrideAttrs
        (old: {
          # You could also ignore all collisions with:
          venvIgnoreCollisions = [ "*" ];

        });
    in {
      # The devShell is all you need for interactive work
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [ virtualenv pkgs.uv ];
        env = {
          # Prevent uv from auto-syncing the environment
          UV_NO_SYNC = "1";
          # Force uv to use the Python interpreter from our virtualenv
          UV_PYTHON = "${virtualenv}/bin/python";
          # Disable uv from downloading prebuilt pythons
          UV_PYTHON_DOWNLOADS = "never";
          # Force QT to use X11/XWayland
          QT_QPA_PLATFORM = "xcb";
        };
        shellHook = ''
          # Clear PYTHONPATH to avoid conflicts with Nixpkgs Python
          unset PYTHONPATH
          # Set repository root for editable mode (if needed)
          export REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo .)
        '';
      };
    };
}
