curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test", "password":"test", "email":"test@localhost"}' http://localhost:3000/api/v1.0/account
# 0cf0b195-fb04-4413-be32-920c79ae654a

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test1", "password":"test1", "email":"test1@localhost"}' http://localhost:3000/api/v1.0/account
# 00d01ed2-b410-4fe2-986f-d2891b00af59

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test2", "password":"test2", "email":"test2@localhost"}' http://localhost:3000/api/v1.0/account
# 18801f9a-37f2-466c-846e-52cb16a9c2f7

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"shsmad", "password":"shsmad"}' http://localhost:3000/api/v1.0/account/token

curl -i -H "Content-Type: application/json" -X GET -d '{}' http://localhost:3000/api/v1.0/auction

curl -i -H "Content-Type: application/json" -H "Authorization: Token 0cf0b195-fb04-4413-be32-920c79ae654a" -X POST -d '{"description": "d1", "bid_start": "140", "bid_step": "20", "finish_date": "2018-02-02 20:22:25.32"}' http://localhost:3000/api/v1.0/auction

curl -i -H "Content-Type: application/json" -X GET -d '{}' http://localhost:3000/api/v1.0/auction/1

curl -i -H "Content-Type: application/json" -H "Authorization: Token 0cf0b195-fb04-4413-be32-920c79ae654a" -X POST -d '{"bid": 150}' http://localhost:3000/api/v1.0/auction/3/bid
curl -i -H "Content-Type: application/json" -H "Authorization: Token 00d01ed2-b410-4fe2-986f-d2891b00af59" -X POST -d '{"bid": 150}' http://localhost:3000/api/v1.0/auction/3/bid
curl -i -H "Content-Type: application/json" -H "Authorization: Token 00d01ed2-b410-4fe2-986f-d2891b00af59" -X POST -d '{"bid": 140}' http://localhost:3000/api/v1.0/auction/3/bid
curl -i -H "Content-Type: application/json" -H "Authorization: Token 00d01ed2-b410-4fe2-986f-d2891b00af59" -X POST -d '{"bid": 160}' http://localhost:3000/api/v1.0/auction/3/bid
curl -i -H "Content-Type: application/json" -H "Authorization: Token 18801f9a-37f2-466c-846e-52cb16a9c2f7" -X POST -d '{"bid": 160}' http://localhost:3000/api/v1.0/auction/3/bid
