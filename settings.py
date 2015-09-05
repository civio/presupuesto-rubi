# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

MAIN_ENTITY_LEVEL = 'municipio'
MAIN_ENTITY_NAME = 'Rubí'

BUDGET_LOADER = 'RubiBudgetLoader'
PAYMENTS_LOADER = 'RubiPaymentsLoader'

FEATURED_PROGRAMMES = ['1710', '3321', '3261', '1630', '2410', '3263', '3340', '3370', '3410', '4411', '9242']

OVERVIEW_INCOME_NODES = [['11', '113'], '13', '42', '43', '45', '46', '30', '33', '34', '39']
OVERVIEW_EXPENSE_NODES = ['23', '92', '13', '16', '15', '01', '33', '32', '43', '44', '91', '93', '17']

# Show an extra tab with institutional breakdown. Default: True.
SHOW_INSTITUTIONAL_TAB = False

# Show an extra tab with funding breakdown (only applicable to some budgets). Default: False.
# SHOW_FUNDING_TAB = False

# Show an extra column with actual revenues/expenses. Default: True.
# Warning: the execution data still gets shown in the summary chart and in downloads.
#SHOW_ACTUAL = True

# Include financial income/expenditures in overview and global policy breakdowns. Default: False.
INCLUDE_FINANCIAL_CHAPTERS_IN_BREAKDOWNS = True

# Search in entity names. Default: True.
SEARCH_ENTITIES = False

# Supported languages. Default: ('ca', 'Catal&agrave;')
LANGUAGES = (
  ('ca', 'Catal&agrave;'),
  ('es-ES', 'Castellano')
)

# Allow overriding of default treemap color scheme
COLOR_SCALE = [ '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#e7969c', '#bcbd22', '#17becf' ]
