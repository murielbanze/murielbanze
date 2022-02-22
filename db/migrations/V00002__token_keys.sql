-- This is an empty sql file for the flyway baseline

CREATE TABLE token (token_id INT,
                    token_name VARCHAR(256) NOT NULL,
                    token_symbol VARCHAR(256) NOT NULL,
                    eth_contract_hash TIMESTAMP);


INSERT INTO token
VALUES 
(0, "Bitcoin", "BTC", NULL),
(1, "Ethereum", "ETH", NULL),
(2, "Solana", "SOL", NULL),
(3, "Near", "NEAR", NULL);