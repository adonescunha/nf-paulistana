#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


import datetime
from pyvows import Vows, expect
from mock import Mock
from decimal import Decimal

from nf_paulistana.lote_rps.lote import Lote
from nf_paulistana.lote_rps.registries import RPS

today = datetime.date(2014, 2, 20)

VALID_LOTE_KWARGS = (
    ('inscricao_municipal', '99999999'),
    ('data_inicio', today - datetime.timedelta(days=3)),
    ('data_fim', today)
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

        class WithDataInicioGreaterThanDataFim(Vows.Context):

            def topic(self):
                kwargs = (
                    ('inscricao_municipal', '99999999'),
                    ('data_inicio', today + datetime.timedelta(days=3)),
                    ('data_fim', today)
                )

                return Lote(**dict(kwargs))

            def it_raises_a_type_error(self, topic):
                expect(topic).to_be_an_error_like(TypeError)

    class Append(Vows.Context):

        def topic(self):
            lote = Lote(**dict(VALID_LOTE_KWARGS))
            rps = Mock()
            lote.append(rps)

            return lote, rps

        def it_appends_rps_to_rps_set(self, topic):
            lote, rps = topic
            expect(lote.rps_set).to_include(rps)

    class BuildCabecalhoRegistry(Vows.Context):

        def topic(self):
            lote = Lote(**dict(VALID_LOTE_KWARGS))
            cabecalho = lote.build_cabecalho_registry()

            for attribute_name in map(lambda t: t[0], VALID_LOTE_KWARGS):
                yield lote, cabecalho, attribute_name

        def it_inherits_lote_attribute(self, topic):
            lote, cabecalho, attribute_name = topic
            expect(getattr(cabecalho, attribute_name)).to_equal(
                getattr(lote, attribute_name))

    class CalculateTotalServicos(Vows.Context):

        def topic(self):
            lote = Lote(**dict(VALID_LOTE_KWARGS))
            lote.append(RPS(valor_servicos=Decimal('32.90')))
            lote.append(RPS(valor_servicos=Decimal('36.85')))

            return Decimal('69.75'), lote.calculate_total_servicos()

        def it_sums_rps_valor_servicos(self, topic):
            expected, actual = topic

    class CalculateTotalDeducoes(Vows.Context):

        def topic(self):
            lote = Lote(**dict(VALID_LOTE_KWARGS))
            lote.append(RPS(valor_deducoes=Decimal('32.90')))
            lote.append(RPS(valor_deducoes=Decimal('36.85')))

            return Decimal('69.75'), lote.calculate_total_deducoes()

        def it_sums_rps_valor_deducoes(self, topic):
            expected, actual = topic
            expect(actual).to_equal(expected)