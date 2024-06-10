import sys

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def verify_pin(self, pin):
        return self.pin == pin

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)

class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def register_user(self, user_id, pin, balance=0):
        if user_id in self.users:
            return False
        self.users[user_id] = User(user_id, pin, balance)
        return True

    def authenticate_user(self, pin):
        for user in self.users.values():
            if user.verify_pin(pin):
                self.current_user = user
                print("Authentication successful.")
                return True
        print("Authentication failed.")
        return False

    def show_transaction_history(self):
        if self.current_user:
            if not self.current_user.transaction_history:
                print("No transactions found.")
            else:
                for transaction in self.current_user.transaction_history:
                    print(transaction)
        else:
            print("No user authenticated.")

    def show_balance(self):
        if self.current_user:
            print(f"Current balance: ${self.current_user.balance}")
        else:
            print("No user authenticated.")

    def withdraw(self, amount):
        if self.current_user:
            if amount > self.current_user.balance:
                print("Insufficient funds.")
            else:
                self.current_user.balance -= amount
                self.current_user.add_transaction(f"Withdrew: ${amount}")
                print(f"${amount} withdrawn successfully.")
        else:
            print("No user authenticated.")

    def deposit(self, amount):
        if self.current_user:
            self.current_user.balance += amount
            self.current_user.add_transaction(f"Deposited: ${amount}")
            print(f"${amount} deposited successfully.")
        else:
            print("No user authenticated.")

    def transfer(self, to_user_id, amount):
        if self.current_user:
            if to_user_id not in self.users:
                print("Recipient user ID not found.")
            elif amount > self.current_user.balance:
                print("Insufficient funds.")
            else:
                self.current_user.balance -= amount
                self.users[to_user_id].balance += amount
                self.current_user.add_transaction(f"Transferred: ${amount} to {to_user_id}")
                self.users[to_user_id].add_transaction(f"Received: ${amount} from {self.current_user.user_id}")
                print(f"${amount} transferred to user {to_user_id} successfully.")
        else:
            print("No user authenticated.")

    def quit(self):
        print("Exiting the ATM system.")
        sys.exit()

def main():
    atm = ATM()

    users = [("user1", "1234", 0), ("user2", "5678", 0)]
    for user_id, pin, balance in users:
        atm.register_user(user_id, pin, balance)

    print("Welcome to the ATM")
    while True:
        print("\nPlease insert your card and then enter your PIN.")
        pin = input("Enter PIN: ")
        
        if atm.authenticate_user(pin):
            while True:
                print("\n1. Show Transaction History\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Show Balance\n6. Quit")
                choice = input("Choose an option: ")

                if choice == '1':
                    atm.show_transaction_history()
                elif choice == '2':
                    amount = float(input("Enter amount to withdraw: "))
                    atm.withdraw(amount)
                elif choice == '3':
                    amount = float(input("Enter amount to deposit: "))
                    atm.deposit(amount)
                elif choice == '4':
                    to_user_id = input("Enter recipient user ID: ")
                    if to_user_id not in atm.users:
                        print("Recipient user ID not found.")
                    else:
                        amount = float(input("Enter amount to transfer: "))
                        atm.transfer(to_user_id, amount)
                elif choice == '5':
                    atm.show_balance()
                elif choice == '6':
                    atm.quit()
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Authentication failed. Please try again.")

if __name__ == "__main__":
    main()
