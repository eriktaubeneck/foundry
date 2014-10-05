import sys
import unittest
import fudge
from yaml.scanner import ScannerError
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.declarative import declarative_base
from tests.models import models_factory
from tests.fudged_files import (
    fake_file_factory, fudged_data_files, fudged_copied_data_files,
    fudged_bad_yaml_data_files)

from foundry import Mold, DictFoundry

if sys.version_info[0] < 3:
    open_function_string = '__builtin__.open'
else:
    open_function_string = 'builtins.open'


class FoundryTestCase(unittest.TestCase):
    def setUp(self):
        self.Crew, self.Ship = models_factory(declarative_base())
        crew_converters = {
            'birthday': lambda s: datetime.strptime(s, '%Y-%m-%d'),
            'salary': lambda s: Decimal(s)
        }
        self.foundry = DictFoundry(
            [Mold('crew.yml', self.Crew, str_converters=crew_converters),
             ('ship.yml', self.Ship)]
        )

    @fudge.patch(open_function_string)
    def test_foundry_default(self, fudged_open):
        fudged_open.is_callable().calls(fake_file_factory(fudged_data_files))
        self.foundry.load()
        fry = self.foundry['fry']
        self.assertIsInstance(fry, self.Crew)
        self.assertEqual(fry.id, 1)
        self.assertEqual(fry.name, u'philip j. fry')
        self.assertEqual(fry.birthday, datetime(1974, 8, 14))
        self.assertEqual(fry.salary, Decimal('10000.00'))
        for k in ('leela', 'bender', 'farnsworth', 'hermes', 'zoidberg', 'amy'):
            self.assertIsInstance(self.foundry[k], self.Crew)

        planet_express_ship = self.foundry['planet-express-ship']
        self.assertIsInstance(planet_express_ship, self.Ship)
        for k in ('fry', 'leela', 'bender'):
            self.assertIn(self.foundry[k], planet_express_ship.crew)
            self.assertEqual(self.foundry[k].ship, planet_express_ship)

    @fudge.patch(open_function_string)
    def test_foundry_copied_local_settings(self, fudged_open):
        fudged_open.is_callable().calls(fake_file_factory(
            fudged_copied_data_files))
        with self.assertRaises(TypeError):
            self.foundry.load()

    @fudge.patch(open_function_string)
    def test_foundry_bad_yaml_local_settings(self, fudged_open):
        fudged_open.is_callable().calls(fake_file_factory(
            fudged_bad_yaml_data_files))
        with self.assertRaises(ScannerError):
            self.foundry.load()
