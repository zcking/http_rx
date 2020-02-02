.PHONY: dist push-pypi clean set-version

HOST_PYTHON=/usr/bin/python3

clean:
	rm -rf dist

run:
	python main.py

dist:
	${HOST_PYTHON} setup.py sdist bdist_wheel

push-pypi:
	${HOST_PYTHON} -m twine upload dist/*

set-version:
	sed -i -E "s/version='.*',/version='${VERSION}',/" setup.py

