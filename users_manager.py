import json
import hashlib

class Users:
    '''users manager'''
    logged_in = False
    def __init__(self, filename = "users.json"):
        self.filename = filename
        self.data = self.load_users()

    def load_users(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"Users": {}}
    
    def save_data(self): 
        '''save data to json file'''
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)
    

    def hash_password(self, password):
        '''hash password'''
        return hashlib.sha256(password.encode()).р2
    
    def verify_password(self, username, password):
        ''''verify hashed password'''
        return self.hash_password(password) == self.data["Users"][username]
    
    
    
    def verify_name(self, username):
        '''verify username'''
        try:
            return username in self.data["Users"]
        except KeyError:
            return 'User not found'

    def verify_user(self, username, password):
        '''verify users data'''
        if self.verify_name(username):
            self.data["Users"][username] = self.hash_password(password)
            self.save_data()
            return True
        else:
            return False
    
    
   
   
    def add_user(self, username, password):
        '''add user'''
        if not self.verify_user(username):
            self.data["Users"][username] = self.hash_password(password)
            self.save_data()
            return True
        else:
            print("User already exists")
            return False
    
    def login(self, username, password):
        '''login'''
        if self.verify_user(username, password):
            self.logged_in = username
            return True
        else:
            return False
    def logout(self):
        '''logout'''
        self.logged_in = False
        return True
    
    def delete_user(self, username):
        '''delete user'''
        if self.logged_in == username:
            del self.data["Users"][username]
            self.save_data()
            return True
        else:
            return False

        
