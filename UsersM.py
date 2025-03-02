import users_manager
users = users_manager.Users()
admins = users_manager.Admin()
def admin_menu():
    if not admins.login(input("Enter username: "), input("Enter password: ")):
        print("❌ Invalid data, please try again")
        return

    while True:
        print("\n🔹 Admin menu:")
        print("1. Show users")
        print("2. Change user priority")
        print("3. Delete user")
        print("4. Exit")
        match input('Enter your choice: ').strip():
            case "1":
                admins.show_users()
            case "2":
                username = input("Enter username: ")
                priority = input("Enter priority: ")
                admins.change_user_priority(username, priority)
            case "3":
                username = input("Enter username: ")
                admins.delete_user_for_admin(username)
            case "4":
                break
            case _:
                print("❌ Invalid option")    

def main():
    while True:
        print("\n📌 Main Menu:")
        options = []
        if not users.logged_in:
            options.append("Register")
        options.append("Login")
        options.append("Logout")
        options.append("Delete User")
        options.append("Exit")
        options.append("🔹 Admin 🔹")

        # Print numbered options dynamically / remove 1 if user is logged in
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        options = []
        
    
        match input('Enter your choice: ').strip():
            case "1":
                username = input("Enter username: ")
                if input("Generate password? (y/n): ").strip() == "y":
                    password = users.generate_password()
                    print(f"Generated password: {password}")
                else:
                    password = input("Enter password: ")
                users.add_user(username, password)
            case "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                users.login(username, password)
            case "3":
                users.logout()
            case "4":
                username = input("Enter username: ")
                users.delete_user(username)
            case "5":
                users.user_exit()
            case "6":
                    admin_menu()
            case _:
                print("❌ Invalid option")



if __name__ == "__main__":
    main()
            