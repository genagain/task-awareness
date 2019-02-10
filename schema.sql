DROP TABLE IF EXISTS cards;

CREATE TABLE cards (
  id serial PRIMARY KEY, 
  datetime TIMESTAMPTZ NOT NULL, 
  board_id VARCHAR (40) NOT NULL, 
  card_id VARCHAR (40) NOT NULL UNIQUE, 
  card_name VARCHAR (50) NOT NULL
);
