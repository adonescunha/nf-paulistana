#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


class Field(object):

    def __init__(self, length, order=0, default=None):
        self.length  = length
        self.default = default
        self.order   = order
        self._value  = None

    @property
    def value(self):
        return self._value or self.default

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def value_str(self):
        value_str = str(self.value or '')
        length = self.length

        return value_str[:length]

    def as_registry(self):
        value_str = self.value_str

        return value_str + ' ' * (self.length - len(value_str))

    def attach_to_registry(self, name, cls):
        self.registry = cls
        self.attribute_name = name
        cls.add_field(self)

class RegistryField(Field):

    def __init__(self, **kwargs):
        kwargs['length'] = 0
        super(RegistryField, self).__init__(**kwargs)

    @property
    def value_str(self):
        return self.value.as_registry()
