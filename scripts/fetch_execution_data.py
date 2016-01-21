# -*- coding: UTF-8 -*-
import urllib2
import csv
import os.path

# Find base path to generate output files
base_path = os.path.dirname(os.path.realpath(__file__))


# Download income data
# See https://opendata.rubi.cat/es/Finances-Municipals/Pressupost-municipal_Estat-d-execuci-d-ingressos/ds9h-xggj
print "Descargando datos de ingresos..."
response = urllib2.urlopen('https://opendata.rubi.cat/api/views/ds9h-xggj/rows.csv?accessType=DOWNLOAD')

# Parse downloaded data
print "Parseando datos..."
reader = csv.reader(response)
# Note: the output is the same for both languages in this case (not for payments for example)
writer_ca = csv.writer(open(os.path.join(base_path, '..', 'data', 'ca', 'municipio', '2015', 'ejecucion_ingresos.csv'), 'wb'))
writer_es = csv.writer(open(os.path.join(base_path, '..', 'data', 'es-es', 'municipio', '2015', 'ejecucion_ingresos.csv'), 'wb'))
for index, line in enumerate(reader):
  if index==0:         # Ignore header line
      continue

  # Keep EXERCICI, CODI_ECONOMIC, APLICACIO, PRESSUPOST_INICIAL, MODIFICACIONS_CREDIT,
  # PREVISIONS_DEFINITIVES, DRETS_RECONEGUTS_NETS
  # Note: we keep the descriptions but we ignore them in the application whenever possible, 
  # i.e. if the economic code already existed in the budget data, because the descriptions
  # in execution data tend to be crappy. We are assuming that the description for a given 
  # economic code doesn't change in a given year, which seems like a reasonable assumption.
  writer_ca.writerow([line[0], line[3], line[5], line[6], line[7], line[8], line[9]])
  writer_es.writerow([line[0], line[3], line[5], line[6], line[7], line[8], line[9]])


# Download expense data
# See https://opendata.rubi.cat/es/Finances-Municipals/Pressupost-municipal_Estat-d-execuci-de-despeses/ynig-hhni
print "Descargando datos de gasto..."
response = urllib2.urlopen('https://opendata.rubi.cat/api/views/ynig-hhni/rows.csv?accessType=DOWNLOAD')

# Parse downloaded data
print "Parseando datos..."
reader = csv.reader(response)
# Note: the output is the same for both languages in this case (not for payments for example)
writer_ca = csv.writer(open(os.path.join(base_path, '..', 'data', 'ca', 'municipio', '2015', 'ejecucion_gastos.csv'), 'wb'))
writer_es = csv.writer(open(os.path.join(base_path, '..', 'data', 'es-es', 'municipio', '2015', 'ejecucion_gastos.csv'), 'wb'))
for index, line in enumerate(reader):
  if index==0:         # Ignore header line
      continue

  # Keep EXERCICI, CODI_FUNCIONAL, CODI_ECONOMIC, APLICACIO, PRESSUPOST_INICIAL, MODIFICACIONS_CREDIT,
  # CREDIT_DEFINITIU, OBLIGACIONS_RECONEGUDES
  writer_ca.writerow([line[0], line[3], line[5], line[7], line[8], line[9], line[10], line[11]])
  writer_es.writerow([line[0], line[3], line[5], line[7], line[8], line[9], line[10], line[11]])


# Done
print u"Datos descargados con éxito. %s líneas." % (reader.line_num)
