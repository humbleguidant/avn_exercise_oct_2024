from configs.config import get_db

class TradingCard:

    def __init__(self):
        self.db = get_db()
        self.collection = self.db['trading_cards']

    def get_cards(self, email):
        response = {}
        fetch = {"email": email}
        try:
            cards = self.collection.find(fetch)
            results = list(cards)
            if len(results) == 0:
                response['has_cards'] = False
                return response
            response['has_cards'] = True
            response['cards'] = [{"id": card["id"], "name": card["name"], "type": card["type"]} for card in cards]
            return response
        except:
            response['error_message'] = 'An error has occured. Please contact IT services.'
            return response