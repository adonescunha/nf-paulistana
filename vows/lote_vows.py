#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


import datetime
from pyvows import Vows, expect

from nf_paulistana.lote import Lote

today = datetime.date(2014, 2, 20)

VALID_LOTE_KWARGS = (
    ('inscricao_municipal', '99999999'),
    ('data_inicial', today - datetime.timedelta(days=3)),
    ('data_final', today)
)

@Vows.batch
class LoteVows(Vows.Context):

    class WhenInitialized(Vows.Context):

        class ItAssigns(Vows.Context):
            def topic(self):
                kwargs = VALID_LOTE_KWARGS
                lote = Lote(**dict(kwargs))

                for attribute, value in kwargs:
                    yield (lote, attribute, value)

            def it_assigns_attribute(self, topic):
                lote, attribute, value = topic
                expect(getattr(lote, attribute)).to_equal(value)

        class WithDataInicialGreaterThanDataFinal(Vows.Context):

            def topic(self):
                kwargs = (
                    ('inscricao_municipal', '99999999'),
                    ('data_inicial', today + datetime.timedelta(days=3)),
                    ('data_final', today)
                )

                return Lote(**dict(kwargs))

            def it_raises_a_type_error(self, topic):
                expect(topic).to_be_an_error_like(TypeError)

    class HeaderRegistry(Vows.Context):

        def topic(self):
            lote = Lote(**dict(VALID_LOTE_KWARGS))

            return lote.header_registry()

        def returns_a_valid_registry(self, topic):
            expect(topic).to_equal('1001999999992014021720140220')
