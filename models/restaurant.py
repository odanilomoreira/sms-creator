from sql_alchemy import db

class RestaurantModel(db.Model):
    __tablename__ = 'restaurants'

    restaurant_id = db.Column(db.String(80), primary_key=True)
    restaurant_name = db.Column(db.String(80))
    restaurant_phone = db.Column(db.String(20))
    users = db.relationship('UserModel') # users list

    def __init__(self, restaurant_id, restaurant_name, restaurant_phone):
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.restaurant_phone = restaurant_phone

    def json(self):
        return {
            'restaurant_id': self.restaurant_id,
            'restaurant_name': self.restaurant_name,
            'restaurant_phone': self.restaurant_phone,
            'users': [user.json() for user in self.users]
        }

    @classmethod
    def find_restaurant(cls, restaurant_name):
        restaurant = cls.query.filter_by(restaurant_name=restaurant_name).first()
        if restaurant:
            return restaurant
        return None

    @classmethod
    def find_by_id(cls, restaurant_id):
        restaurant = cls.query.filter_by(restaurant_id=restaurant_id).first()
        if restaurant:
            return restaurant
        return None

    def save_restaurant(self):
        db.session.add(self)
        db.session.commit()

    def delete_restaurant(self):
        # deleting all users associated with the restaurant
        [user.delete_user() for user in self.users]
        # deleting  restaurant
        db.session.delete(self)
        db.session.commit()
