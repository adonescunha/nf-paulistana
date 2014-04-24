#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from decimal import Decimal

from .registries import *


class Lote(object):

    def __init__(self, inscricao_municipal, data_inicio, data_fim):
        if data_inicio > data_fim:
            raise TypeError(u'A data de início do período do lote deve ser ' +\
                'anterior a data de fim')

        self.inscricao_municipal = inscricao_municipal
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.rps_set = []

    def append(self, rps):
        self.rps_set.append(rps)

    def build_cabecalho_registry(self):
        return Cabecalho(
            inscricao_municipal=self.inscricao_municipal,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim
        )

    def build_rodape_registry(self):
        return Rodape(
            numero_linhas=len(self.rps_set),
            total_servicos=self.calculate_total_servicos(),
            total_deducoes=self.calculate_total_deducoes()
        )

    def reduce_rps_set(self, attribute_name):
        return reduce(lambda x, y: x + getattr(y, attribute_name), self.rps_set,
            Decimal('0.00'))

    def calculate_total_servicos(self):
        return self.reduce_rps_set('valor_servicos')

    def calculate_total_deducoes(self):
        return self.reduce_rps_set('valor_deducoes')

    def as_text(self):
        return (self.build_cabecalho_registry().as_registry() +\
            reduce(lambda x, y: x + y.as_registry(), self.rps_set, '') +\
                self.build_rodape_registry().as_registry())\
                    .encode('iso-8859-1', 'ignore')
