import users_manager

def main():
    users = users_manager.Users()
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. Delete user")
    print("5. Exit")
    while True:
        match input():
            case "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                users.add_user(username, password)
                break
            case "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                users.login(username, password)
                break
            case "3":
                users.logout()
                break
            case "4":
                username = input("Enter username: ")
                users.delete_user(username)
                break
            case "5":
                break
            case _:
                print("Invalid option")
                break



if __name__ == "__main__":
    main()
            