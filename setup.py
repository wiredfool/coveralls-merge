import sys
from setuptools import setup

setup(
    name='coveralls-merge',
    version='0.0.2',
    packages=['coveralls_merge'],
    url='http://github.com/wiredfool/coveralls-merge',
    license='MIT',
    author='Eric Soroos',
    author_email='eric@soroos.net',
    description='Upload coverage for C extensions to coveralls.io ',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    entry_points={
        'console_scripts': [
            'coveralls-merge = coveralls_merge.core:main',
        ],
    },
    install_requires=['coveralls>=0.4.2', 'requests>=1.0.0'],
    zip_safe=False,
    keywords=['Testing', 'Coverage', 'Coveralls.io', 'Travis-ci.org'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
