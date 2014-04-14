#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from ..registries import (
    Registry,
    Field,
    RegistryField,
    DateField,
    NumericField,
    DecimalField,
    TextField
)


class Cabecalho(Registry):

    tipo_registro = NumericField(length=1, order=1, default=1)
    versao_arquivo = NumericField(length=3, order=2, default=1)
    inscricao_municipal = NumericField(length=8, order=3)
    data_inicio = DateField(order=4)
    data_fim = DateField(order=5)


class RPS(Registry):

    tipo_registro = NumericField(length=1, order=1, default=2)
    tipo_rps = Field(length=5, order=2, default='RPS')
    serie_rps = Field(length=5, order=3)
    numero_rps = NumericField(length=12, order=4)
    data_emissao_rps = DateField(order=5)
    situacao_rps = Field(length=1, order=6, default='T')
    valor_servicos = DecimalField(order=7)
    valor_deducoes = DecimalField(order=8)
    codigo_servico_prestado = NumericField(length=5, order=9)
    aliquota = DecimalField(length=4, order=10)
    iss_retido = NumericField(length=1, order=11, default=1)
    tomador = RegistryField(order=12)
    discriminacao_servicos = TextField(order=13)


class Tomador(Registry):

    indicador_cpf_cnpj = NumericField(length=1, order=1, default=1)
    cpf_cnpj = NumericField(length=14, order=2)
    inscricao_municipal = NumericField(length=8, order=3)
    inscricao_estadual = NumericField(length=12, order=4)
    nome_razao_social = Field(length=75, order=5)
    tipo_endereco = Field(length=3, order=6)
    endereco = Field(length=50, order=7)
    numero_endereco = Field(length=10, order=8)
    complemento_endereco = Field(length=30, order=9)
    bairro = Field(length=30, order=10)
    cidade = Field(length=50, order=11)
    # uf = Field(length=2, order=12)
    cep = NumericField(length=8, order=13)
    email = Field(length=75, order=14)


class Rodape(Registry):

    tipo_registro = NumericField(length=1, order=1, default=9)
    numero_linhas = NumericField(length=7, order=2)
    total_servicos = DecimalField(order=3)
    total_deducoes = DecimalField(order=4)
