#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from pyvows import Vows, expect
from mock import Mock

from nf_paulistana.registries.fields import Field, RegistryField


FIELD_LENGTH  = 12
DEFAULT_VALUE = 'DEFAULT'
CURRENT_VALUE = 'CURRENT'

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

    class WhenInitialized(Vows.Context):

        def topic(self):
            return RegistryField()

        def it_does_not_require_length(self, topic):
            expect(topic).Not.to_be_an_error()

    class ValueStr(Vows.Context):

        def topic(self):
            field = RegistryField()
            expected_value = 'EXPECTEDVALUE'
            registry = Mock()
            registry.as_registry = Mock(return_value=expected_value)
            field.value = registry

            return expected_value, field.value_str

        def it_returns_value_registry_representation(self, topic):
            print topic
            expected, actual = topic
            expect(actual).to_equal(expected)
