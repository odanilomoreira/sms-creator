from flask_restful import Resource, reqparse
from models.restaurant import RestaurantModel
from models.user import UserModel


body_request = reqparse.RequestParser()
body_request.add_argument('restaurant_name', type=str)
body_request.add_argument('restaurant_phone', type=str)
body_request.add_argument('restaurant_id', type=str)
body_request.add_argument('pickup_message', type=str)
body_request.add_argument('delivery_message', type=str)


class UsersByRestaurantId(Resource):
    def get(self,restaurant_id):
        return {'users': [user.json() for user in UserModel.query.all() if user.restaurant_id == restaurant_id]}

class Restaurants(Resource):
    def get(self):
        return {'restaurants': [restaurant.json() for restaurant in RestaurantModel.query.all()]}

class RestaurantById(Resource):
    def get(self, restaurant_id):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if restaurant:
            return restaurant.json()
        return {'message': 'Restaurant not found.'}, 404 # not found

    def put(self,restaurant_id):
        data = body_request.parse_args()
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if restaurant:
            if data.get('pickup_message'):
                restaurant.pickup_message = data.get('pickup_message')
                restaurant.save_restaurant()
                return {'message': 'Restaurant pickup message updated successfully'}, 200

            if data.get('delivery_message'):
                restaurant.delivery_message = data.get('delivery_message')
                restaurant.save_restaurant()
                return {'message': 'Restaurant delivery message updated successfully'}, 200
            
        return {'message': 'Restaurant message could not be updated'}, 404

    def delete(self, restaurant_id):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if restaurant:
            restaurant.delete_restaurant()
            return {'message':'Restaurant deleted.'}
        return {'message': 'Restaurant not found.'}, 404

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
