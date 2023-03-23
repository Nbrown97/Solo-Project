from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = 'project'
class Item:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.image_upload = data['image_upload']
        self.num_of = data['num_of']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM items JOIN users on items.user_id = users.id WHERE items.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        if not results:
            return False
        results = results[0]
        this_item = cls(results)
        user_data = {
            'id': results['users.id'],
            'first_name': results['first_name'],
            'last_name': results['last_name'],
            'email': results['email'],
            'password': "",
            'date_due': "",
            'created_at': results['users.created_at'],
            'updated_at': results['users.updated_at']
        }
        this_item.creator = user.User(user_data)
        return this_item
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items JOIN users ON items.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        items = []
        for row in results:
            this_item = cls(row)
            user_data = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'date_due': "",
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            this_item.creator = user.User(user_data)
            items.append(this_item)
        return items
    
    @staticmethod
    def validate_item(val_item):
        is_valid = True
        if len(val_item['name']) < 3:
            flash('Please enter the name of the item; must be 3 characters','item')
            is_valid = False
        if val_item['price'] == '':
            flash('Please enter the price; numbers only','item')
            is_valid = False
        if len(val_item['description']) < 1:
            flash('Please enter the description of the item','item')
            is_valid = False
        if val_item['num_of'] < "1":
            flash('Please enter how many of this item you are requesting; must display 1 or more','item')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO items (name, price, description, image_upload, num_of, user_id) VALUES (%(name)s, %(price)s, %(description)s, %(image_upload)s, %(num_of)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE items SET name = %(name)s, price = %(price)s, description = %(description)s, image_upload = %(image_upload)s, num_of = %(num_of)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def edit_no_pic(cls,data):
        query = "UPDATE items SET name = %(name)s, price = %(price)s, description = %(description)s, num_of = %(num_of)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def remove(cls, data):
        query = "DELETE FROM items WHERE id = %(id)s;"
        connectToMySQL(db).query_db(query, data)