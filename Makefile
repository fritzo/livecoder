test: FORCE
	pyflakes .
	pep8 .
	py.test

FORCE:
