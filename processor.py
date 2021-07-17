import json
import yaml
import pprint
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def parse(json_file, test_name):
    with open(json_file, 'r') as output:
        results = json.load(output)
        jobs = results.get('jobs')[0]
        metadata = {key: value for key, value in results.items() if type(value) != dict and type(value) != list}
        metadata.update({key: value for key, value in jobs.items() if type(value) != dict and type(value) != list})
        metadata["global_options"] = results.get('global options')
        with open(json_file[:-5] + "-metadata.yml", 'w+') as f:
            yaml.dump(metadata, f, allow_unicode=True)
        connection = create_connection("admin", "admin", "a3b2f5c4", "frizzle.clients.homelab", "5432")
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            print(cursor.execute("CREATE DATABASE sm_app"))
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        gen = (key for key, value in jobs.items() if value is dict)
        pp = pprint.PrettyPrinter(indent=4)
        for key in gen:
            print(key)
    return 0

parse("2-2-30-8k.json", "asdf")