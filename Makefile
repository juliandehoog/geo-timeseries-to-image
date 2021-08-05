clean:
	rm -f dist/*

deploy: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

local-install: local-uninstall
	python setup.py develop --user

local-uninstall:
	python setup.py develop --uninstall --user
