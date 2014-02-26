#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


import datetime
from pyvows import Vows, expect
from decimal import Decimal

from nf_paulistana.lote_rps.registries import RPS, Tomador
from nf_paulistana.lote_rps.lote import Lote


EXPECTED = u'1001318010002006090120060904\n\r2RPS  A    00000000056220060903T000000000421500000000000000000071290500210008573745657900000000000000000000José Carlos                                                                R  Marina Ciufuli Zanfelice                          48                                      Lapa                          São Paulo                                         SP05040000jcarlos@josecarlos.org.br                                                  Cruzeiro: Sky Wonder|Destinos: Santos, Búzios, Angra dos Reis, Cabo Frio.|Cabine Externa\n\r2RPS  A    00000000056320060904T000000000348000000000000000000071290500210008407836699600000000000000000000Sergio Raul Salgado                                                        R  Marina Ciufuli Zanfelice                          50                                      Lapa                          São Paulo                                         SP05040000                                                                           Passagem Aérea: São Paulo - Lisboa - São Paulo.\n\r90000002000000000769500000000000000000\n\r'

@Vows.batch
class IntegrationVows(Vows.Context):

    def topic(self):
        lote = Lote('318010002', datetime.date(2006, 9, 1),
            datetime.date(2006, 9, 4))

        lote.append(RPS(
            serie_rps='A',
            numero_rps=562,
            data_emissao_rps=datetime.date(2006, 9, 3),
            valor_servicos=Decimal('4215'),
            codigo_servico_prestado=7129,
            aliquota=Decimal(5),
            iss_retido=2,
            tomador=Tomador(
                cpf_cnpj='85737456579',
                nome_razao_social=u'José Carlos',
                tipo_endereco='R',
                endereco='Marina Ciufuli Zanfelice',
                numero_endereco='48',
                bairro='Lapa',
                cidade=u'São Paulo',
                uf='SP',
                cep='05040000',
                email='jcarlos@josecarlos.org.br'
            ),
            discriminacao_servicos=u'''Cruzeiro: Sky Wonder
Destinos: Santos, Búzios, Angra dos Reis, Cabo Frio.
Cabine Externa'''
        ))

        lote.append(RPS(
            serie_rps='A',
            numero_rps=563,
            data_emissao_rps=datetime.date(2006, 9, 4),
            valor_servicos=Decimal('3480'),
            codigo_servico_prestado=7129,
            aliquota=Decimal(5),
            iss_retido=2,
            tomador=Tomador(
                cpf_cnpj='84078366996',
                nome_razao_social=u'Sergio Raul Salgado',
                tipo_endereco='R',
                endereco='Marina Ciufuli Zanfelice',
                numero_endereco='50',
                bairro='Lapa',
                cidade=u'São Paulo',
                uf='SP',
                cep='05040000'
            ),
            discriminacao_servicos=u'Passagem Aérea: São Paulo - Lisboa - São Paulo.'
        ))

        return EXPECTED, lote.as_text()

    def it_generates_a_valid_batch_text(self, topic):
        expected, actual = topic
        expect(expected).to_equal(actual)
