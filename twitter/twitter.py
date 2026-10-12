from account_manager import AccountManager, AgeTooLowError
from post_manager import PostManager
from user import AlreadyFollowingError, NotFollowingError, SelfFollowError

class Twitter:
    def __init__(self):
        self.accounts = AccountManager()
        self.posts = PostManager()

    def run(self):
        print("Welcome to Twitter!")    
        while True:
            if self.accounts.current_user is None:
                keep_going = self.show_login_menu()
                if not keep_going:
                    print("Bye!")
                    break
            else:
                self.show_main_menu()

    def show_login_menu(self):  
        # Returns False when the user picks Exit
        print("\n1. Log in")  
        print("2. Create account")        
        print("0. Exit") 
        choice = input("Pick an option: ")

        if choice == "1":
            username = input("Username: ").lstrip("@")
            password = input("Password: ")
            # Login returns true if succesful
            if self.accounts.login(username, password):
                print(f"Welcome back, {self.accounts.current_user.name}!")
            else:
                print("Wrong username or password.")

        elif choice == "2":
            username = input("Username: ").lstrip("@")
            password = input("Password: ")
            name = input("Name: ")
            try:
                age = int(input("Age: "))
                if self.accounts.create_account(username, password, name, age):
                    print("Account created! You can log in now.")
                else:
                    print("That username is taken.")
            except ValueError:
                print("Age has to be a number.")
            except AgeTooLowError as e:
                print(e)

        elif choice == "0":
            return False

        return True

    def who_main_menu(self):
        #TODO Zoe - add the posting features to the menu
        print("1. See who I follow and who follows me")
        print("2. Delete my account")
        print("0. Log out")
        choice = input("Pick an option: ")

        if choice == "1":
            self.view_my_follows()

        elif choice == "2":
            self.delete_my_account()

        elif choice == "0":
            self.accounts.logout()
            print("Logged out.")

    def delete_my_account(self):
        # Confirm that user wants to delete their account
        confirm = input("Are you sure? Type yes to delete your account: ")
        if confirm.lower() == "yes":
            self.accounts.delete_account(self.posts)
            print("Your account was delted.")
        else:
            print("Account not delted.")

    def view_my_follows(self):
        # View all followers and following
        me = self.accounts.current_user
        print(f"\n{len(me.following)} following | {len(me.followers)} followers")
        print ("Following:", ", ".join("@" + user.username for user in me.following) or "nobody yet")
        print ("Followers:", ", ".join("@" + user.username for user in me.followers) or "nobody yet")