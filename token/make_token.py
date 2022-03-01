import os
import json
import pandas as pd
import requests
import pymysql as sql
import pymysql.err
from decimal import Decimal


DATABASE = json.loads(os.getenv('TOKEN_SCHEMA_CONNECT'))

#########################
## ADD NEW TOKENS HERE ##
#########################


# token_name / token_symbol
NEW_TOKENS = {
    'Dogecoin': 'DOGE'
}

#########################
#########################
#########################

# start static token table
TOKEN = pd.DataFrame([[0,'Bitcoin','BTC'],
[1,'Aave','AAVE'],
[2,'Algorand','ALGO'],
[3,'Amp','AMP'],
[4,'Avalanche','AVAX'],
[5,'Basic Attention Token','BAT'],
[6,'BNB','BNB'],
[7,'Bitcoin Cash','BCH'],
[8,'Bitcoin SV','BSV'],
[9,'Stacks','STX'],
[10,'Cardano','ADA'],
[11,'Celo','CELO'],
[12,'Celsius Network','CEL'],
[13,'Chainlink','LINK'],
[14,'Chia','XCH'],
[15,'Compound','COMP'],
[16,'ConstitutionDAO','PEOPLE'],
[17,'Cosmos','ATOM'],
[18,'Dai','DAI'],
[19,'DAO Maker','DAO'],
[20,'Dash','DASH'],
[21,'Decentraland','MANA'],
[22,'Elrond','EGLD'],
[23,'Enjin Coin','ENJ'],
[24,'EOS','EOS'],
[25,'Ethereum','ETH'],
[26,'Ethereum Classic','ETC'],
[27,'Ethereum Name Service','ENS'],
[28,'Filecoin','FIL'],
[29,'Flow','FLOW'],
[30,'FTX Token','FTT'],
[31,'Gemini Dollar','GUSD'],
[32,'Hedera','HBAR'],
[33,'Helium','HNT'],
[34,'Internet Computer','ICP'],
[35,'Litecoin','LTC'],
[36,'Livepeer','LPT'],
[37,'Maker','MKR'],
[38,'Polygon','MATIC'],
[39,'Monero','XMR'],
[40,'Near','NEAR'],
[41,'PancakeSwap','CAKE'],
[42,'PAX Gold','PAXG'],
[43,'Pax Dollar','USDP'],
[44,'Polkadot','DOT'],
[45,'Ravencoin','RVN'],
[46,'renBTC','RENBTC'],
[47,'REN','REN'],
[48,'XRP','XRP'],
[49,'Shiba Inu','SHIB'],
[50,'Solana','SOL'],
[51,'Stellar','XLM'],
[52,'Sushi','SUSHI'],
[53,'Terra','LUNA'],
[54,'TerraUSD','UST'],
[55,'Tether','USDT'],
[56,'Tezos','XTZ'],
[57,'The Graph','GRT'],
[58,'THORChain','RUNE'],
[59,'TRON','TRX'],
[60,'Uniswap','UNI'],
[61,'USD Coin','USDC'],
[62,'VeChain','VET'],
[63,'Waves','WAVES'],
[64,'Wrapped Bitcoin','WBTC'],
[65,'yearn.finance','YFI'],
[66,'Horizen','ZEN'],
[67,'Zilliqa','ZIL'],
[68,'0x','ZRX']
], columns = ['token_id', 'token_name', 'token_symbol'])

def add_new_tokens():
    new = pd.DataFrame(NEW_TOKENS.items(),columns = ['token_name', 'token_symbol'])
    merged = pd.concat([TOKEN, new], ignore_index=True)
    merged['token_id']=merged['token_id'].fillna(merged.index.to_series())
    return merged

TOKEN = add_new_tokens()

def create_token_table():
    try:
        connection = sql.connect(host=DATABASE['host'], password= DATABASE['password'], user=DATABASE['user']) 
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS token')
        cursor.execute('USE token')
        cursor.execute(''' CREATE TABLE token (
            token_id INT,
            token_name VARCHAR(256) NOT NULL,
            token_symbol VARCHAR(12) NOT NULL,
            ethereum_contract_hash NVARCHAR(256),
            polygon_contract_hash NVARCHAR(256),
            avalanche_contract_hash NVARCHAR(256),
            solana_contract_hash NVARCHAR(256),
            circulating_supply DECIMAL(45,25),
            total_supply DECIMAL(45,25),
            max_supply DECIMAL(45,25)) ''')

        array = TOKEN.values.tolist()
        placeholders = ', '.join(['%s'] * len(TOKEN.columns))
        columns = ', '.join([col for col in list(TOKEN.columns.values)])
        statement = "INSERT INTO token ( %s ) VALUES ( %s )" % (columns, placeholders)
        cursor.executemany(statement, array)
        connection.commit()
    except pymysql.err.ProgrammingError:
        print('error')
        pass 
    connection.autocommit=True
    cursor.close()
    connection.close()

def zipinsert(type, value, symbol, cur, con):
    statement = """UPDATE token.token SET {} = '{}' WHERE token_symbol = '{}';""". format(type, value, symbol)
    cur.execute(statement)
    con.commit()

def insert_supply_info(token_data):
    zippeddata = zip(token_data['token_symbol'], token_data['circulating_supply'], token_data['total_supply'], token_data['max_supply'])

    connection = sql.connect(host=DATABASE['host'], password= DATABASE['password'], user=DATABASE['user']) 
    cursor = connection.cursor()

    try:
        for tsym, csupp, tsupp, msupp in zippeddata:
    
            if csupp:
                zipinsert('circulating_supply', csupp, tsym, cursor, connection)
            if tsupp:
                zipinsert('total_supply', tsupp, tsym, cursor, connection)
            if msupp:
                zipinsert('max_supply', msupp, tsym, cursor, connection)

    except pymysql.err.ProgrammingError as error:
        print(error)
        pass

def insert_contract_hashes(token_data):
    zippeddata = zip(token_data['token_symbol'], token_data['ethereum_contract_hash'], token_data['polygon_contract_hash'], token_data['avalanche_contract_hash'], token_data['solana_contract_hash'])

    connection = sql.connect(host=DATABASE['host'], password= DATABASE['password'], user=DATABASE['user']) 
    cursor = connection.cursor()

    try:
        for tsym, chash, phash, ahash, shash in zippeddata:
            if chash:
                zipinsert('ethereum_contract_hash', chash, tsym, cursor, connection)
            if phash:
                zipinsert('polygon_contract_hash', phash, tsym, cursor, connection)
            if ahash:
                zipinsert('avalanche_contract_hash', ahash, tsym, cursor, connection)
            if shash:
                zipinsert('solana_contract_hash', shash, tsym, cursor, connection)

    except pymysql.err.ProgrammingError as error:
        return error

    connection.autocommit=True
    cursor.close()
    connection.close()
        
def get_token_data():
    df = pd.read_json("https://api.coingecko.com/api/v3/coins/list?include_platform=true")
    # makes requests and dumps raw data into dataframe
    calls = [requests.get(url) for url in ['https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page={}'.format(i + 1) for i in range(10)]]
    data = pd.concat([pd.DataFrame(call.json()) for call in calls]).reset_index()
    data = data[['index', 'id', 'symbol', 'name', 'circulating_supply', 'total_supply',
        'max_supply', 'ath', 'ath_date', 'atl', 'atl_date', 'last_updated']]
    df_normalize = pd.json_normalize(df['platforms'])
    df = pd.concat([df,df_normalize], axis = 1).drop(columns='platforms')

    # normalizes raw data
    df.columns = df.columns.str.replace('-','_')
    df = df.rename(columns = {'polygon_pos': 'polygon'})
    df = df.rename(columns={col: col+'_contract_hash' 
                            for col in df.columns if col not in ['id', 'symbol', 'name']})
    df_merged_files= pd.merge(df, data, on=['id','symbol','name'], how='inner')
    df_merged_files = df_merged_files.rename(columns = {'id':'token_id', 'symbol':'token_symbol', 'name':'token_name'})
    df_merged_files['token_symbol'] = df_merged_files['token_symbol'].str.upper()
    df_merged_files.dropna(how='all', axis=1, inplace=True)

    # filter to tokens in TOKEN table, fills NaNs with None
    df_merged_files = df_merged_files[df_merged_files['token_symbol'].isin(TOKEN['token_symbol'])].reset_index(drop=False)
    df_merged_files = df_merged_files.astype(object).where(pd.notnull(df_merged_files), None )
    df_merged_files['circulating_supply'] = df_merged_files.circulating_supply.apply(Decimal)
    df_merged_files['total_supply'] = df_merged_files.circulating_supply.apply(Decimal)
    df_merged_files['max_supply'] = df_merged_files.circulating_supply.apply(Decimal)
    return df_merged_files[['token_name','token_symbol','ethereum_contract_hash','polygon_contract_hash','avalanche_contract_hash','solana_contract_hash','circulating_supply','total_supply','max_supply']]

# makes call to CoinGecko to grab token information for Top 300 tokens by MarketCap
token_data = get_token_data()

# creates token_table
create_token_table()

######### Insert ethereum_contract_hash, circulating_supply, total_supply and max_supply ############
insert_supply_info(token_data)
insert_contract_hashes(token_data)