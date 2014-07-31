Coveralls-merge
---------------

Get coverage data on Python C extensions, on both the python side and
the C side of the api.  The package combines the output from 
coverage-lcov_ and coveralls_ to upload your coverage data to 
`coveralls.io`_. 

.. _coverage-lcov: https://github.com/okkez/coveralls-lcov
.. _coveralls: https://github.com/coagulant/coveralls-python
.. _`coveralls.io`: https://coveralls.io

This only supports `travis-ci`_.

.. _`travis-ci`: https://travis-ci.org

Usage
-----

Setup coveralls, and make sure that it's working with coveralls.io for
the python portion. Then, to add c coverage, add a few lines to your
.travis.yml::

    python:
      - 2.7

    install:
        # install lcov
      - "sudo apt-get -qq install lcov"
        # install test runners, coveralls, and coveralls-merge
      - "pip install coveralls nose coveralls-merge"
        # install the lcov parser
      - "gem install coveralls-lcov"

    script:
      - coverage erase
      - python setup.py clean
      # build, using coverage flag
      - CFLAGS="-coverage" python setup.py build_ext --inplace

      # run your tests, with coverage as normal
      - coverage run -m nose Tests/test_*.py

    after_success:
      # combine and generate json
      - lcov --capture --directory . -b . --output-file coverage.info
      - coveralls-lcov -v -n coverage.info > coverage.c.json

      # upload
      - coveralls-merge coverage.c.json
    


