class People:
    def __init__(self, token, audience_ids: list, address_id, location_city_id, receiver, cellphone, detail_address,
                 express_fee: dict):
        self.token = token
        self.audience_ids = audience_ids
        self.address_id = address_id
        self.location_city_id = location_city_id
        self.receiver = receiver
        self.cellphone = cellphone
        self.detail_address = detail_address
        self.express_fee = express_fee


