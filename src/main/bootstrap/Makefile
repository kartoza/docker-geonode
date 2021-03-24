
.PHONY: bootstrap clean-overlay overlay generate test phase-test setup

bootstrap:
	prepare_deps.sh || scripts/prepare_deps.sh
	direnv exec . nix-shell '--run' 'python -m bootstrap $${OVERLAY_DIRECTORY} $${BUILD_DIRECTORY} $${BOOTSTRAP_DIRECTORY} $${PROJECT_ROOT}'

clean-overlay:
	rm -rf $${BUILD_DIRECTORY}
	make overlay

overlay:
	overlay.py $${OVERLAY_DIRECTORY} $${BUILD_DIRECTORY}

generate:
	generate.py ${OVERLAY_DIRECTORY} ${BUILD_DIRECTORY}

test:
	python -m unittest discover -s python/bootstrap -v

phase-test:
	#cd scripts/phase-tests; python -m unittest discover -v test_phases.TestPhases.test_generate
	cd scripts/phase-tests; python -m unittest -v test_phases

setup: overlay generate
