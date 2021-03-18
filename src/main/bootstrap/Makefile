

bootstrap:
	# In the bootstrap phase, do everything natively because we haven't
	# set up dependency manager and environment manager
	# build basic dependency and setup direnv
	nix-build --no-out-link
	# hooking direnv
	direnv allow
	# execute bootstrap script, but using direnv as entrypoint
	#direnv exec . nix-shell '--run' 'python -m bootstrap $${OVERLAY_DIRECTORY} $${BUILD_DIRECTORY} $${BOOTSTRAP_DIRECTORY} $${PROJECT_ROOT}'
	direnv exec . python '-m bootstrap' '$${OVERLAY_DIRECTORY}' '$${BUILD_DIRECTORY}' '$${BOOTSTRAP_DIRECTORY}' '$${PROJECT_ROOT}'

overlay:
	overlay.py $${OVERLAY_DIRECTORY} $${BUILD_DIRECTORY}

generate:
	generate.py ${OVERLAY_DIRECTORY} ${BUILD_DIRECTORY}

test:
	python -m unittest discover -s python/bootstrap -v
