from pathlib import Path

from osutool import __author__, __doc__, __license__, __module__, __version__
from setuptools import setup

setup(
	name=__module__,
	version=__version__,
	description=(__doc__ or '').split('\n')[0],
	long_description=Path('README.md').read_text(),
	long_description_content_type='text/markdown',
	url=f'https://github.com/{__author__}/{__module__}',
	author=__author__,
	include_package_data=True,
	license=__license__,
	packages=[__module__],
	package_data={},
	install_requires=['colorama==0.4.6'],
	setup_requires=['pytest_runner'],
	python_requires='>=3.8',
	scripts=[],
	tests_require=['pytest'],
	entry_points={'console_scripts': [f'{__module__}={__module__}:main']},
	zip_safe=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',
		'Topic :: Games/Entertainment',
		'Topic :: Utilities',
	],
)
