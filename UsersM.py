import users_manager

def main():
    users = users_manager.Users()
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
                pass
            case _:
                print("Invalid option")
                print("Exiting...")
                break



if __name__ == "__main__":
    main()
            