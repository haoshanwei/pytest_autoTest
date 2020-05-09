all: echo_env
	@echo "do nothing"

clean:
	@echo "=========clean files========="
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr *.egg-info build dist

build: clean
	@echo "=========build wheel package========="
	python setup.py build_py bdist_wheel
	cp Makefile dist

uninstall:
	@echo "=========uninstall dapiauto========="
	pip uninstall -y dapiauto

publish: clean
	@echo "=========publish wheel package========="
	python setup.py build_py bdist_wheel upload -r daling
	# pip install dist/*.whl -U
local: clean
	@echo "=========local wheel package========="
	python setup.py build_py bdist_wheel upload -r daling
	@echo "=========local install wheel package========="
	pip install dist/*.whl -U

.PHONY : echo_env all clean build_egg install_egg local_install build install uninstall publish publish_whl release-major release-minor release-patch
