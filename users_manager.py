import json
import hashlib
import string
import random

class Users:
    '''users manager'''
    logged_in = False
    priority = "Users"
    def __init__(self, filename = "users.json"):
        self.filename = filename
        self.data = self.load_users()

    def load_users(self):
        """Load users from JSON or create new"""
        try:
            with open(self.filename, "r") as f:
                content = f.read().strip()  
                if not content: #check if file is empty
                    return {"Users": {}}  
                return json.loads(content)  
        except FileNotFoundError: #except FileNotFoundError:
            print("⚠️File not found. Creating new...")
            return {"Users": {}} 
        except json.JSONDecodeError:     #except json.JSONDecodeError:
            print("❌ Error: File users.json is damaged! Fixing...")
            return {"Users": {}}  
    
    def save_data(self): 
        '''save data to json file'''
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)
    

    def hash_password(self, password):
        '''hash password'''
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username, password):
        ''''verify hashed password'''
        return self.hash_password(password) == self.data["Users"][username]
    
    
    
    def verify_name(self, username):
        '''verify username'''
        return username in self.data["Users"]

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
        if not self.verify_name(username):
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
            print(f"Welcome {username}")
            return True
        else:
            return False
        


    def logout(self):
        '''logout'''
        self.logged_in = False
        return True
    
    def delete_user(self, username):
        '''delete user'''
        if self.logged_in == username:  #check if user is logged in and can delete account
            del self.data["Users"][username]
            self.save_data()
            return True
        else:
            return "At first login,then you can delete your account"

    def user_exit(self):
        '''user exit'''
        self.logged_in = False #logout user
        return True
    def generate_password(self, length = random.randint(8, 12)):
        '''generate password'''
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    

class Admin(Users):
    '''admin'''
    def __init__(self, filename = "users.json"):
        #super().__init__(filename)
        pass
    def change_user_password(self, username, password):
        pass
        
        
        
        
