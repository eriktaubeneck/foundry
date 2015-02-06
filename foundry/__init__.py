import os
import sys
import yaml


def is_str_or_unicode(s):
    if sys.version_info[0] < 3:
        return isinstance(s, basestring)
    else:
        return isinstance(s, str)


def _unicode(s):
    if sys.version_info[0] < 3:
        return unicode(s)
    else:
        return s


class Mold(object):
    def __init__(self, filename, model, base_path=None, relation_key=None,
                 custom_id_gen=None, str_converters=None):
        self.filename = filename
        self.model = model
        self.base_path = base_path
        self.relation_key = relation_key
        self.custom_id_gen = custom_id_gen or (lambda x: x)
        self.str_converters = str_converters or {}

    def init_foundry(self, foundry):
        self.foundry = foundry
        if not self.base_path:
            self.base_path = foundry.path
        if not self.relation_key:
            self.relation_key = foundry.relation_key
        if not self.custom_id_gen:
            self.custom_id_gen = foundry.custom_id_gen

    @property
    def file_path(self):
        if self.base_path:
            return os.path.join(self.base_path, self.filename)

    def load(self):
        data = self._load_yaml()
        if not data:
            raise TypeError(u'YAML file {} did not load.  Please '
                            u'check that it has data.'.format(
                                self.file_path))

        if not isinstance(data, dict):
            raise TypeError(u'YAML file {} did not load as a dict.  Please '
                            u'check its formatting.'.format(
                                self.file_path))

        for fixture_name, fixture_data in data.items():
            fixture_data.update(
                {attr.replace(self.relation_key+'_', ''):
                 self.foundry.load_relation(value)
                 for attr, value in fixture_data.items()
                 if attr.startswith(self.relation_key)}
            )
            relation_attrs = [f for f in fixture_data if
                              f.startswith(self.relation_key)]
            for attr in relation_attrs:
                del fixture_data[attr]

            for attr, str_converter in self.str_converters.items():
                if attr in fixture_data:
                    fixture_data[attr] = str_converter(fixture_data[attr])

            obj = self.model(**fixture_data)
            obj.id = self.custom_id_gen(getattr(obj, 'id', None))
            self.foundry.create(fixture_name, obj)

    def _load_yaml(self):
        try:
            with open(self.file_path) as f:
                return yaml.load(f)
        except IOError:
            pass


class Foundry(object):
    def __init__(self, molds, relation_key=None, path=None,
                 custom_id_gen=None):
        self.relation_key = relation_key or 'foundry_relation'
        self.path = path or os.path.join(os.getcwd(), 'foundry', 'data')
        self.custom_id_gen = custom_id_gen
        self.molds = [mold if isinstance(mold, Mold) else
                      Mold(mold[0], mold[1])
                      for mold in molds]
        [mold.init_foundry(self) for mold in self.molds]
        self.fixtures = {}
        self.staged_fixtures = {}
        self.model_lookup = {mold.model.__name__: mold.model
                             for mold in self.molds}

    def load(self):
        for mold in self.molds:
            mold.load()
        self.commit()
        self.make_fixtures()

    def load_relation(self, value):
        if isinstance(value, list):
            return [self.staged_fixtures[v] for v in value]
        else:
            return self.staged_fixtures[value]

    def __getitem__(self, fixture_name):
        if not self.fixtures:
            self.load_cached_fixtures()

        model_name, _id = self.fixtures.get(fixture_name, (None, None))
        if not (model_name and _id):
            raise KeyError('Fixture {} was not found.'.format(fixture_name))
        obj = self.query(self.model_lookup[model_name], _id)
        if not obj:
            raise KeyError(
                'Fixture {} not found in datastore.'.format(fixture_name))
        return obj

    def create(self, fixture_name, obj):
        if fixture_name in self.staged_fixtures.keys():
            raise Exception('Cannot load two fixtures with same fixture name.')
        self.staged_fixtures[fixture_name] = obj
        self.queue(obj)

    def queue(self, obj):
        raise NotImplemented(
            'Must use or implement a subclass of Foundry that defines a method'
            ' `queue` which queues an object to be commited to the data store.'
        )

    def commit(self):
        raise NotImplemented(
            'Must user or implement a subclass of Foudry that defines a method'
            ' `commit` which commits the queued data to the data store.'
        )

    def query(self, model, _id):
        raise NotImplemented(
            'Must user or implement a subclass of Foudry that defines a method'
            ' `query` which retriees data from the data store by model and id.'
        )

    def make_fixtures(self):
        self.fixtures = {fixture_name: (type(obj).__name__, obj.id)
                         for fixture_name, obj in
                         self.staged_fixtures.items()}
        with open(os.path.join(self.path, '.foundry_ids'), 'w') as f:
            f.write(_unicode(yaml.dump(self.fixtures)))

    def load_cached_fixtures(self):
        try:
            with open(os.path.join(self.path, '.foundry_ids')) as f:
                self.fixtures = yaml.load(f)
        except IOError:
            raise IOError(
                'No stashed .foundry_ids file found. Please (re)poulate.')



class DictFoundry(Foundry):
    def __init__(self, *args, **kwargs):
        super(DictFoundry, self).__init__(*args, **kwargs)
        self.store = {}

    def queue(self, obj):
        self.store[(type(obj), obj.id)] = obj

    def commit(self):
        pass

    def query(self, model, _id):
        return self.store[model, _id]


class SQLAlchemyFoundry(Foundry):
    def __init__(self, session, *args, **kwargs):
        super(SQLAlchemyFoundry, self).__init__(*args, **kwargs)
        self.session = session

    def queue(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()

    def query(self, model, _id):
        return self.session.query(model).get(_id)
