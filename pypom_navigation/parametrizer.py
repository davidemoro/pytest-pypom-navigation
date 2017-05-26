# -*- coding: utf-8 -*-

import json
from string import Template


class Parametrizer(object):
    """ This class let you parametrize raw_conf (json strings)
        and convert them to regular Python dictionaries.

        Matching name
        -------------

        >>> value = '{"baudrate": $baudrate_value}'
        >>> mapping = {"baudrate_value": 250, "name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"baudrate": 250}'


        With the ``json_loads`` method you'll get a parametrized regular
        Python mapping:

        >>> parametrizer.json_loads(value)
        {'baudrate': 250}

        Non matching names
        ------------------

        >>> value = '{"name": "$a_name"}'
        >>> mapping = {"name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"name": "$a_name"}'


        With the ``json_loads`` method you'll get a parametrized regular
        Python mapping:

        >>> parametrizer.json_loads(value)
        {'name': '$a_name'}

        Json not valid
        --------------

        >>> value = '{"name": $name}'
        >>> mapping = {"name": "a name"}
        >>> parametrizer = Parametrizer(mapping)

        With the ``parametrize`` method you'll get a parametrized
        string:

        >>> parametrizer.parametrize(value)
        '{"name": a name}'


        With the ``json_loads`` method you'll get a parametrized regular
        Python mapping:

        >>> parametrizer.json_loads(value)
        Traceback (most recent call last):
            ...
        json.decoder.JSONDecodeError: Expecting value: line 1 column 10 (char 9)
    """

    def __init__(self, mapping):
        self.mapping = mapping

    def parametrize(self, value):
        """ Return the value with template substitution """
        template = Template(value)
        return template.safe_substitute(**self.mapping)

    def json_loads(self, value):
        """ Return the json load of template substitution """
        parametrized = self.parametrize(value)
        return json.loads(parametrized)
