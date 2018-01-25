#!/usr/bin/env python

## Merge coveralls-python coverage with the output of other json based
## coveralls parsers. (e.g. lcov)

## (c) Eric Soroos 2014-2018

## This file is released under the MIT license -- see LICENSE.txt for
## more details.

from __future__ import print_function

import json
import requests
import coveralls
import sys
import os

API_URL = 'https://coveralls.io/api/v1/jobs'

class merger(object):

    def __init__(self, files, debug=None, strip=None):
        self.merged = {}
        self.files = files
        self.debug = debug
        self.strip = strip

        f = os.path.dirname
        if '.egg' in __file__:
            self.prefix = f(f(f(__file__))) + '/'
        else:
            self.prefix = f(f(__file__)) + '/'


    def parse(self, path):
        #
        # :param path: path to json file
        # :returns: json object
        # :raises NotFound: file not found
        # :raises JsonException: invalid json

        with open(path,'r') as src:
            return json.loads(src.read())

    def strip_one(self, path):
        path = path.replace(self.prefix, '')
        elts = path.split('/')
        if '.egg' in elts[0]:
            path = path.replace(elts[0] + '/', '')
        return path

    def strip_path(self, data):
        if not self.strip: return data

        # structure: data['source_files'][0].keys()=['source', 'name', 'coverage']
        ret = dict((k,v) for k,v in data.items() if k != 'source_files')
        ret['source_files'] = [{'source':f['source'],
                                'coverage':f['coverage'],
                                'name': self.strip_one(f['name'])}
                               for f in data['source_files']]
        return ret

    def merge(self, data):
        if not self.merged:
            self.merged = dict(data.items())
            self.merged['source_files'] = [];

        self.merged['source_files'].extend(data.get('source_files',[]))


    def collect(self):
        coverall = coveralls.Coveralls()
        self.merge(self.strip_path(coverall.create_data()))

        for f in self.files:
            self.merge(self.strip_path(self.parse(f)))

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
        -s --strip: Strip prefixes from packages installed in site-packages.

        """)
        return 1

    debug = False or '-d' in sys.argv[1:] or '--debug' in sys.argv[:1]
    files = [f for f in sys.argv[1:] if not f.startswith('-')]
    strip = False or '-s' in sys.argv[1:] or '--strip' in sys.argv[:1]

    m = merger(files, debug, strip)
    m.collect()
    print(m.report())
    return 0

if __name__ == '__main__':
    sys.exit(main())
