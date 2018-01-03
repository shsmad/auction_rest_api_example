# auction_rest_api_example
Example of REST API on auctions

## Requirements

- psycopg2==2.7.3.2
- Flask==0.12.2

## Installation

1. Create database structure and role using [install script](sql/install.sql)
2. Configure cron, moving [cron script](cron/finish_auctions.cron) to /etc/cron.d/ and changing path to finish_auctions.py
3. Configure application in [config file](config/app.cfg)
4. Run either standalone app `$python2.7 /path/to/app.py` or apache virtual host, using app.wsgi

## API

Creating user:

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"username", "password":"password", "email":"email"}' http://localhost:3000/api/v1.0/account
```

Getting token for user:

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"username", "password":"password"}' http://localhost:3000/api/v1.0/account/token
```

Listing auctions:

```
curl -i -H "Content-Type: application/json" -X GET -d '{}' http://localhost:3000/api/v1.0/auction
```

Creating auction:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Token 0cf0b195-fb04-4413-be32-920c79ae654a" -X POST -d '{"description": "description", "bid_start": 100, "bid_step": 20, "finish_date": "2018-02-02 20:22:25.32"}' http://localhost:3000/api/v1.0/auction
```

Getting auction details:

```
curl -i -H "Content-Type: application/json" -X GET -d '{}' http://localhost:3000/api/v1.0/auction/1
```

Placing bid on auction:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Token 0cf0b195-fb04-4413-be32-920c79ae654a" -X POST -d '{"bid": 140}' http://localhost:3000/api/v1.0/auction/3/bid
```

## TODO

Some improvements that can be done, but *were not* indicated as critical/necessary

- Logging (currently only database errors are logged)
- Move mail sending to Flask-mail extension and optimise sending queue
- Move some sql to stored procedures
- Auctions without winners processed by cron script everytime
- Rotating and multiple tokens for user
- Show some info on DB errors to users in json
- Move some field checks to DB


## Licence
auction_rest_api_example (c) by shsmad

auction_rest_api_example is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

You should have received a copy of the license along with this work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0/
