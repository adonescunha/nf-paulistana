#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


class Lote(object):

    def __init__(self, inscricao_municipal, data_inicial, data_final):
        if data_inicial > data_final:
            raise TypeError(u'A data de início do período do lote deve ser ' +\
                'anterior a data de fim')

        self.inscricao_municipal = inscricao_municipal
        self.data_inicial = data_inicial
        self.data_final = data_final

    def header_registry(self):
        date_format = '%Y%m%d'
        return '1001%s%s%s' % (self.inscricao_municipal,
                self.data_inicial.strftime(date_format),
                    self.data_final.strftime(date_format))
