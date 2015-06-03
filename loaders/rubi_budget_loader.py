# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class RubiBudgetLoader(SimpleBudgetLoader):

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def clean(self, s):
        return s.split('.')[0]

    def parse_item(self, filename, line):
        # Skip lines without the first element
        if line[0] == '':
            return {
                'amount': 0
            }

        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            '1330': '1340',     # Mobilidad
            '1340': '1350',     # Protección Civil
            '1520': '1521',     # Vivienda
            '1550': '1531',     # Vías públicas
            '1620': '1621',     # Recogida de residuos
            '1720': '1721',     # Medio ambiente
            '2320': '2312',     # Mujer
            '2321': '2313',     # Ciudadanía y civismo
            '2330': '2314',     # Personas mayores y dependencia
            '3130': '3110',     # Salud pública
            '3132': '3111',     # Acogida de animales
            '3210': '3261',     # Guarderías
            '3221': '3262',     # Escuela de arte
            '3222': '3263',     # Escuela de música
            '3230': '3260',     # Promoción educativa
            '3320': '3321',     # Bibliotecas públicas
            '3360': '3330',     # Museos
            '3350': '3342',     # Artes escénicas
            '4311': '4312',     # Mercado
            '4410': '4411',     # Transporte colectivo urbano de viajeros
            '9211': '9202',     # Servicios generales del área de planificación estratégica
            '9213': '9206',     # Servicios generales del área de cohesión social
        }

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            fc_code = self.clean(line[1]).zfill(4)          # Fill with zeroes on the left if needed

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if year in ['2011', '2012', '2013', '2014']:
                new_programme = programme_mapping.get(fc_code)
                if new_programme:
                    fc_code = new_programme

            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': self.clean(line[2]),
                'ic_code': '100',
                'item_number': self.clean(line[2])[-2:],    # Last two digits
                'description': line[3],
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }

        else:
            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': self.clean(line[1]),
                'ic_code': '100',                           # All income goes to the root node
                'item_number': self.clean(line[1])[-2:],    # Last two digits
                'description': line[2],
                'amount': self._parse_amount(line[6 if is_actual else 3])
            }

    # We don't have an institutional breakdown in Torrelodones, so we create just a catch-all organism.
    # (We then configure the theme so we don't show an institutional breakdown anywhere.)
    def load_institutional_classification(self, path, budget):
        InstitutionalCategory(  institution='1',
                                section='10',
                                department='100',
                                description='Ayuntamiento de Rubí',
                                budget=budget).save()

