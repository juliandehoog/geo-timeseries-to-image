deploy:
	python setup.py sdist bdist_wheel && python -m twine upload dist/*

local-install: local-uninstall
	python setup.py develop --user

local-uninstall:
	python setup.py develop --uninstall --user
