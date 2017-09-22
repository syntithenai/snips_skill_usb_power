test:
	python3 setup.py test

format:
	pip3 install pycodestyle
	pip3 install autopep8
	autopep8 --in-place --recursive --exclude='src,temp' .
	pycodestyle --exclude='src,temp' .

install:
	@make clean
	python3 setup.py install --user
	python3 setup.py develop --user

pypi:
	@make install
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*

clean:
	rm -fr build
	rm -fr dist
	rm -fr *.egg-info
	rm -fr **/*.pyc
