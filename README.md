# DELTA V2
## DB(D)  Endpoint(E)  Latency(L)  Testing(T)  Ammeter(A) Version 2

Annoucing a new version of DELTA, a tool to calculate Cloud Database endpoint latency using SQL queries. This version is written from scratch to calculate latency more accurately and also to give p99 latency

📌 Introducing DELTA (DB Endpoint Latency Testing Ammeter). DELTA is a tool to test real-world latency against a remote database using execution of a query and calculating the network return time. The tool provides functions to test latency of Oracle, MySQL and Postgres databases.

The tool uses the oracledb, psycopg2 and pymysql packages to connect to the respective databases and execute a single query per request (you can specify multiple requests as well). The tool uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. It calculates the latency of each request and the average latency of all requests.

![DALL·E 2023-03-22 12 23 40 - pixel image of ammeter with 4 clouds in background](https://user-images.githubusercontent.com/39692236/226779332-fe58d03f-307a-45bc-9459-1a2225bbafad.png)


🔧 DELTA is a cloud tool to test real-world latency against a remote database endpoint using execution of a query and calculating the network return time. 


🔧 Network tools like ping ,iperf or tcp ping can only give you network based latency which does not always translate well to an application running those queries on a remote database. 


🐍 DELTA uses Python client for Oracle, MySQL and PostgreSQL to run a query like “SELECT 1” or "SELECT 1 FROM DUAL". You can then specific the number of executions of the query and DELTA calculates the average network round-trip time for all the executions of the query on the remote database. The script also includes error handling to track failed requests. You can also include your own custom queries. 



 ## Databases Supported 🔌 :

 
 ### Oracle DB >= 12.2 📌  : 

- Amazon RDS Oracle

- OCI Autonomous Database

- OCI VMDB

- OCI Exadata Cloud Service

- Oracle Database On-Premise

## Coming Soon

### Postgres >= 11 📌 :

- Amazon RDS Postgres

- Amazon RDS Aurora Postgres

- Postgres On-premise 


### MySQL >= 5.7 📌  : 

- Amazon RDS MySQL

- Amazon RDS Aurora MySQL

- OCI MySQL Database Service

- OCI MySQL Heatwave

- MySQL On-Premise


### SQL Server >= 2014 📌 : 

- Amazon RDS SQL Server

- Azure SQL Server

- SQL Server On-Premise


### URL - HTTPS | HTTP 📌 :

- Check Public or Private URLs for latency

# Requirements

Python >= 3.6.8

# Deploy

## Clone Repository



## Install Python packages

sudo pip3 install -r requirements.txt

## Run for Oracle 


