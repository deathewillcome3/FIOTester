import json
import yaml
import pprint
import psycopg2
import re
from psycopg2 import OperationalError


# Self Explanatory
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
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    return connection


# Recursively weeds out all the items in a dictionary
def unpack_dict(old_dict, new_dict, dup):
    if old_dict:
        new_dict.update({dup + key: value for key, value in old_dict.items() if type(value) != dict
                         and type(value) != list})
        temp = (key for key, value in old_dict.items() if type(value) == list or type(value) == dict)

        if temp:
            for key in temp:
                unpack_dict(old_dict.get(key), new_dict, dup[:-1] + "_" + key + "_") if dup != "" else \
                    unpack_dict(old_dict.get(key), new_dict, key + "_")
    else:
        pass


# Helper Function
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


# Formats the data headers in a style that PostgreSQL likes
def process_headers(args):
    temp = "rw_mix INT, \n threads INT, \n queue_depth INT, \n blocksize VARCHAR, \n "
    temp_iter = iter(args)

    while True:
        try:
            arg = next(temp_iter)
            if arg.rfind('.') != -1:
                arg = arg.replace(".", "")
            if arg.rfind('>=') != -1:
                arg = arg.replace(">=", "greater_")
            temp += arg + " decimal, \n "
        except StopIteration:
            temp = temp[:-4]
            break

    return temp


# Inits proper database schemas
def set_up_tables(connection, args, name):
    connection = create_connection("benchmarking", "admin", "", "frizzle.clients.homelab", "5432")
    connection.autocommit = True
    cursor = connection.cursor()
    temp = "CREATE TABLE " + name + "( \n" + args \
           + ");"

    # DEBUG: Too be removed later
    # print(temp)

    try:
        cursor.execute(temp)
        cursor.close()
        connection.commit()
    except psycopg2.errors.DuplicateTable as error:
        pass


# Does a simple Insert statement to the database
def insert_data(name, headers, data):
    connection = create_connection("benchmarking", "admin", "", "frizzle.clients.homelab", "5432")
    connection.autocommit = True
    headers = "( \n " + headers.replace("decimal", "").replace("INT", "").replace("VARCHAR", "") + ")"
    command = "INSERT INTO %s %s values %s ;" % (name, headers, data)
    cursor = connection.cursor()

    # DEBUG: Too be removed later
    # print(command)

    try:
        cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error")
        print(type(error))
    finally:
        if connection is not None:
            connection.close()


def export_csv(name, dest):
    connection = create_connection("benchmarking", "admin", "", "frizzle.clients.homelab", "5432")
    connection.autocommit = True
    command = "COPY %s TO %s DELIMITER ',' CSV HEADER;" % (name, dest)
    cursor = connection.cursor()

    # DEBUG: Too be removed later
    # print(command)

    try:
        cursor.execute(command)
        cursor.close()
        connection.commit()
    except psycopg2.DatabaseError as error:
        print(type(error))
    finally:
        if connection is not None:
            connection.close()


# Main function does all the heavy lifting
def parse(json_file, test_name, params):
    with open(json_file, 'r') as output:
        # Opening/loading json file
        results = json.load(output)
        jobs = results.get('jobs')[0]
        # Metadata: All the stuff that is not directly measured Data: All the results from the test runs
        metadata = {key: value for key, value in results.items() if type(value) != dict and type(value) != list}
        metadata.update({key: value for key, value in jobs.items() if type(value) != dict and type(value) != list})
        metadata["global_options"] = results.get('global options')
        # Data: All the results from the test runs
        data = {}
        unpack_dict(jobs, data, "")
        data.pop("job options_name")
        # Removing the Duplicate Objects and Processing the Data
        duplicates = {key: value for key, value in data.items() if (metadata.get(key) is not None)}
        gen = (key for key in data if duplicates.get(key) is not None)
        for key in gen:
            data = removekey(data, key)
        # Breaking up the Dictionary into two arrays containing headers + actual data
        data_headers = []
        data_content = [params[0], params[1], params[2],
                        params[3]]
        for key, value in data.items():
            data_headers.append(key)
            data_content.append(value)
        # PostgresSQL Connection
        connection = create_connection("admin", "admin", "", "frizzle.clients.homelab", "5432")
        connection.autocommit = True
        cursor = connection.cursor()

        # Debug code will be removed
        # for key, value in data.items():
        #     print(str(key) + ":" + str(value))

        # Dumping metadata to seperate output file
        with open(json_file[:-5] + "-metadata.yml", 'w+') as f:
            yaml.dump(metadata, f, allow_unicode=True)

        # Executing database insert statement (Creates Tables if it doesnt exist)
        try:
            cursor.execute("CREATE DATABASE benchmarking")
        except psycopg2.errors.DuplicateDatabase as e:
            pass
        finally:
            print(tuple(data_content))
            set_up_tables(data_headers, process_headers(data_headers), test_name)
            insert_data(test_name, process_headers(data_headers), tuple(data_content))
            connection.close()
    return 0

# MORE DEBUG CODE
# parse("16-16-50-512.json", "first_test", {"test": "asdfasdf"})
