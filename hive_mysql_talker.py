"""The Script is meant to export example data from Hive to MySQL. Main reason
 for this is to generate a 500 rows displaying example for data source in
 UCloud SafeHouse Platform

First, connect mysql db and create the import table
Second, create a function to select specified number of rows from hive table
Third, use python's hdfs api to get the path(dir) of the newly created file(
500 row table)
in hdfs.
Fourth, Transfer the data via Sqoop
Important note:
1. we need to install mysql-python (mysqldb) module
check mysql-python support which python version!!
pip install mysql
or
pip install MySQL-Python
or
Download from http://sourceforge.net/projects/mysql-python
Linux user download from: https://pypi.python.org/pypi/MySQL-python
installation in shell:
$ gunzip MySQL-python-1.2.2.tar.gz
$ tar -xvf MySQL-python-1.2.2.tar
$ cd MySQL-python-1.2.2
$ python setup.py build
$ python setup.py install

2. get pyhs2 (python-hive-server) module

3. sqoop from hive to mysql
to transfer the whole table:
sqoop export --connect jdbc:mysql://192.168.32.128:3306/hive
  --username root --password root --table  t_user
   --export-dir /usr/hive/warehouse/hivetest.t_user
    --input-fields-terminated-by '\001'
to transfer certain columns:
sqoop export --connect jdbc:mysql://192.168.32.128:3306/hive
  --username root --password root --table  t_user --columns "id,name"
   --export-dir /usr/hive/warehouse/hivetest.t_user
    --input-fields-terminated-by '\001'

note the '\001' is the delimiter for columns in hive not comma, the column
name must be identical for hive and mysql if specified

as far as i know transfer data from hive to mysql using sqoop, we need to
specify the exporting directory path of hdfs, so we can not use data from a
hive virtual view.

if the chinese character in mysql after transfer is not correctly presented:
use #show variables like 'character%' in mysql and hive to check the encode
convention for these two DB and make changes if necessary
"""

import MySQLdb
import pyhs2
import os

'''MYSQL CONNECTION'''

# the sql query to create a table for later mysql db
CREATE_TABLE_QUERY = '''
    create table Student(
        StdID longtext primary key not null,
        Name longtext,
        Gender longtext,
        Age longtext
    )
'''

# the query to select data from hive; need modification, can not use virtual
# view instead of table
HIVE_SQL_QUERY = '''CREATE TABLE tmpTable as SELECT * FROM xxx LIMIT 500'''

MYSQL_DB = 'xxx'

HIVE_DB = 'xxxx'

NEW_HDFS_TABLE_NAME = 'abc'

mysqldb_config = dict(user="root", passwd="caizihao123", host="11.11.11.11",
                     port=3306, db="aaaaa", charset="utf8")

hive_config = dict(user='hdfs', password='***', host='192.168.8.88',
                       port=8888, authMechanism='PLAIN')


def connect_mysql():
    """"""
    # the ** is to split the dictionary as several parameters for another
    # function, list use single *
    return MySQLdb.connect(**mysqldb_config)


def run_mysql_query(mysql_conn, mysql_query):
    """"""
    with mysql_conn.cursor() as cursor:
        cursor.execute(mysql_query)
        return cursor.fetchall()


'''HIVE CONNECTION'''

# use pyhs2 (python-hive-server) to connect hive
def connect_hive():
    """"""
    return pyhs2.connect(**hive_config)


def run_hive_query(hive_conn, hql_query):
    """"""
    with hive_conn.cursor() as cursor:
        cursor.execute(hql_query)
        return cursor.fetchall()

def mysql_create_table(create_tbl_query, mysql_database):
    """"""
    try:
        mysql_conn = connect_mysql()
    except Exception as e:
        raise e
    # if the database is not exist in mysql db, create one
    # the database representation in mysql is a list rep
    if [mysql_database] not in run_mysql_query(mysql_conn, 'show databases'):
        run_mysql_query(mysql_conn, 'create database' + mysql_database)
    # now create the table in this database
    with mysql_conn.cursor() as cursor:
        cursor.execute('use '+ mysql_database)
        cursor.execute(create_tbl_query)
        # check the table has created
        my_cursor.execute('select * from xxx')
        example = my_cursor.fetchone()
        print('check create table: ', example)

'''
def hdfs_table_path_getter(hive_conn, database, table_name):
    """"""
    with hive_conn.cursor() as cursor:
        cursor.execute('use '+database)
        cursor.execute('show create table ' + table_name)
        # fetchall returns a tuple of strings
        table_info_tuple = cursor.fetchall()
        index_of_dir = 0
        # need to know how does the tuple looks like
        # a bit imagination of the tuple
        # (....,('LOCATION'), ('hdfs:mycluster/user/dir'),)
        for i in range(len(table_info_tuple)):
            if 'LOCATION' in table_info_tuple[i]:
                # the index of the dir is the next one of LOCATION
                index_of_dir = i + 1
        # now get the useful part of the dir from starting from /user..
        table_path = table_info_tuple[index_of_dir]
        # table path is still a tuple, we get the str[0]
        index_of_useful_path = table_path[0].index('/user')
        # now return the useful part of the table path starting from /user/...
        return table_path[0][index_of_useful_path:]
'''

def hive_to_mysql(hive_conn, username, password, host, port, export_dir,
                  table_name):
    """The function is meant to make use of the sqoop export functionality to
    export data from hive to mysql db.
    jdbc: mysql host server address

    Parameters:
        hive_conn: (str) the connector of python-hive api
        username: (str) the username of mysql db example:
        'root'
        password: (str) the password of mysql db example:
        'caizihao12345'
        host: (str) the host/master node public IP example: '192.168.88.888'
        port: (str) the host/master node port number example: '8888'
        export_dir: (str) export from which hdfs directory example:
        '/user/hive/warehouse/hadoop.db/m_d'
        table_name: (str) the table export from in hdfs/hive
    """
    # the input fields terminated by parameter is to specify
    os.system("sqoop export --connect jdbc:mysql://{0}:{1}/hive  --username " \
"{2} --password {3} --table {4} --export-dir {5} --input-fields-terminated-by " \
"'\001'".format(host,port,username,password,table_name,export_dir))


if __name__ == "__main__":
    ''' Connect MySQL and Create output table'''
    # connect mysql and create a cursor to execute sql command
    try:
        conn_mysql = connect_mysql()
    except Exception as e:
        print('fail to connect mysql db')
        raise e

    my_cursor = conn_mysql.cursor()
    try:
        # check mysql connection again
        conn_mysql.ping()

        # create the table in mysql db
        mysql_create_table(CREATE_TABLE_QUERY, MYSQL_DB)

        #end point of mysql connection
        conn_mysql.commit()
    except Exception as err:
        conn_mysql.rollback()
        print('fail to create table in mysql db')
        raise err
    finally:
        conn_mysql.close()

    '''Connect Hive and transfer data'''
    # try to talk to hive
    try:
        hive_conn = connect_hive()
    except Exception as e:
        print('fail to connect to hive')
        raise e

    # select the data from hive for transfer
    try:
        run_hive_query(hive_conn, HIVE_SQL_QUERY)
    except Exception as e:
        print('fail to select rows from hive and create the result table')
        raise e

    # find the dir/path of the newly created result table in HDFS
    try:
        #export_dir = hdfs_table_path_getter(hive_conn, HIVE_DB,
    # NEW_HDFS_TABLE_NAME)
        export_dir = 'hdfs://pub-cdh-01:8020/user/hive/warehouse/' + \
                     HIVE_DB + '/' + NEW_HDFS_TABLE_NAME
    except Exception as e:
        print('fail to get the path for the newly created table in hdfs')
        raise e

    # use sqoop to transfer data from hive to mysql db
    #hive_to_mysql(hive_conn, user, password, host, port, database, table)
    try:
        hive_to_mysql(hive_conn, 'root',...)
    except Exception as e:
        print('fail to transfer data from hive to mysql db')
        raise e
    finally:
        hive_conn.close()

