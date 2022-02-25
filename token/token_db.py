import pymysql as sql
import pymysql.err
import pandas as pd
import numpy as np

import pandas as pd
from make_token import TOKEN, df2


try:

    connection = sql.connect(host='localhost', password='foundry123', user='root') 
    cursor = connection.cursor()


    cursor.execute('CREATE DATABASE IF NOT EXISTS token_db')
    cursor.execute('USE token_db')

    cursor.execute(''' CREATE TABLE token (
        token_id INT,
        token_name VARCHAR(256) NOT NULL,
        token_symbol VARCHAR(256) NOT NULL,
        ethereum_contract_hash VARCHAR(256),
        circulating_supply FLOAT,
        total_supply VARCHAR(256),
        max_supply VARCHAR(256)) ''')


    array = TOKEN.values.tolist()
    placeholders = ', '.join(['%s'] * len(TOKEN.columns))
    columns = ', '.join([col for col in list(TOKEN.columns.values)])
    statement = "INSERT INTO token ( %s ) VALUES ( %s )" % (columns, placeholders)
    cursor.executemany(statement, array)

    connection.commit()


    ######### Insert ethereum_contract_hash, circulating_supply, total_supply and max_supply ############
    df2 = df2.rename(columns={'name': 'token_name', 'symbol': 'token_symbol'})
    
    for i in (range(len(df2.values))):
        statement2 = ""
        statement2 += """ UPDATE token 
        SET ethereum_contract_hash = " %s " , 
        circulating_supply = %s, 
        total_supply = "%s", 
        max_supply = " %s " WHERE token_name = ( "%s" ) """ % (df2['ethereum_contract_hash'][i], df2['circulating_supply'][i], df2['total_supply'][i], df2['max_supply'][i], df2['token_name'][i])
        #print(statement2)

        cursor.execute(statement2)
    connection.commit()
    
   

except pymysql.err.ProgrammingError:
    print('error')
    pass 

connection.autocommit=True
cursor.close()
connection.close()

