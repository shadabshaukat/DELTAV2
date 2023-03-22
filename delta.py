import warnings
import argparse
import datetime
import time
import csv
import os
import numpy as np
from cryptography import __version__ as cryptography_version
from urllib.parse import urlparse
import requests

import cx_Oracle as oracledb
import psycopg2
import pymysql
import pyodbc

if cryptography_version < "3.4":
    warnings.filterwarnings("ignore", category=UserWarning, message=".*will be forbidden in the future.*")

query_times = []

# Oracle Database credentials
oracle_un = 'your_username'
oracle_pw = 'your_password'
oracle_cs = 'your_oracle_connection_string' # Can be full connectivity string or host:port/servicename. Works with Oracle DB >= 12.2 only

# PostgreSQL credentials
pgsql_un = 'your_username'
pgsql_pw = 'your_password'
pgsql_host = 'your_host'
pgsql_port = 'your_port'
pgsql_db = 'your_database'

# MySQL credentials
mysql_un = 'your_username'
mysql_pw = 'your_password'
mysql_host = 'your_host'
mysql_port = 'your_port'
mysql_db = 'your_database'

# SQL Server credentials
sql_server_un = 'your_username'
sql_server_pw = 'your_password'
sql_server_host = 'your_host'
sql_server_port = 'your_port'
sql_server_db = 'your_database'

# URL for testing
test_url = 'https://www.google.com.au'

def calculate_p99_latency():
    if len(query_times) > 0:
        p99_latency = np.percentile(query_times, 99)
        print("P99 latency: {:.2f} ms".format(p99_latency))
    else:
        print("No queries were executed.")

def oracle_ping(interval, csvfile):
    # Establish a new database connection
    conn = oracledb.connect(user=oracle_un, password=oracle_pw, dsn=oracle_cs)

    # Get cursor object
    cursor = conn.cursor()

    # Get session information
    cursor.execute("select sys_context('USERENV','SID'), sys_context('USERENV','INSTANCE') from dual")
    sid, instance = cursor.fetchone()

    # Execute the query and time it
    t0 = time.perf_counter()
    cursor.execute("select 1 from dual")
    cursor.fetchall()
    t1 = time.perf_counter()

    # Calculate the timings
    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    # Write the timings to the CSV file
    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time, sid, instance])

    # Close the cursor and the connection
    cursor.close()
    conn.close()



def postgresql_ping(interval, csvfile):
    conn = psycopg2.connect(host=pgsql_host, port=pgsql_port, dbname=pgsql_db, user=pgsql_un, password=pgsql_pw)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def mysql_ping(interval, csvfile):
    conn = pymysql.connect(host=mysql_host, port=int(mysql_port), user=mysql_un, password=mysql_pw, db=mysql_db)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def sql_server_ping(interval, csvfile):
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={sql_server_host},{sql_server_port};DATABASE={sql_server_db};UID={sql_server_un};PWD={sql_server_pw}'
    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def url_ping(interval, csvfile):
    t0 = time.perf_counter()
    response = requests.get(test_url)
    t1 = time.perf_counter()

    # (The rest of the function remains the same)

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])



# Parse command line arguments
parser = argparse.ArgumentParser(description="Connect and run a query.")
parser.add_argument("--interval", type=float, help="interval between each query, default 1", default=1)
parser.add_argument("--period", type=int, help="runtime in seconds; default 60", default=60)
parser.add_argument("--csvoutput", help="write timings to the named CSV file")
parser.add_argument("--db", choices=['oracle', 'postgresql', 'mysql', 'sqlserver', 'url'], required=True, help="specify the database or url to test")
args = parser.parse_args()

# Open the CSV file if specified
if args.csvoutput is not None:
    csvfile = open(args.csvoutput, "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Query time (ms)", "SID", "Instance"])
else:
    csvfile = None

# Calculate the start time and the end time
start_time = time.perf_counter()
end_time = start_time + args.period

# Run the main loop
while time.perf_counter() < end_time:
    if args.db == 'oracle':
        oracle_ping(args.interval, csvfile)
    elif args.db == 'postgresql':
        postgresql_ping(args.interval, csvfile)
    elif args.db == 'mysql':
        mysql_ping(args.interval, csvfile)
    elif args.db == 'sqlserver':
        sql_server_ping(args.interval, csvfile)
    elif args.db == 'url':
        url_ping(args.interval, csvfile)
    time.sleep(args.interval)

# Calculate and print the final P99 latency
calculate_p99_latency()