import json
import bcrypt
import string
import random
from tabulate import tabulate
from datetime import datetime
from time import sleep


'''Made by Luc1k1
    Version: 1.0.0
    Date: 2025-03-02
    Made for fun
    '''

class Users:
    '''users manager'''
    logged_in = False
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
    
    def verify_banned(self, username):
        '''Verify banned'''
        return username in self.data["Banned"]
    
    def clear_console(self):
        '''Clear console'''
        print("\033c", end="")

    def verify_user(self, username, password):
        '''Verify users data'''
        if self.verify_banned(username):
            print("❌ You are banned")
            sleep(3)
            self.clear_console()
            return False
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
            print(f"✅ {username} registered")
            sleep(3)
            self.clear_console()
            return True
        else:
            print("❌ User already exists")
            self.log_action(f"❌ {username} failed to register")
            return False
    
    def login(self, username, password):
        '''Login to account'''
        if not self.limit_attempts(username):
            return False
        if self.verify_banned(username):
            print("❌ You are banned")
            return False
        if self.verify_user(username, password):
            self.logged_in = username
            print(f"✅ Welcome, {username}!")
            self.log_action(f"{username} logged in")
            sleep(3)
            self.clear_console()
            return True
        else:
            print("❌ Invalid data")
            return False


    def logout(self):
        '''logout'''
        self.logged_in = False
        self.log_action(f"{self.logged_in} logged out")
        print(f"✅ {self.logged_in} logged out")
        sleep(3)
        self.clear_console()
        return True
    

    def delete_user(self, username):
        '''delete user'''
        if self.logged_in == username:  #check if user is logged in and can delete account
            del self.data[self.priority][username]
            self.save_data()
            self.log_action(f"✅ {username} deleted their account")
            print(f"✅ {username} deleted their account")
            sleep(3)
            self.clear_console()
            return True
        else:
            self.log_action(f"❌ {username} failed to delete their account")
            print("❌ At first login,then you can delete your account")
            sleep(3)
            self.clear_console()
            return False

    def user_exit(self):
        '''user exit'''
        self.logged_in = False #logout user
        self.log_action(f"{self.logged_in} logged out")
        print(f"✅ {self.logged_in} logged out")
        sleep(3)
        self.clear_console()
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
            sleep(3)
            self.clear_console()
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
            print(f"✅ {username} deleted their account")
            sleep(3)
            self.clear_console()
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

    def change_user_priority(self, username, new_priority):
        """Change user priority between Users and Admins"""
        # Determine the current priority of the user
        if username in self.data["Users"]:
            old_priority = "Users"
        elif username in self.data["Admins"]:
            old_priority = "Admins"
        else:
            print(f"❌ User {username} not found!")
            sleep(3)
            self.clear_console()
            return False

        
        if old_priority == new_priority:
            print(f"⚠️ {username} is already in {new_priority}!")
            sleep(3)
            self.clear_console()
            return False

        # Move the user to the new priority group
        self.data[new_priority][username] = self.data[old_priority][username]
        del self.data[old_priority][username]

        # Save changes
        self.save_data()
        self.log_action(f"Admin changed {username} priority from {old_priority} to {new_priority}")

        print(f"✅ {username} is now in {new_priority}!")
        sleep(3)
        self.clear_console()
        return True
    

    def ban_user(self, username):
        '''Ban user'''
        self.data["Banned"][username] = self.data[super().priority][username]
        del self.data[super().priority][username]
        self.save_data()
        self.log_action(f"{username} banned by admin")
        print(f"✅ {username} banned by admin")
        sleep(3)
        self.clear_console()
        return True
        

        
        
