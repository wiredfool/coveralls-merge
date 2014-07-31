#!/usr/bin/env python

## Merge coveralls-python coverage with the output of other json based
## coveralls parsers. (e.g. lcov)

## (c) Eric Soroos 2014

## This file is released under the MIT license -- see LICENSE.txt for
## more details.

from __future__ import print_function

import json
import requests
import coveralls 
import sys


API_URL = 'https://coveralls.io/api/v1/jobs'

class merger(object):

    def __init__(self, files, debug=None):
        self.merged = {}
        self.files = files
        self.debug = debug

    def parse(self, path):
        #
        # :param path: path to json file
        # :returns: json object
        # :raises NotFound: file not found
        # :raises JsonException: invalid json
        
        with open(path,'r') as src:
            return json.loads(src.read())
        
    def merge(self, data):
        if not self.merged:
            self.merged = dict(data.items())
            self.merged['source_files'] = [];
            
        self.merged['source_files'].extend(data.get('source_files',[]))


    def collect(self):
        coverall = coveralls.Coveralls()
        self.merge(coverall.create_data())

        for f in self.files:
            self.merge(self.parse(f))

    def report(self):
        print("Reporting on files:", file=sys.stderr)
        print("\n".join(s['name'] for s in self.merged['source_files']), file=sys.stderr)

        if self.debug:
            del(self.merged['source_files'])
            return json.dumps(self.merged, indent=2)
        else:
            response = requests.post(API_URL, files={'json_file': json.dumps(self.merged)})
            response.raise_for_status()
            return response.json()

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("""
        Usage:

        coveralls-merge [-h|--help] [-d|--debug] filename.json [filename2.json ...]

        -h --help: This message
        -d --debug: Print the response, don't upload to coveralls.io
        filename.json: The files that you wish to combine with the python
                       coveralls data.

        """)
        return 1
    
    debug = False or '-d' in sys.argv[1:] or '--debug' in sys.argv[:1]
    files = [f for f in sys.argv[1:] if not f.startswith('-')]

    m = merger(files, debug)
    m.collect()
    print(m.report())
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
