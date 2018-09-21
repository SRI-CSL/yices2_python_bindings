#iam's makefile; maybe migrate some targets to the main Makefile when done.

all: help


help:
	@echo ''
	@echo 'Here are the targets:'
	@echo ''
	@echo 'To test                :    "make check"'
	@echo 'To develop             :    "make develop"'
	@echo 'To install             :    "make install"'
	@echo 'To publish             :    "make publish"'
	@echo 'To pylint (errors)     :    "make lint"'
	@echo 'To pylint (all)        :    "make lint_all"'
	@echo ''



check:
	pytest test_api test


#local editable install for developing
develop:
	pip install -e .

iam:
	python -m pip install -e .

dist: clean
	python setup.py bdist_wheel

# If you need to push this project again,
# INCREASE the version number in yices/version.py,
# otherwise the server will give you an error.

publish: dist
	python setup.py sdist upload

install:
	pip install

clean:
	rm -rf  *.pyc *~ __pycache__ */*.pyc */*~ */__pycache__ */*/*.pyc */*/*~ */*/__pycache__



PYLINT = $(shell which pylint)


check_lint:
ifeq ($(PYLINT),)
	$(error lint target requires pylint)
endif


lint: check_lint
# for detecting just errors:
	@ $(PYLINT) -E  yices_api.py yices/*.py test/*.py examples/sudoku/sudoku.py

lint_all: check_lint
# for detecting more than just errors:
	@ $(PYLINT) --disable=missing-docstring --disable=global-statement --disable=duplicate-code --rcfile=.pylintrc yices_api.py yices/*.py examples/sudoku/*.py

.PHONY: test lint lint check_lint
