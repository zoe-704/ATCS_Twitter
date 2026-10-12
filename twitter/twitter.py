from account_manager import AccountManager, AgeTooLowError
from post_manager import PostManager
from user import AlreadyFollowingError, NotFollowingError, SelfFollowError
from search import Search
from post import Post

class Twitter:
    def __init__(self):
        self.accounts = AccountManager()
        self.posts = PostManager()
        self.search = Search(self.accounts, self.posts)

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

    def show_main_menu(self):
        me = self.accounts.current_user
        print(f"\nLogged in as @{me.username}")
        print("1. See who I follow and who follows me")
        print("2. Delete my account")
        print("3. Search for account (to follow/unfollow an account)")
        print("4. Write a post")
        print("5. View all posts")
        print("6. Delete one of my posts")
        print("7. View a profile")
        print("0. Log out")

        choice = input("Pick an option: ")

        if choice == "1":
            self.view_my_follows()

        elif choice == "2":
            self.delete_my_account()

        elif choice == "3":
            self.search_for_account()

        elif choice == "4":
            self.write_post()

        elif choice == "5":
            self.view_all_posts()

        elif choice == "6":
            self.delete_my_post()

        elif choice == "7":
            self.view_profile()

        elif choice == "0":
            self.accounts.logout()
            print("Logged out.")

    # Option 1
    def view_my_follows(self):
        # View all followers and following
        me = self.accounts.current_user
        print(f"\n{len(me.following)} following | {len(me.followers)} followers")
        print ("Following:", ", ".join("@" + user.username for user in me.following) or "nobody yet")
        print ("Followers:", ", ".join("@" + user.username for user in me.followers) or "nobody yet")

    # Option 2
    def delete_my_account(self):
        # Confirm that user wants to delete their account
        confirm = input("Are you sure? Type yes to delete your account: ")
        if confirm.lower() == "yes":
            self.accounts.delete_account(self.posts)
            print("Your account was deleted.")
        else:
            print("Account not deleted.")

    # Option 3
    def search_for_account(self):
        search_text = input("Search for an account (@___): ").strip()
        if not search_text.startswith("@"):
            print("Searches for users have to start with @")
            return

        other = self.search.search_user(search_text)
        if other is None:
            print("user does not exist")
            return

        me = self.accounts.current_user
        print(f"\nFound: {other.name} (@{other.username})")
        if other is me:
            print("That's you!")
            return

        if me.is_following(other):
            answer = input(f"Do you want to unfollow @{other.username}? (yes/no): ")
        else:
            answer = input(f"Do you want to follow @{other.username}? (yes/no): ")

        if answer.lower() != "yes":
            return

        try:
            if me.is_following(other):
                self.accounts.unfollow_user(other.username)
                print(f"You unfollowed @{other.username}")
            else:
                self.accounts.follow_user(other.username)
                print(f"You followed @{other.username}")
        except(AlreadyFollowingError, NotFollowingError, SelfFollowError) as e:
            print(e)

    # Option 4
    def write_post(self):
        text = input(f"What's happening? (max {Post.MAX_POST_LENGTH} characters): ")
        try:
            post = self.posts.create_post(self.accounts.current_user, text)
            print("Posted!")
            print(post)
        except ValueError as e:
            # Post raises ValueError if the text is empty or too long
            print(e)

    # Option 5
    def view_all_posts(self):
        posts = self.posts.get_all_posts()
        if not posts:
            print("No posts yet.")
            return
        print(f"\n--- All posts ({len(posts)}) ---")
        for post in posts:
            print(post)
            print()

    # Option 6
    def delete_my_post(self):
        me = self.accounts.current_user
        if not me.posts:
            print("You haven't posted anything yet.")
            return

        # Show the user's posts so they know which IDs they can delete
        print("\nYour posts:")
        for post in reversed(me.posts):
            print(post)
            print()

        try:
            post_id = int(input("ID of the post to delete: ").lstrip("#"))
        except ValueError:
            print("Post ID has to be a number.")
            return

        try:
            self.posts.delete_post(me, post_id)
            print(f"Post #{post_id} deleted.")
        except (ValueError, PermissionError) as e:
            print(e)

    # Option 7
    def view_profile(self):
        me = self.accounts.current_user
        search_text = input("Whose profile? (@username, or press Enter for yours): ").strip()

        if search_text == "":
            user = me
        else:
            user = self.search.search_user(search_text)
            if user is None:
                print("That user doesn't exist. Usernames have to start with @")
                return

        # Profile header
        print(f"\n{user.name}")
        print(f"@{user.username}")
        print(f"{len(user.following)} following | {len(user.followers)} followers | {len(user.posts)} posts")

        if user is not me:
            if me.is_following(user):
                print("You follow this account")
            else:
                print("You don't follow this account")

        # Their posts, newest first
        print(f"\n--- Posts by @{user.username} ---")
        if not user.posts:
            print("No posts yet.")
            return
        for post in reversed(user.posts):
            print(post)
            print()

if __name__ == "__main__":
    Twitter().run()
