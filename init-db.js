// Drop existing tables when initializing application
db = db.getSiblingDB("trading_card_shop_db");
db.users.drop();
db.shopping_cart_items.drop();
db.trading_cards.drop();
