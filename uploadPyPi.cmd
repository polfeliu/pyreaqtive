:: https://realpython.com/pypi-publish-python-package/#versioning-your-package
:: https://packaging.python.org/tutorials/packaging-projects/
rmdir /s /q "dist"
rmdir /s /q "build"

pipenv run python setup.py sdist bdist_wheel


python -m pip install --upgrade twine
python -m twine check dist/*
python -m twine upload --repository pypi dist/*