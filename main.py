""" This script will read a directory and check if there are new JSON for processing.
Crontab: 30 * * * * /bin/bash -c '/usr/bin/python /var/www/besm/restrito/scripts/besm_json_parser/main.py'
to run every 30 minutes.
"""

import os
import subprocess

json_dir = "/".join((os.path.dirname(os.path.abspath(__file__)), "json"))
print(" ".join(("Scanning", json_dir)))

def checkList(file_to_check):
    list_file = open("/".join((json_dir, "list.txt")), "r+")
    lines = list_file.readlines()
    lines = [w.replace('\n', '') for w in lines]
    if file_to_check not in lines:
        list_file.write(file_to_check + "\n")
        command = "/usr/bin/python {}/besm_json_parser.py json/{} ../db_info.txt".format(
            os.path.dirname(os.path.abspath(__file__)),
            file_to_check
        )
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)

for (dirpath, dirnames, filenames) in os.walk(json_dir):
    for json_file in filenames:
        if ".json" in json_file:
            checkList(json_file)