
.PHONY: bootstrap overlay clean-overlay generate build clean-build

bootstrap:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) bootstrap

overlay:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) overlay

clean-overlay:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) clean-overlay

generate:
	cd $(BOOTSTRAP_DIRECTORY) && $(MAKE) generate

build:
	cd $(BUILD_DIRECTORY) && ./build.sh

