CREATE ROLE smedialink LOGIN ENCRYPTED PASSWORD 'md5e2995fb4c0d48f6e0e6584ea4648ac28'
  CREATEDB
   VALID UNTIL 'infinity';

-- Database: smedialink

-- DROP DATABASE smedialink;

CREATE DATABASE smedialink
  WITH OWNER = smedialink
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'ru_RU.UTF8'
       LC_CTYPE = 'ru_RU.UTF8'
       CONNECTION LIMIT = -1;

-- Schema: public

-- DROP SCHEMA public;

CREATE SCHEMA public
  AUTHORIZATION postgres;

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public
  IS 'standard public schema';

-- Table: accounts

-- DROP TABLE accounts;

CREATE TABLE accounts
(
  id serial NOT NULL,
  username character varying(255) NOT NULL,
  password character varying(255) NOT NULL,
  token uuid,
  email character varying(512) NOT NULL,
  CONSTRAINT accounts_pk_id PRIMARY KEY (id),
  CONSTRAINT accounts_unq_username UNIQUE (username)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE accounts
  OWNER TO smedialink;

-- Table: auctions

-- DROP TABLE auctions;

CREATE TABLE auctions
(
  id serial NOT NULL,
  description text NOT NULL,
  bid_start numeric NOT NULL,
  bid_step numeric NOT NULL,
  finish_date timestamp with time zone NOT NULL,
  account_id integer NOT NULL,
  win_bid_id integer,
  CONSTRAINT auctions_pk_id PRIMARY KEY (id),
  CONSTRAINT account_fk_id FOREIGN KEY (account_id)
      REFERENCES accounts (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT win_bid_fk_id FOREIGN KEY (win_bid_id)
      REFERENCES bids (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE auctions
  OWNER TO smedialink;


-- Table: bids

-- DROP TABLE bids;

CREATE TABLE bids
(
  id serial NOT NULL,
  bid_date timestamp with time zone NOT NULL DEFAULT now(),
  account_id integer NOT NULL,
  auction_id integer NOT NULL,
  bid_value numeric NOT NULL,
  CONSTRAINT bids_pk_id PRIMARY KEY (id),
  CONSTRAINT accounts_fk_id FOREIGN KEY (account_id)
      REFERENCES accounts (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT auctions_fk_id FOREIGN KEY (auction_id)
      REFERENCES auctions (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT auction_bid_value_unq UNIQUE (auction_id, bid_value)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE bids
  OWNER TO smedialink;
