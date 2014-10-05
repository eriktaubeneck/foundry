# Foundry

[![Build Status](https://travis-ci.org/eriktaubeneck/foundry.svg?branch=master)](https://travis-ci.org/eriktaubeneck/foundry)
[![Coverage Status](https://img.shields.io/coveralls/eriktaubeneck/foundry.svg)](https://coveralls.io/r/eriktaubeneck/foundry)
[![Latest Version](https://pypip.in/version/foundry/badge.png)](https://pypi.python.org/pypi/foundry/)
[![Downloads](https://pypip.in/download/foundry/badge.png)](https://pypi.python.org/pypi/foundry/)
[![License](https://pypip.in/license/foundry/badge.png)](https://pypi.python.org/pypi/foundry/)

Often times, when building an application, it is handy to create some seed data with which to use and test how parts of your application will work. When this dataset is small, a python script works just fine, but as that data set (and number of different data models) grow, this approach becomes quite cumbersome.

Foundry is an tool designed to make this easier, by allowing you to orgainze this data in a data friendly format, YAML. All data that is imported is defined by a key in the YAML file, and Foundry acts as a proxy to fetch these objects for you from the datastore. This also allows the user to specify relations by referencing these keys to other objects.

![Gussmetallschmelze](http://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gussmetallschmelze.jpg/640px-Gussmetallschmelze.jpg)

## Installation

Inside a [virtualenv](http://virtualenv.readthedocs.org/en/latest/) run

```
pip install foundry
```

## Quickstart

```
from foundry import Foundry
from models import Crew, Ship
foundry = Foundry([('crew.yml', Crew), ('ship.yml', Ship)])
foundry.load()

zoidberg = foundry['zoidberg']
```

Then, in your app root path, create a directory `foundry/data` and create the two files `crew.yml` and `ship.yml`. See the tests for a more thorough example.



## TODO

 - Add an Example to README.md
 - Expand support for other backend datastores


## Contributing

If anything on the TODO list looks like something you'd like to take on, go
ahead and fork the project and submit a Pull Request. For other features,
please first open an issue proposing the feature/change.

### Environment

To hack on foundry, make sure to install the development requirements in your
virtual environment.

`pip install -r dev_requirements.txt`

### Tests

Pull Requests should include tests covering the changes/features being
proposed.  To run the test suite, simply run:

`nosetests`

#LICENSE
MIT License

Copyright (C) 2014 by Erik Taubeneck

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
