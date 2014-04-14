#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from decimal import Decimal


class DefaultLengthMixin(object):

    def __init__(self, **kwargs):
        if not kwargs.has_key('length'):
            kwargs['length'] = self.length

        Field.__init__(self, **kwargs)


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
    def empty_value(self):
        return ''

    @property
    def value_str(self):
        value_str = self.value and self.process_value() or self.empty_value
        length = self.length

        return value_str[:length]

    def process_value(self):
        return unicode(self.value)

    def as_registry(self):
        value_str = self.value_str

        return value_str + ' ' * (self.length - len(value_str))

    def attach_to_registry(self, name, cls):
        self.registry = cls
        self.attribute_name = name
        cls.add_field(self)


class DateField(DefaultLengthMixin, Field):

    length = 8

    def process_value(self):
        return self.value.strftime('%Y%m%d')


class NumericField(Field):

    @property
    def empty_value(self):
        return '0' * self.length

    def get_numeric_value_as_string(self):
        return str(self.value)

    def process_value(self):
        numeric_str = self.get_numeric_value_as_string()

        return '0' * (self.length - len(numeric_str)) + numeric_str


class DecimalField(DefaultLengthMixin, NumericField):

    length = 15

    @property
    def default(self):
        return Decimal('0')

    @default.setter
    def default(self, value):
        pass

    def get_numeric_value_as_string(self):
        return ('%.2f' % self.value).replace('.', '')


class TextField(DefaultLengthMixin, Field):

    length = 0

    @property
    def value_str(self):
        return self.value and self.process_value() or self.empty_value

    def process_value(self):
        return '|'.join(self.value.splitlines())


class RegistryField(DefaultLengthMixin, Field):

    length = 0

    @property
    def value_str(self):
        return ''.join(self.value.as_registry().splitlines())
