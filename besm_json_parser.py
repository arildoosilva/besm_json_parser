""" This script will read a json file and use peewee to insert data into a MySQL table.
External packages needed: peewee, PyMySQL
https://github.com/PyMySQL/PyMySQL
https://peewee.readthedocs.org/en/latest/peewee/installation.html
"""

import json
import sys
import peewee
from peewee import *

json_file = None
db_file = None

if len(sys.argv) != 3:
    print("You need to specify a JSON file and the DB file in format 'database username password'")
    sys.exit(2)
if len(sys.argv) == 3:
    json_file = sys.argv[1]
    db_file = sys.argv[2]

with open(db_file, "r") as db_info:
    lines = db_info.readlines()
    for line in lines:
        db_name, db_user, db_pass = line.split()

db = MySQLDatabase(database=db_name, user=db_pass, passwd=db_pass)
status_choices = (
    ('ativo_ok', 'ativo_ok'),
    ('ativo_erro', 'ativo_erro'),
    ('ativo_aborted', 'ativo_aborted'),
    ('completo_ok', 'completo_ok'),
    ('completo_erro', 'completo_erro'),
    ('completo_aborted', 'completo_aborted')
)

class wp_experimentos(peewee.Model):
    id_experimento = peewee.IntegerField(primary_key=True, unique=True)
    nome_experimento = peewee.CharField(null=False, max_length=30)
    readme = peewee.TextField(null=False)
    anos_total = peewee.IntegerField(null=False)
    ano_atual = peewee.IntegerField(null=False)
    total_erros = peewee.IntegerField(null=False)
    status = peewee.CharField(null=False, choices=status_choices)

    class Meta:
        database = db



with open(json_file) as data_file:
    data = json.load(data_file)

for experimento in data["experimentos"]:
    try:
        with db.transaction():
            peewee_experiment = wp_experimentos.create(
                id_experimento=experimento["id_experimento"],
                nome_experimento="'{}'".format(experimento["nome_experimento"]),
                readme="'{}'".format(experimento["readme"]),
                anos_total=experimento["anos_total"],
                ano_atual=experimento["ano_atual"],
                total_erros=experimento["total_erros"],
                status="'{}'".format(experimento["status"])
            )
        print("Added {} in the database".format(experimento["nome_experimento"]))
    except IntegrityError:
        peewee_experiment = wp_experimentos.update(
            id_experimento=experimento["id_experimento"],
            nome_experimento="'{}'".format(experimento["nome_experimento"]),
            readme="'{}'".format(experimento["readme"]),
            anos_total=experimento["anos_total"],
            ano_atual=experimento["ano_atual"],
            total_erros=experimento["total_erros"],
            status="'{}'".format(experimento["status"])
        ).where(wp_experimentos.id_experimento == experimento["id_experimento"])
        peewee_experiment.execute()
        print("Updated {} in the database".format(experimento["nome_experimento"]))
