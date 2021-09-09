.PHONY: test dist publish

check: fmt mypy test

fmt:
	black -t py36 ibmcloud_iam

mypy:
	mypy --show-error-codes ibmcloud_iam

test:
	python -m unittest discover -v tests

dist:
	python setup.py sdist bdist_wheel


publish: dist
	pip install 'twine>=1.5.0'
	twine upload --repository ibmcloud_iam --skip-existing dist/*
	rm -fr build dist .egg *.egg-info
