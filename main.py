from database import (
    create_account,
    get_accounts,
    deposit_money,
    withdraw_money,
    get_transaction_history
)
accounts = {}


def show_menu():
    print("\n===== WELCOME TO THE BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. View Accounts")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transaction History")
    print("6. Exit")


while True:
    show_menu()

    choice = input("Enter your choice: ").strip()

    
    # 1. Create Account
    if choice == '1':
       name = input("Enter account holder's name: ").strip()

       if not name:
        print("Account holder name cannot be empty.")
        continue

       try:
        account_number = create_account(name)

        print("\nAccount created successfully!")
        print(f"Your account number is {account_number}")
        print(f"Account Holder: {name}")
        print("Balance: Rs. 0.00")

       except Exception as error:
        print("Account creation failed:", error)
    
    # 2. View Accounts
    elif choice == '2':
        try:
            accounts = get_accounts()

            if not accounts:
                print("No accounts found.")
            else:
                print("\n===== ALL BANK ACCOUNTS =====")

                for account in accounts:
                    account_number, name, balance = account

                    print(f"\nAccount Number: {account_number}")
                    print(f"Account Holder: {name}")
                    print(f"Balance: Rs. {balance:.2f}")
                    print("-----------------------------")

        except Exception as error:
            print("Unable to retrieve accounts:", error)

    
    # 3. Deposit Money
    elif choice == '3':
        try:
            account_number = int(
                input("Enter your account number: ")
            )

            amount = float(
                input("Enter deposit amount: Rs. ")
            )

            if amount <= 0:
                print("Deposit amount must be greater than zero.")
                continue

            result = deposit_money(account_number, amount)

            if result is None:
                print("Account not found.")
                continue

            name, balance = result

            print("\nDeposit successful!")
            print(f"Account Holder: {name}")
            print(f"Deposited Amount: Rs. {amount:.2f}")
            print(f"Available Balance: Rs. {balance:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

        except Exception as error:
            print("Deposit failed:", error)

    
    # 4. Withdraw Money
    elif choice == '4':
        try:
            account_number = int(
                input("Enter your account number: ")
            )

            amount = float(
                input("Enter withdrawal amount: Rs. ")
            )

            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
                continue

            result = withdraw_money(account_number, amount)

            if result == "not_found":
                print("Account not found.")
                continue

            if result == "insufficient_balance":
                print("Insufficient balance.")
                continue

            name, balance = result

            print("\nWithdrawal successful!")
            print(f"Account Holder: {name}")
            print(f"Withdrawn Amount: Rs. {amount:.2f}")
            print(f"Available Balance: Rs. {balance:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

        except Exception as error:
            print("Withdrawal failed:", error)

   
    
    # 5. Transaction History
    elif choice == '5':
        try:
            account_number = int(
                input("Enter your account number: ")
            )

            accounts = get_accounts()

            account = next(
                (acc for acc in accounts if acc[0] == account_number),
                None
            )

            if account is None:
                print("Account not found.")
                continue

            transactions = get_transaction_history(account_number)

            print("\n===== TRANSACTION HISTORY =====")
            print(f"Account Holder: {account[1]}")
            print(f"Account Number: {account_number}")

            if not transactions:
                print("No transactions found.")
            else:
                for index, transaction in enumerate(transactions, start=1):
                    transaction_type, amount, transaction_date = transaction

                    print(f"\nTransaction {index}")
                    print(f"Type: {transaction_type}")
                    print(f"Amount: Rs. {amount:.2f}")
                    print(f"Date: {transaction_date}")

            print(f"\nCurrent Balance: Rs. {account[2]:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid account number.")

        except Exception as error:
            print("Unable to retrieve transaction history:", error)

    # 6. Exit
    elif choice == '6':
        print("Thank you for using our Bank!")
        break

    # Invalid Choice
    else:
        print("Invalid choice. Please try again.")