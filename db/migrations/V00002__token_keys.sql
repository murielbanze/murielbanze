-- This is an empty sql file for the flyway baseline

CREATE TABLE token (token_id INT,
                    token_name VARCHAR(256) NOT NULL,
                    token_symbol VARCHAR(256) NOT NULL,
                    eth_contract_hash TIMESTAMP);

INSERT INTO token
VALUES 
(0, "Bitcoin", "BTC"),
(1, "Ethereum", "ETH"),
(2, "Solana", "SOL"),
(3, "Near", "NEAR"),
(4, "Helium", "HNT"), 
(5, "Stacks", "STX"), 
(6, "Litecoin", "LTC"),
(7, "Dogecoin", "DOGE"),
(8, "Bitcoin Cash", "BCH");