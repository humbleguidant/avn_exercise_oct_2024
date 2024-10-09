db = db.getSiblingDB("trading_card_shop_db");
//db.trading_card_shop_tb.drop();
db.users.drop();
db.shopping_cart_items.drop();
db.trading_cards.drop();

/**db.users.insertMany([
    {
        "id": 1,
        "email": "aubreynickerson@gmail.com",
        "password": "letmein",
        "date_registered": "2024-10-06"
    }
])

db.trading_card_shop_tb.insertMany([
    {
        "id": 1,
        "name": "Lion",
        "type": "wild"
    },
    {
        "id": 2,
        "name": "Cow",
        "type": "domestic"
    },
    {
        "id": 3,
        "name": "Tiger",
        "type": "wild"
    },
]);*/