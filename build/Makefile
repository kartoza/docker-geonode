
.PHONY: bootstrap overlay clean-overlay generate build clean-build

bootstrap:	
	prepare_deps.sh || bootstrap/scripts/prepare_deps.sh || build/bootstrap/scripts/prepare_deps.sh
	nix-shell --run 'bash initial_bootstrap.sh || bash bootstrap/scripts/initial_bootstrap.sh || bash build/bootstrap/scripts/initial_bootstrap.sh' shell.nix

overlay:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) overlay

clean-overlay:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) clean-overlay

generate:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) generate

build:
	cd $(BUILD_DIRECTORY) && ./build.sh

