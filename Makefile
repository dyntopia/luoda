.PHONY: all dist install install-dev test qa

all:

install:
	pip3 install -r requirements/requirements.txt --no-binary :all:
	./setup.py install

install-dev:
	pip3 install -r requirements/requirements.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-1.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-2.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-3.txt --no-binary :all:
	./setup.py develop

test:
	python3 -m pytest

qa:
	coverage run -m pytest -v
	coverage report -m
	isort --check-only --diff --recursive .
	mypy .
	pycodestyle .
	pyflakes setup.py luoda
	pylint --output-format parseable setup.py luoda tests
	yapf --diff --recursive .
	safety check --bare --cache
	ossaudit \
		--file requirements/requirements.txt \
		--file requirements/requirements-dev-1.txt \
		--file requirements/requirements-dev-2.txt \
		--file requirements/requirements-dev-3.txt

dist:
	rm -rf dist tmp

	tag="$$(git tag --sort=-creatordate |head -n 1)" && \
	git verify-tag "$$tag" && \
	git clone --shared --branch "$$tag" . tmp

	cd tmp && \
	./setup.py sdist && \
	gpg --detach-sign --armor "$$(ls dist/*.tar.gz)"

	mv tmp/dist .
	rm -rf tmp
	gpg --verify dist/*.asc
