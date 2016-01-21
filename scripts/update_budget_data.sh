# To be scheduled via cron like:
# 00 03 * * * cd /var/www/rubi.dondevanmisimpuestos.es/public/presupuesto-rubi/scripts && ./update_budget_data.sh

echo 'Disabled until 2016 budget is available'
exit

python fetch_execution_data.py

python fetch_payment_data.py

python ../../manage.py load_budget 2015 --status=D --language=ca
python ../../manage.py load_budget 2015 --status=D --language=es-es

python ../../manage.py load_payments 2015 --language=ca
python ../../manage.py load_payments 2015 --language=es-es

sudo /home/david/clean-tmp-folder.sh rubi
