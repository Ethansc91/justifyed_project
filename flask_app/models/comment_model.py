from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model


class Comment:
    db = 'justifyed_music_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    
    @classmethod
    def save_comment_with_user(cls, data):
        query = """INSERT INTO comments(content, rating, user_id)
        VALUES(%(content)s,%(rating)s,%(user)s)"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_comment(cls, id):
        query = """DELETE FROM comments WHERE comments.id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, {'id':id})
    
    @classmethod
    def get_comments_with_user(cls):
        query = """SELECT * FROM comments
        LEFT JOIN users on comments.user_id = users.id
        ORDER BY comments.created_at DESC"""
        results = connectToMySQL(cls.db).query_db(query)
        all_comments = []
        for row in results:
            one_comment = cls(row)
            one_comment_users_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'description': row['description'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            author = user_model.User(one_comment_users_info)
            one_comment.creator = author
            all_comments.append(one_comment)
        return all_comments
    


    @staticmethod
    def validate_comments(data):
        is_valid = True
        if len(data['content']) == 0:
            flash("Comment can't be blank", 'comments')
            is_valid = False
        elif data['rating'] == 'Rate':
            flash('Please leave a rating', 'rating')
            is_valid = False
        return is_valid
