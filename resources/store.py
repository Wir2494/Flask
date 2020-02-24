from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_item_by_name(name)

        if store:
            return store.json()

        return {'message': "Store could not be found"}, 404

    def post(self, name):
        if StoreModel.find_item_by_name(name):
            return {'message': "A store with the name {} already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_database()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            store.delete_from_database()

        return {'message': 'Store deleted'}


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
