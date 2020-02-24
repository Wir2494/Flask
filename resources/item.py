import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Items(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {"items": items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store ID")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            return item.json()

        return {'message': "Item doesn't exist. Please try another one."}, 404

    def post(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            return {'message': "Item with name {} already exists. Please try another one.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)

        try:
            item.save_to_database()
        except:
            return {'message': 'An error occured during the insertion of the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            item.delete_from_database()

        return {'message': 'Item deleted!'}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(
                name, **request_data)
        else:
            item.price = request_data['price']

        item.save_to_database()

        return item.json()
