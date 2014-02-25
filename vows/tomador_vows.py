# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# # Nota Fiscal Paulistana
# # https://github.com/orygens/nf-paulistana

# # Licensed under the MIT license:
# # http://www.opensource.org/licenses/mit-license
# # Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


# from pyvows import Vows, expect

# from nf_paulista.tomador import Tomador


# CPF = '99999999999'
# CNPJ = '99999999999999'

# @Vows.batch
# class TomadorVows(Vows.Context):

#     class InitializedWithCPF(Vows.Context):

#         def topic(self):
#             return Tomador(cpf=CPF), CPF

#         def it_assigns_cpf(self, topic):
#             tomador, cpf = topic
#             expect(tomador.cpf).to_equal(cpf)

#         def it_has_a_valid_registry(self, topic):
#             tomador, _ = topic
#             expect(tomador.registry).to_equal('199999999999')

#     class InitializedWithCNPJ(Vows.Context):

#         def topic(self):
#             return Tomador(cnpj=CNPJ), CNPJ

#         def it_assigns_cnpj(self, topic):
#             tomador, cnpj = topic
#             expect(tomador.cnpj).to_equal(cnpj)
