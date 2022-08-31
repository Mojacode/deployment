from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Tree:
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.dateplanted = data['dateplanted']
        self.users_id = data['users_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        

    @classmethod
    def save_tree(cls,data):
        query = "INSERT INTO trees.trees (species, location, reason , dateplanted , users_id, created_at, updated_at) VALUES (%(species)s,%(location)s,%(reason)s ,%(dateplanted)s, %(users_id)s, NOW(),NOW());"
        return connectToMySQL("trees").query_db(query, data)

    @classmethod
    def update_tree(cls,data):
        query = "UPDATE trees.trees SET species=%(species)s, location=%(location)s, reason=%(reason)s, dateplanted=%(dateplanted)s, updated_at= NOW() WHERE id = %(id)s;"
        return connectToMySQL("trees").query_db(query, data)

    @classmethod
    def update_visitors(cls,data):
        query = "INSERT INTO trees.treeVisitors (trees_id, users_id) VALUES (%(id)s, %(users_id)s);"
        return connectToMySQL("trees").query_db(query, data)
    
    @classmethod
    def count_visitors(cls,data):
        query = "SELECT COUNT(users_id) from treevisitors where trees_id =  %(id)s;"
        return connectToMySQL("trees").query_db(query, data)


    @classmethod
    def get_all(cls, data):
        query = "SELECT * from trees LEFT JOIN users on users.id = trees.users_id; "
        results = connectToMySQL("trees").query_db(query,data)
        all_trees = []
        for tree in results:
            print(tree)
            all_trees.append(cls(tree))
        return all_trees

    @classmethod
    def get_all_from_user(cls, data):
        query = "SELECT *, COUNT(*) AS visitor from trees.trees LEFT JOIN users on users.id = trees.trees.users_id WHERE users.id = %(users_id)s GROUP BY trees.id ;"
        results = connectToMySQL("trees").query_db(query,data)
        all_trees = []
        for tree in results:
            print(tree)
            all_trees.append(cls(tree))
        return all_trees

    @classmethod
    def get_one(cls, data):
        query = "SELECT * from trees LEFT JOIN users on users.id = trees.users_id WHERE trees.id = %(id)s"
        results = connectToMySQL("trees").query_db(query,data)
        return cls(results[0])

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM trees.trees WHERE id = %(id)s;"
        return connectToMySQL('trees').query_db(query,data)