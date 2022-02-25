
from unicodedata import name
import pandas as pd
import requests
import numpy as np
import json
import time

TOKEN = {"token_id" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
"token_name": ["0x", "1inch", "Aave", "Alchemix USD", "Alchemy Pay", "Algorand", "Amp", "Anchor Protocol", "Ankr", "APENFT", "API3", "Aragon", "Ardor", "Arweave", "AscendEx Token", "Astar", "Audius", "Aurora", "Avalanche", "Axie Infinity", "Baby Doge Coin", 
 "Bancor Network Token", "Band Protocol", "Basic Attention Token", "BNB", "Binance USD", "Decentralized Social", "Bitcoin", "Bitcoin Cash", "Bitcoin SV", "Ethereum", "Solana", "Near", "Helium", "Stacks", "Litecoin", "Dogecoin"],
"token_symbol": ["ZRX", "1INCH", "AAVE", "ALUSD", "ACH", "ALGO", "AMP", "ANC", "ANKR", "NFT", "API3", "ANT", "ARDR", "AR", "ASD", "ASTR", "AUDIO", "AURORA", "AVAX", "AXS", "BABYDOGE", "BNT", "BAND", "BAT", "BNB", "BUSD", "DESO", "BTC", "BCH", "BSV", "ETH", "SOL", "NEAR", "HNT", "STX", "LTC", "DOGE"],
"ethereum_contract_hash": [None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None ],
"circulating_supply": [None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None ],
"total_supply": [None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None ],
"max_supply": [None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None ]}

TOKEN = pd.DataFrame(TOKEN)



df = pd.read_json("https://api.coingecko.com/api/v3/coins/list?include_platform=true")
urls = ['https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page={}'.format(i) for i in [1,2,3]]

eth_main_url = "https://api.etherscan.io/api?module=contract&action=getabi"
api_key = "VTEKW5DXBGIGAQXCD17HCR5SVJYW2YN57U"


def get_token_data(df, urls):

    calls = [requests.get(url) for url in urls]
    data = pd.concat([pd.DataFrame(call.json()) for call in calls]).reset_index()
    data = data[['index', 'id', 'symbol', 'name', 'circulating_supply', 'total_supply',
        'max_supply', 'ath', 'ath_date', 'atl', 'atl_date', 'last_updated']]

    df_normalize = pd.json_normalize(df['platforms'])
    df = pd.concat([df,df_normalize], axis = 1).drop(columns='platforms')


    df.columns = df.columns.str.replace('-','_')
    df = df.rename(columns={col: col+'_contract_hash' 
                            for col in df.columns if col not in ['id', 'symbol', 'name']})
    df_merged_files= pd.merge(df, data, on=['id','symbol','name'], how='inner')
    df_merged_files['symbol'] = df_merged_files['symbol'].str.upper()
    df_merged_files.dropna(how='all', axis=1, inplace=True)
    df_merged_files = df_merged_files[['id','symbol','name','polygon_pos_contract_hash','ethereum_contract_hash',
    'avalanche_contract_hash','solana_contract_hash', 'circulating_supply','total_supply','max_supply','ath','ath_date','atl',
    'atl_date','last_updated']]
    pd.DataFrame.to_csv(df_merged_files, 'Top_300_tokens.csv', sep=',', na_rep= 'NaN', index=False)

    return df_merged_files



def get_abi(eth_main_url, api_key, df_merged_files,):

    eth_col = df_merged_files['ethereum_contract_hash'][~df_merged_files['ethereum_contract_hash'].isna()].reset_index(drop=True)  
    
    session = requests.Session()
    contracts = pd.DataFrame()

    for i in eth_col:
        time.sleep(0.5)
        url_getABI = eth_main_url + '&address=' + str(i) + '&apikey=' + api_key
        json_data = session.get(url_getABI).json()
        if json_data['message'] == 'OK':
            dataframe = pd.json_normalize(json.decoder.JSONDecoder().decode(json_data['result']))
            dataframe['ethereum_contract_hash'] = i
            contracts = pd.concat([contracts, dataframe])

    #pd.DataFrame.to_csv(contracts,'contract_abi2.csv', mode='a', index=False)
    return contracts 

token_data = get_token_data(df, urls)


#contract_abi = get_abi(eth_main_url, api_key, token_data)
#print(contract_abi['ethereum_contract_hash'])

#df2 = token_data[['ethereum_contract_hash','circulating_supply','total_supply','max_supply']]


df2 = token_data[token_data ['symbol'].isin(TOKEN['token_symbol'])].reset_index(drop=False)
df2 = df2[['name','symbol','ethereum_contract_hash','circulating_supply','total_supply','max_supply']]
df2 = df2.astype(object).where(pd.notnull(df2), None )


