.PHONY: dist push-pypi

HOST_PYTHON=/usr/bin/python3

dist:
	${HOST_PYTHON} setup.py sdist bdist_wheel

push-pypi:
	${HOST_PYTHON} -m twine upload dist/*

