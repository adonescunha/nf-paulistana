#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from pyvows import Vows, expect
from mock import Mock, MagicMock

from nf_paulistana.registries.registry import Registry, RegistryBase
from nf_paulistana.registries.fields import Field


@Vows.batch
class RegistryBaseVows(Vows.Context):

    class AddToClass(Vows.Context):

        class WhenValueIsAField(Vows.Context):

            def topic(self):
                class RegistryClass(object):

                    __metaclass__ = RegistryBase

                field = Mock()
                field.attach_to_field = Mock()
                field_name = 'field'
                RegistryClass.add_to_class(field_name, field)

                return RegistryClass, field_name, field

            def it_attachs_field_to_registry(self, topic):
                registry_class, _, field = topic
                field.attach_to_field.assert_with(registry_class)

        class WhenValueIsNotAField(Vows.Context):

            def topic(self):
                class RegistryClass(object):

                    __metaclass__ = RegistryBase

                name = 'a'
                value = 'ANYVALUE'
                RegistryClass.add_to_class(name, value)

                return RegistryClass, name, value

            def it_assigns_value_as_class_attribute(self, topic):
                registry_class, name, value = topic
                expect(getattr(registry_class, name)).to_equal(value)

    class AddField(Vows.Context):

        def topic(self):
            class RegistryClass(object):

                __metaclass__ = RegistryBase

                fields = {}

            field = Mock(attribute_name='field_attribute')
            RegistryClass.add_field(field)

            return RegistryClass, field

        def it_adds_field_to_fields_list(self, topic):
            registry_class, field = topic
            expect(registry_class.fields.values()).to_include(field)


@Vows.batch
class RegistryVows(Vows.Context):

    class WhenInitialized(Vows.Context):

        class WithValidKwargs(Vows.Context):

            def topic(self):
                class RegistryClass(Registry):

                    field1 = Field(length=20)
                    field2 = Field(length=20)

                kwargs = {
                    'field1': 'FIELD 1',
                    'field2': 'FIELD 2'
                }
                registry = RegistryClass(**kwargs)

                for attribute, value in kwargs.iteritems():
                    yield registry, attribute, value

            def it_assigns_attribute_values(self, topic):
                registry, attribute, value = topic
                expect(getattr(registry, attribute)).to_equal(value)

        class WithNonFieldKwargs(Vows.Context):

            def topic(self):
                class RegistryClass(Registry):

                    field1 = Field(length=20)

                RegistryClass(field3=20)

            def it_raises_type_error(self, topic):
                expect(topic).to_be_an_error_like(TypeError)

        class GetOrderedFields(Vows.Context):

            def topic(self):
                field1 = Field(length=20, order=2)
                field2 = Field(length=20, order=1)

                class RegistryClass(Registry):

                    registry_field1 = field1
                    registry_field2 = field2

                registry = RegistryClass()

                return registry.get_ordered_fields(), (field2, field1)


            def it_returns_fields_in_correct_order(self, topic):
                expected_set, actual_set = topic

                for expected, actual in zip(expected_set, actual_set):
                    expect(actual).to_equal(expected)

        class AsRegistry(Vows.Context):

            def topic(self):
                class RegistryClass(Registry):

                    registry_field1 = Field(length=5, order=1, default='MANGA')
                    registry_field2 = Field(length=10, order=2, default=10)

                return  'MANGA10        \r\n', RegistryClass().as_registry()


            def it_concatenates_fields_registry_representation(self, topic):
                expected, actual = topic
                expect(expected).to_equal(actual)
