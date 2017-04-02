# To be scheduled via cron like:
# 00 03 * * * cd /var/www/rubi.dondevanmisimpuestos.es/public/presupuesto-rubi/scripts && ./update_budget_data.sh

python fetch_execution_data.py

python fetch_payment_data.py

python ../../manage.py load_budget 2016 --status=D --language=ca
python ../../manage.py load_budget 2016 --status=D --language=es

python ../../manage.py load_payments 2016 --language=ca
python ../../manage.py load_payments 2016 --language=es

sudo /home/david/clean-tmp-folder.sh rubi
