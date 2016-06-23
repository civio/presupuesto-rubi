# -*- coding: UTF-8 -*-
import urllib2
import csv
import os.path
import re
import datetime

# TODO: This shouldn't be hardcoded
YEAR_TO_LOAD = '2016'

# Read functional categories from given file and return as a dictionary
def read_functional_categories(filename):
  reader = csv.reader(open(filename, 'rb'))
  categories = {}
  for index, line in enumerate(reader):
    if re.match("^#", line[0]):     # Ignore comments
        continue

    area = line[0]
    policy = line[1]
    group = line[2]
    programme = line[3]
    description = line[4]

    categories[area+policy+group+programme] = description

  return categories


# Find base path to generate output files
base_path = os.path.dirname(os.path.realpath(__file__))

# Read functional categories data, to cross reference with payments
functional_categories_file_ca = os.path.join(base_path, '..', 'data', 'ca', 'areas_funcionales.csv')
functional_categories_ca = read_functional_categories(functional_categories_file_ca)

functional_categories_file_es = os.path.join(base_path, '..', 'data', 'es-es', 'areas_funcionales.csv')
functional_categories_es = read_functional_categories(functional_categories_file_es)

# There have been some changes in 2016 (with a new government in place), some
# programme codes have been changed. We could modify 2015 data and reload all
# budgets or -easier- modify new 2016 data to match existing.
programme_mapping_from_2016 = {
    '1720': '1721',     # Medio ambiente
    '3264': '3213',     # Guardería La Bruna
    '3265': '3211',     # Guardería La Lluna
}

# Download payment data
# See https://opendata.rubi.cat/es/Finances-Municipals/Obligacions-reconegudes/qnp2-hje6
print "Descargando datos de pagos..."
response = urllib2.urlopen('https://opendata.rubi.cat/api/views/qnp2-hje6/rows.csv?accessType=DOWNLOAD')

# Parse downloaded data
print "Parseando datos..."
reader = csv.reader(response)
# Note: the output is NOT the same for both languages in this case
writer_ca = csv.writer(open(os.path.join(base_path, '..', 'data', 'ca', 'municipio', YEAR_TO_LOAD, 'pagos.csv'), 'wb'))
writer_es = csv.writer(open(os.path.join(base_path, '..', 'data', 'es-es', 'municipio', YEAR_TO_LOAD, 'pagos.csv'), 'wb'))
for index, line in enumerate(reader):
  if index==0:          # Ignore header line
      continue

  # Soemtimes there are error lines in the output. Ignore them
  if 'DATABASE_ERROR' in line[0]:
      continue

  # Parse (and transform) the payment item
  programme_id = programme_mapping_from_2016.get(line[11], line[11])
  economic_id = line[12]
  beneficiary_id = line[2]
  # The current table breakdown implementation can't handle empty strings well.
  # This is the best place to patch it at the moment.
  description = line[4] if line[4]!='' else '...'
  amount = line[9]

  # We're only interested in the payments for the current year
  budget_year = line[14]
  if budget_year != YEAR_TO_LOAD:
      continue

  # Read and reformat the date to match what the loader expects (yyyy-mm-dd).
  # Note that the date is not always available.
  try:
      date = datetime.datetime.strptime(line[6], "%d/%m/%Y")
      formatted_date = date.strftime("%Y-%m-%d")
  except ValueError:
      formatted_date=None

  # If we have no beneficiary it's because of personal data protection laws. Make a note about it
  if line[3]!='':
    beneficiary_name_ca = line[3]
    beneficiary_name_es = line[3]
  else:
    beneficiary_name_ca = "<abbr title='Aquest concepte recull les persones físiques, la identitat " \
                          "de les quals queda protegida en compliment de la Llei Orgànica de Protecció " \
                          "de Dades.'>[Anonimitzat]*</abbr>"
    beneficiary_name_es = "<abbr title='Este concepto recoge las personas físicas cuya identidad " \
                          "queda protegida en cumplimiento de la Ley Organica de Protección de Datos.'>" \
                          "[Anonimizado]*</abbr>"

  # Output lines
  writer_ca.writerow([
      functional_categories_ca[programme_id],
      programme_id,
      economic_id,
      '',               # period, for historical reasons, ignore
      formatted_date,
      beneficiary_id,
      beneficiary_name_ca,
      '',               # contract type, for historical reasons, ignore
      description,
      amount,
      ''                # data source, for historical reasons, ignore
    ])

  writer_es.writerow([
      functional_categories_es[programme_id],
      programme_id,
      economic_id,
      '',               # period, for historical reasons, ignore
      formatted_date,
      beneficiary_id,
      beneficiary_name_es,
      '',               # contract type, for historical reasons, ignore
      description,
      amount,
      ''                # data source, for historical reasons, ignore
    ])


# Done
print u"Datos descargados con éxito. %s líneas." % (reader.line_num)
