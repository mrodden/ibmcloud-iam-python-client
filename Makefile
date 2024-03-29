.PHONY: test dist publish

check: fmt mypy test

fmt:
	black -t py36 ibmcloud_iam tests example.py

mypy:
	mypy --show-error-codes --config-file mypy.ini ibmcloud_iam tests example.py

test:
	python -m unittest discover -v tests

dist:
	python setup.py sdist bdist_wheel


publish: dist
	pip install 'twine>=1.5.0'
	twine upload --repository ibmcloud_iam --skip-existing dist/*
	rm -fr build dist .egg *.egg-info
