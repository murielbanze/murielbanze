-- This is an empty sql file for the flyway baseline
CREATE TABLE token (token_id INT,
                    token_name VARCHAR(256) NOT NULL,
                    token_symbol VARCHAR(256) NOT NULL,
                    eth_contract_hash TIMESTAMP,
                    circulating_supply FLOAT,
                    total_supply FLOAT,
                    max_supply FLOAT);


INSERT INTO token
VALUES 
(0, "0x", "ZRX", NULL, NULL, NULL, NULL),
(1, "1inch", "1INCH", NULL, NULL, NULL, NULL),
(2, "Aave",	"AAVE",  NULL, NULL, NULL, NULL),
(3, "Alchemix USD",	"ALUSD", NULL, NULL, NULL, NULL),
(4, "Alchemy Pay", "ACH", NULL, NULL, NULL, NULL),
(5, "Algorand",	"ALGO",  NULL, NULL, NULL, NULL),
(6, "Amp",	"AMP",  NULL, NULL, NULL, NULL),
(7, "Anchor Protocol", "ANC",  NULL, NULL, NULL, NULL),
(8, "Ankr",	"ANKR",  NULL, NULL, NULL, NULL),
(9, "APENFT", "NFT",  NULL, NULL, NULL, NULL),
(10, "API3", "API3",  NULL, NULL, NULL, NULL),
(11, "Aragon", "ANT",  NULL, NULL, NULL, NULL),
(12, "Ardor", "ARDR", NULL, NULL, NULL, NULL)
(13, "Arweave",	"AR", NULL, NULL, NULL, NULL),
(14, "AscendEx Token", "ASD", NULL, NULL, NULL, NULL),
(15, "Astar", "ASTR", NULL, NULL, NULL, NULL)
(16, "Audius", "AUDIO",  NULL, NULL, NULL, NULL),
(17, "Aurora", "AURORA",  NULL, NULL, NULL, NULL),
(18, "Avalanche", "AVAX",  NULL, NULL, NULL, NULL),
(19, "Axie Infinity", "AXS",  NULL, NULL, NULL, NULL),
(20, "Baby Doge Coin", "BABYDOGE",  NULL, NULL, NULL, NULL),
(21, "Bancor Network Token", "BNT",  NULL, NULL, NULL, NULL),
(22, "Band Protocol", "BAND",  NULL, NULL, NULL, NULL),
(23, "Basic Attention Token", "BAT",  NULL, NULL, NULL, NULL),
(24, "BNB",	"BNB",  NULL, NULL, NULL, NULL),
(25, "Binance USD",	"BUSD",  NULL, NULL, NULL, NULL),
(26, "Decentralized Social", "DESO",  NULL, NULL, NULL, NULL),
(27, "Bitcoin",	"BTC",  NULL, NULL, NULL, NULL),
(29, "Bitcoin Cash", "BCH",  NULL, NULL, NULL, NULL),
(30, "Bitcoin SV", "BSV",  NULL, NULL, NULL, NULL),
(31, "Ethereum", "ETH",NULL, NULL, NULL, NULL),
(32, "Solana", "SOL", NULL, NULL, NULL, NULL),
(33, "Near", "NEAR", NULL, NULL, NULL, NULL),
(34, "Helium", "HNT", NULL, NULL, NULL, NULL),
(35, "Stacks", "STX", NULL, NULL, NULL, NULL),
(36, "Litecoin", "LTC", NULL, NULL, NULL, NULL),
(37, "Dogecoin", "DOGE", NULL, NULL, NULL, NULL),
(38, "Bitcoin Cash", "BCH", NULL, NULL, NULL, NULL);

