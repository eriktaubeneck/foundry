import os
from contextlib import contextmanager
from io import StringIO
from copy import deepcopy


def fake_file_factory(fudged_files):
    @contextmanager
    def fake_file(filename, method='r'):
        content = fudged_files.get(
            os.path.relpath(
                filename,
                os.path.join(os.getcwd(), 'foundry', 'data')),
            u'')

        yield StringIO(content)
    return fake_file

fudged_data_files = {
    u'planet.yml': u"""
earth:
    id: 1
    name: Earth
    """,
    u'crew.yml': u"""
fry:
    id: 1
    name: 'philip j. fry'
    birthday: '1974-08-14'
    role: 'delivery boy'
    salary: '10000.00'
    foundry_relation_planet: 'earth'

leela:
    id: 2
    name: 'turanga leela'
    birthday: '2974-12-03'
    role: 'captain'
    salary: '80000.00'

bender:
    id: 3
    name: 'bender bending rodr\xc3guez, sr.'
    birthday: '2996-01-01'
    role: 'bending unit'
    salary: '50000.00'

farnsworth:
    id: 4
    name: 'hubert j. farnsworth'
    birthday: '2841-04-09'
    role: 'the professor'
    salary: '1000000.00'

hermes:
    id: 5
    name: 'hermes conrad'
    birthday: '2959-07-15'
    role: 'bureaucrat'
    salary: '120000.00'

zoidberg:
    id: 6
    name: 'john a. zoidberg'
    birthday: '2875-05-05'
    role: 'doctor'
    salary: '0.99'

amy:
    id: 7
    name: 'amy wong'
    birthday: '2978-05-05'
    role: 'intern'
    salary: '0.00'
""",
    u'ship.yml': u"""
planet-express-ship:
    id: 1
    name: 'planet express ship'
    call_sign: '7ACV15'
    purchased_at: '2985-01-01'
    warranty_expires_at: '2995-01-01'
    last_serviced_at: '3014-10-6'
    foundry_relation_crew: ['fry', 'bender', 'leela']
"""}

fudged_copied_data_files = deepcopy(fudged_data_files)
fudged_copied_data_files.update({
    u'ship.yml': u"""
- foo
- bar
- baz
"""})

fudged_bad_yaml_data_files = deepcopy(fudged_data_files)
fudged_bad_yaml_data_files.update({
    u'ship.yml': u"""
planet-express-ship:
    id: 1
    name: 'planet express ship'
    call_sign = '7ACV15'
"""
})
