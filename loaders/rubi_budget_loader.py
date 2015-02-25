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

        # Skip lines whitout the first element
        if line[0] == '':
            return {
                'amount': 0
            }
        
        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            fc_code = self.clean(line[1]).zfill(4)          # Fill with zeroes on the left if needed
            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': self.clean(line[2]),
                'ic_code': '100', #self.clean(line[0]).replace('U','').zfill(4),    # Fill with zeroes on the left if needed
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

