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
                if users.verify_name(username):
                    priority = input("Enter priority: ")
                    admins.change_user_priority(username, priority)
                else:
                    print("❌ Invalid username, please check the username")
            case "3":
                username = input("Enter username: ")
                admins.delete_user_for_admin(username)
            case "4":
                break
            case _:
                print("❌ Invalid option")    

def main():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Delete user")
        print("5. Exit")
        print("6. Admin")
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
            