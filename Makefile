deploy:
	python setup.py sdist
	twine upload dist/*

local-install: local-uninstall
	python setup.py develop --user

local-uninstall:
	python setup.py develop --uninstall --user
