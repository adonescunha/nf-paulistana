#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


import datetime
from pyvows import Vows, expect
from mock import Mock
from random import randint
from decimal import Decimal

from nf_paulistana.registries.fields import (
    DefaultLengthMixin,
    Field,
    RegistryField,
    DateField,
    NumericField,
    DecimalField,
    TextField
)


FIELD_LENGTH  = 12
DEFAULT_VALUE = 'DEFAULT'
CURRENT_VALUE = 'CURRENT'


@Vows.batch
class DefaultLengthMixinVows(Vows.Context):

    def topic(self):
        expected_length = randint(1, 64)

        class FieldClass(DefaultLengthMixin, Field):

            length = expected_length

        return FieldClass, expected_length

    class WhenLengthIsNotProvided(Vows.Context):

        def topic(self, topic):
            field_class, expected_length = topic

            return field_class(), expected_length

        def it_does_not_require_length(self, topic):
            expect(topic).Not.to_be_an_error()

        def it_defaults_length_to_class_attribute_value(self, topic):
            field, expected_length = topic
            expect(field.length).to_equal(expected_length)

    class WhenLengthIsProvided(Vows.Context):

        def topic(self, topic):
            field_class, _ = topic
            expected_length = randint(65, 100)

            return field_class(length=expected_length), expected_length

        def it_assigns_length(self, topic):
            field, expected_length = topic
            expect(field.length).to_equal(expected_length)

@Vows.batch
class FieldVows(Vows.Context):

    class WhenInitialized(Vows.Context):

        def topic(self):
            return Field(length=FIELD_LENGTH), FIELD_LENGTH

        def it_assigns_length(self, topic):
            field, length = topic
            expect(field.length).to_equal(length)

        class WithoutLength(Vows.Context):

            def topic(self):
                return Field()

            def it_raises_a_type_error(self, topic):
                expect(topic).to_be_an_error_like(TypeError)

        class WithDefault(Vows.Context):

            def topic(self):
                return (Field(length=FIELD_LENGTH, default=DEFAULT_VALUE),
                    DEFAULT_VALUE)

            def it_assigns_default(self, topic):
                field, default = topic
                expect(field.default).to_equal(default)

            def it_returns_default_as_value(self, topic):
                field, default = topic
                expect(field.value).to_equal(default)

    class Value(Vows.Context):

        def topic(self):
            field = Field(length=FIELD_LENGTH)
            field.value = CURRENT_VALUE

            return field, CURRENT_VALUE

        def it_returns_its_current_value(self, topic):
            field, value = topic
            expect(field.value).to_equal(value)

    class AsRegistry(Vows.Context):

        def topic(self):
            field = Field(length=FIELD_LENGTH)
            field.value = 1

            return field, field.as_registry()

        def it_has_field_length(self, topic):
            field, registry = topic
            expect(len(registry)).to_equal(field.length)

        def it_prepends_field_value(self, topic):
            field, registry = topic
            expect(registry.startswith(str(field.value))).to_be_true()

    class ValueStr(Vows.Context):

        class WhenValueIsNone(Vows.Context):

            def topic(self):
                return Field(length=FIELD_LENGTH).value_str

            def it_returns_an_empty_string(self, topic):
                expect(topic).to_equal('')

        class WhenValueIsNotNone(Vows.Context):

            def topic(self):
                field = Field(length=FIELD_LENGTH)
                field.value = 12

                return field.value_str

            def it_returns_value_string_representation(self, topic):
                expect(topic).to_equal('12')

        class WhenValueExceedsLength(Vows.Context):

            def topic(self):
                field = Field(length=2)
                field.value = CURRENT_VALUE

                return field.value_str

            def it_truncates_value(self, topic):
                expect(topic).to_equal('CU')

    class AttachToRegistry(Vows.Context):

        def topic(self):
            field = Field(length=FIELD_LENGTH)
            registry_class = Mock()
            registry_class.add_field = Mock()
            attribute_name = 'field_attribute'
            field.attach_to_registry(attribute_name, registry_class)

            return field, attribute_name, registry_class

        def it_assigns_registry(self, topic):
            field, _, registry_class = topic
            expect(field.registry).to_equal(registry_class)

        def it_assigns_attribute_name(self, topic):
            field, attribute_name, _ = topic
            expect(field.attribute_name).to_equal(attribute_name)

        def it_add_itself_to_registry_fields(self, topic):
            field, _, registry_class = topic
            registry_class.add_field.assert_called_with(field)

@Vows.batch
class RegistryFieldVows(Vows.Context):

    class ValueStr(Vows.Context):

        def topic(self):
            field = RegistryField()
            expected_value = 'EXPECTEDVALUE'
            registry = Mock()
            registry.as_registry = Mock(return_value=expected_value + '\r\n')
            field.value = registry

            return expected_value, field.value_str

        def it_returns_value_registry_representation_without_breakline(self, topic):
            expected, actual = topic
            expect(actual).to_equal(expected)

@Vows.batch
class DateFieldVows(Vows.Context):

    class ProcessValue(Vows.Context):

        def topic(self):
            field = DateField()
            field.value = datetime.date(2014, 2, 25)

            return field.process_value()

        def it_returns_a_date_representation(self, topic):
            expect(topic).to_equal('20140225')

@Vows.batch
class NumericFieldVows(Vows.Context):

    class EmptyValue(Vows.Context):

        def topic(self):
            field = NumericField(length=10)

            return field, field.empty_value

        def its_a_zeroed_string(self, topic):
            _, empty_value = topic

            for char in empty_value:
                expect(char).to_equal('0')

        def its_length_is_the_same_as_field_length(self, topic):
            field, empty_value = topic
            expect(len(empty_value)).to_equal(field.length)

    class ProcessValue(Vows.Context):

        def topic(self):
            field = NumericField(length=10)
            field.get_numeric_value_as_string = Mock(return_value='12')

            return '0000000012', field.process_value()

        def it_returns_numeric_value_prepended_with_zeros(self, topic):
            expected, actual = topic
            expect(actual).to_equal(expected)

@Vows.batch
class DecimalFieldVows(Vows.Context):

    def topic(self):
        return DecimalField()

    def it_defaults_to_zero(self, topic):
        expect(topic.default).to_equal(Decimal('0'))

    class GetNumericValueAsString(Vows.Context):

        def topic(self):
            cases = [
                (Decimal('34.52')  ,'3452'),
                (Decimal('23.123') ,'2312'),
                (Decimal('54.2')   ,'5420'),
                (Decimal('60')     ,'6000')
            ]

            for value, expected in cases:
                field = DecimalField()
                field.value = value

                yield expected, field.get_numeric_value_as_string()

        def it_returns_a_string_without_decimal_points(self, topic):
            expected, actual = topic
            expect(actual).to_equal(expected)

@Vows.batch
class TextFieldVows(Vows.Context):

    class ProcessValue(Vows.Context):

        def topic(self):
            value = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nNam ac dolor metus'
            field = TextField()
            field.value = value

            return field.process_value(), 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.|Nam ac dolor metus'

        def it_returns_value_with_new_line_replaced_by_pipe(self, topic):
            expected, actual = topic
            expect(actual).to_equal(expected)
