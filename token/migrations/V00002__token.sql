CREATE TABLE token (
            token_id INT,
            token_name VARCHAR(256) NOT NULL,
            token_symbol VARCHAR(12) NOT NULL,
            ethereum_contract_hash VARCHAR(256),
            polygon_contract_hash VARCHAR(256),
            avalanche_contract_hash VARCHAR(256),
            solana_contract_hash VARCHAR(256),
            circulating_supply DECIMAL(45,25),
            total_supply DECIMAL(45,25),
            max_supply DECIMAL(45,25))