import json
import bcrypt
import string
import random
from tabulate import tabulate
from datetime import datetime

class Users:
    '''users manager'''
    __logged_in = False
    priority = "Users"
    def __init__(self, filename = "users.json"):
        self.filename = filename
        self.data = self.load_users()
        self.attempts = {}

    def load_users(self):
        """Load users from JSON or create new"""
        try:
            with open(self.filename, "r") as f:
                content = f.read().strip()  
                if not content: #check if file is empty
                    return {self.priority: {}}  
                return json.loads(content)  
        except FileNotFoundError: #except FileNotFoundError:
            print("❌ File not found. Creating new...")
            return {self.priority: {}} 
        except json.JSONDecodeError:     #except json.JSONDecodeError:
            print("❌ Error: File users.json is damaged! Fixing...")
            return {self.priority: {}}
    
    def log_action(self, action):
        '''Log action'''
        with open("logs.txt", "a") as file:
            file.write(f"{datetime.now()}: {action}\n")

    def save_data(self): 
        '''Save data to json file'''
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)
    

    def hash_password(self, password):
        '''Hash password'''
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return self.password

    def verify_password(self, username, password):
        ''''Verify hashed password'''
        return self.hash_password(password) == self.data[self.priority][username]
    
    
    
    def verify_name(self, username):
        '''Verify username'''
        return username in self.data[self.priority]

    def verify_user(self, username, password):
        '''Verify users data'''
        if self.verify_name(username):
            self.data[self.priority][username] = self.hash_password(password)
            self.save_data()
            return True
        else:
            return False
    
    def limit_attempts(self, username):
        '''limit attempts'''
        if username not in self.attempts:
            self.attempts[username] = 0

        self.attempts[username] += 1

        if self.attempts[username] >= 3:
            print("❌ Too many attempts")
            return False
        return True
   
    def add_user(self, username, password):
        '''Add user'''
        if not self.verify_name(username):
            self.data[self.priority][username] = self.hash_password(password)
            self.save_data()
            self.log_action(f"{username} registered")
            return True
        else:
            print("User already exists")
            self.log_action(f"❌ {username} failed to register")
            return False
    
    def login(self, username, password):
        '''Login to account'''
        if not self.limit_attempts(username):
            return False

        if self.verify_user(username, password):
            self.__logged_in = username
            print(f"✅ Welcome, {username}!")
            self.log_action(f"{username} logged in")
            return True
        else:
            print("❌ Invalid data")
            return False


    def logout(self):
        '''logout'''
        self.logged_in = False
        self.log_action(f"{self.logged_in} logged out")
        return True
    
    def delete_user(self, username):
        '''delete user'''
        if self.logged_in == username:  #check if user is logged in and can delete account
            del self.data[self.priority][username]
            self.save_data()
            self.log_action(f"✅ {username} deleted their account")
            return True
        else:
            self.log_action(f"❌ {username} failed to delete their account")
            return "At first login,then you can delete your account"

    def user_exit(self):
        '''user exit'''
        self.logged_in = False #logout user
        self.log_action(f"{self.logged_in} logged out")
        return True
    def generate_password(self, length = random.randint(8, 12)):
        '''generate password'''
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    

class Admin(Users):
    '''admin'''
    priority = "Admins"
    __logged_in = False
    
    
    def __init__(self, filename = "users.json"):
        super().__init__(filename)
        self.load_users()

    def login(self, username, password):
        '''login'''
        if not self.limit_attempts(username):
            return False

        if self.verify_user(username, password):
            self.__logged_in = username
            print(f"✅ Welcome, {username}!")
            self.log_action(f"{username} logged in")
            return True

    def change_user_password(self, username, password):
        '''Change user password for admin'''
        self.data[super().priority][username] = self.hash_password(password)
        self.save_data()
        self.log_action(f"{username} changed their password")
        return True
    

    def delete_user_for_admin(self, username):
        '''Delete user'''
        if self.verify_name(username):
            del self.data[super().priority][username]
            self.save_data()
            self.log_action(f"{username} deleted their account")
            return True
        else:
            return "User not found, please check the username"
    

    def show_users(self):
        '''Show all users'''
    
        users_data = self.data.get(super().priority, {})
        admins_data = self.data.get(self.priority, {})

        if not users_data and not admins_data:
            print("No users or admins found.")
            return

        def format_table(data, title):
            if not data:
                print(f"{title}: No data available.")
                return

            table = [(user, password) for user, password in data.items()]
            headers = ["Username", "Password"]

            print(f"\n{title}:")
            print(tabulate(table, headers=headers, tablefmt="grid"))

        format_table(users_data, "Users")
        format_table(admins_data, "Admins")
        self.log_action("Users and Admins shown")

    def change_user_priority(self, username, priority):
        '''Change user priority'''      
        self.data[priority][username] = self.data[super().priority][username]
        del self.data[super().priority][username]
        self.save_data()
        self.log_action(f"Admin changed {username} priority to {priority}")
        return True

        
        
