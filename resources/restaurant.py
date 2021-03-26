from flask_restful import Resource, reqparse
from models.restaurant import RestaurantModel
from models.user import UserModel


body_request = reqparse.RequestParser()
body_request.add_argument('restaurant_name', type=str, required=True, help="The field 'restaurant_name' cannot be left blank.")
body_request.add_argument('restaurant_phone', type=str, required=True, help="The field 'restaurant_phone' cannot be left blank.")
body_request.add_argument('restaurant_id', type=str, required=True, help="The field 'restaurant_id' cannot be left blank.")


class UsersByRestaurantId(Resource):
    def get(self,restaurant_id):
        return {'users': [user.json() for user in UserModel.query.all() if user.restaurant_id == restaurant_id]}

class Restaurants(Resource):
    def get(self):
        return {'restaurants': [restaurant.json() for restaurant in RestaurantModel.query.all()]}

class Restaurant(Resource):
    def get(self, restaurant_id):
        restaurant = RestaurantModel.find_restaurant(restaurant_id)
        if restaurant:
            return restaurant.json()
        return {'message': 'Restaurant not found.'}, 404 # not found

    def post(self):
        data = body_request.parse_args()
        
        if RestaurantModel.find_restaurant(data.get('restaurant_id')):
            return {"message": "The restaurant '{}' already exists."}, 400 # bad request
        restaurant = RestaurantModel(**data)
        try:
            restaurant.save_restaurant()
        except:
            return {'message': 'An internal error ocurred trying to create a new restaurant.'}, 500
        return restaurant.json()

    def delete(self, restaurant_id):
        restaurant = RestaurantModel.find_restaurant(restaurant_id)
        if restaurant:
            restaurant.delete_restaurant()
            return {'message':'Restaurant deleted.'}
        return {'message': 'Restaurant not found.'}, 404
