#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


class RegistryBase(type):

    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        new_class = super(RegistryBase, cls).__new__(cls, name, bases,
            {'__module__': module})

        new_class.fields = {}

        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'attach_to_registry'):
            value.attach_to_registry(name, cls)
            setattr(cls, name, value.default)
        else:
            setattr(cls, name, value)

    def add_field(cls, field):
        cls.fields[field.attribute_name] = field


class Registry(object):

    __metaclass__ = RegistryBase

    def __init__(self, *args, **kwargs):
        fields_keys = self.fields.keys()

        for field, value in kwargs.iteritems():
            if field not in fields_keys:
                raise TypeError

            setattr(self, field, value)

    def get_ordered_fields(self):
        return sorted(self.fields.values(),
            cmp=lambda x, y: cmp(x.order, y.order))

    def as_registry(self):
        result = ''

        for f in self.get_ordered_fields():
            f.value = getattr(self, f.attribute_name)
            result = result + f.as_registry()

        return result + '\n\r'
