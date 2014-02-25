#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/orygens/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from ..registries import Registry, Field


class Tomador(Registry):

    indicador_cpf_cnpj = Field(length=1, order=1, default=1)
    cpf_cnpj = Field(length=14, order=2)
    inscricao_municipal = Field(length=8, order=3)
    inscricao_estadual = Field(length=12, order=4)
    nome_razao_social = Field(length=75, order=5)
    tipo_endereco = Field(length=3, order=6)
    endereco = Field(length=50, order=7)
    nummero_endereco = Field(length=10, order=8)
    complemento_endereco = Field(length=30, order=9)
    bairro = Field(length=30, order=10)
    cidade = Field(length=50, order=11)
    uf = Field(length=2, order=12)
    cep = Field(length=8, order=13)
    email = Field(length=75, order=14)
