from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item (Resource):
    # parser declarartion
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every items need a store Id!"
                        )

    @jwt_required()     # decorator declaration
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not Found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}'already exists".format(name)}, 400
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # internal sever error
            return {'message': 'An Error occurred while inserting the item'}, 500

        return item.json(), 201

    # deleting an item
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    # insert/updating an item
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item .json()


class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items "
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        def get(self):
            return {'items': list(map(lambda x: x.json(), ItemModel.query_all()))}

            # return {'item':[x.json() for x in ItemModel.query_all()]}
