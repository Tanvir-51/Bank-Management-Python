class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = self.generate_account_number()
        self.transaction_history = []
        self.loan_limit = 2
        self.loan_taken = 0

    def generate_account_number(self):
        return str(hash(self.email + self.name))

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
        else:
            print("Withdrawal amount exceeded")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_limit > 0:
            self.balance += amount
            self.loan_taken += amount
            self.loan_limit -= 1
            self.transaction_history.append(f"Took a loan of ${amount}")
        else:
            print("Loan limit exceeded")

    def transfer(self, recipient, amount):
        if self.balance >= amount:
            self.balance -= amount
            recipient.deposit(amount)
            self.transaction_history.append(f"Transferred ${amount} to {recipient.name}")
        else:
            print("Insufficient balance for the transfer")

class Admin:
    def __init__(self):
        self.user_accounts = []

    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        self.user_accounts.append(user)
        return user

    def delete_account(self, user):
        if user in self.user_accounts:
            self.user_accounts.remove(user)
            del user
        else:
            print("User account not found")

    def list_user_accounts(self):
        return self.user_accounts

    def check_total_balance(self):
        total_balance = sum(user.check_balance() for user in self.user_accounts)
        return total_balance

    def check_total_loan_amount(self):
        total_loan = sum(user.loan_taken for user in self.user_accounts)
        return total_loan

    def toggle_loan_feature(self, enable):
        User.loan_limit = 2 if enable else 0

def login_as_admin():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == "admin" and password == "123":
        return True
    else:
        print("Invalid credentials.")
        return False

def main():
    admin = Admin()
    users = []

    while True:
        print("\nWelcome to the Banking Management System")
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nUser Login")
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type (Savings/Current): ")

            user = admin.create_account(name, email, address, account_type)
            users.append(user)

            while True:
                print("\nUser Menu")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Check Transaction History")
                print("5. Take a Loan")
                print("6. Transfer Money")
                print("7. Logout")

                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    amount = float(input("Enter the amount to deposit: "))
                    user.deposit(amount)
                    print("Deposited successfully.")

                elif user_choice == "2":
                    amount = float(input("Enter the amount to withdraw: "))
                    user.withdraw(amount)

                elif user_choice == "3":
                    print("Current Balance:", user.check_balance())

                elif user_choice == "4":
                    history = user.check_transaction_history()
                    print("Transaction History:")
                    for entry in history:
                        print(entry)

                elif user_choice == "5":
                    amount = float(input("Enter the loan amount: "))
                    user.take_loan(amount)
                    print("Loan taken successfully.")

                elif user_choice == "6":
                    recipient_name = input("Enter recipient's name: ")
                    recipient = next((u for u in users if u.name == recipient_name), None)
                    if recipient:
                        amount = float(input("Enter the amount to transfer: "))
                        user.transfer(recipient, amount)
                    else:
                        print("Recipient does not exist.")

                elif user_choice == "7":
                    break

        elif choice == "2":
            if login_as_admin():
                while True:
                    print("\nAdmin Menu")
                    print("1. Create Account")
                    print("2. Delete User Account")
                    print("3. List User Accounts")
                    print("4. Check Total Balance")
                    print("5. Check Total Loan Amount")
                    print("6. Toggle Loan Feature")
                    print("7. Logout")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        name = input("Enter user's name: ")
                        email = input("Enter user's email: ")
                        address = input("Enter user's address: ")
                        account_type = input("Enter user's account type (Savings/Current): ")
                        admin.create_account(name, email, address, account_type)
                        print("User account created successfully.")

                    elif admin_choice == "2":
                        name = input("Enter the user's name to delete: ")
                        user_to_delete = next((u for u in users if u.name == name), None)
                        if user_to_delete:
                            admin.delete_account(user_to_delete)
                            users.remove(user_to_delete)
                            print(f"{name}'s account deleted.")
                        else:
                            print("User not found.")

                    elif admin_choice == "3":
                        user_accounts = admin.list_user_accounts()
                        print("\nUser Accounts:")
                        for user in user_accounts:
                            print(f"Account Number: {user.account_number}, Name: {user.name}")

                    elif admin_choice == "4":
                        total_balance = admin.check_total_balance()
                        print(f"Total Bank Balance: {total_balance}")

                    elif admin_choice == "5":
                        total_loan = admin.check_total_loan_amount()
                        print(f"Total Loan Amount: {total_loan}")

                    elif admin_choice == "6":
                        option = input("Enter '1' to enable or '0' to disable the loan feature: ")
                        if option == "1":
                            admin.toggle_loan_feature(True)
                            print("Loan feature enabled.")
                        elif option == "0":
                            admin.toggle_loan_feature(False)
                            print("Loan feature disabled.")

                    elif admin_choice == "7":
                        break
        elif choice == "3":
            print("Exiting the Banking Management System")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
