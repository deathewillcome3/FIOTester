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

def set_up_tables(connection):
    cursor = connection.cursor()
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    try:
        for command in commands:
                cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def parse(json_file, test_name, params):
    with open(json_file, 'r') as output:
        results = json.load(output)
        jobs = results.get('jobs')[0]
        metadata = {key: value for key, value in results.items() if type(value) != dict and type(value) != list}
        metadata.update({key: value for key, value in jobs.items() if type(value) != dict and type(value) != list})
        metadata["global_options"] = results.get('global options')
        with open(json_file[:-5] + "-metadata.yml", 'w+') as f:
            yaml.dump(metadata, f, allow_unicode=True)
        connection = create_connection("admin", "admin", "", "frizzle.clients.homelab", "5432")
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE DATABASE benchmarking")
            print("Query executed successfully")
            set_up_tables(connection)
        except OperationalError as e:
            set_up_tables(connection)

        gen = (key for key, value in jobs.items() if value is dict)
        pp = pprint.PrettyPrinter(indent=4)
        for key in gen:
            print(key)
    return 0

parse("2-2-30-8k.json", "asdf", {"test": "asdfasdf"})