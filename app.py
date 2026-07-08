import json
import os
from datetime import datetime, timedelta

if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        expense_list = json.load(f)
    print("Existing file loaded.")
else:
    expense_list = []
    print("Fresh file started.")



print("Welcome to Budget Calculator!")
print()

def overview():
    print("What action would you like to complete?")
    print("1) Add Expense")
    print("2) Delete Expense")
    print("3) Clear Expenses")
    print("4) Find Next Billing Payment")
    print("5) Calculate Total")
    print("6) Categorical Search")
    print("7) View History")
    print("8) Close Application")
    print()

    user_action = input("Please enter a number 1-8: ")
    while user_action not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        user_action = input("Please enter a number 1-8: ")
    print()

    return user_action

def add_expense():
    global expense_list

    name = input("Name: ").lower()
    
    while True:
        try:
            price = float(input("Price: $"))
            break
        except ValueError:
            print("Please enter a valid number.")

    category = input("Category (Food/Transportation/Entertainment/Shopping/Subscription): ").lower()
    while category != "food" and category != "transportation" and category != "entertainment" and category != "shopping" and category != "subscription":
        category = input("Please enter 'food' or 'transportation' or 'entertainment' or 'shopping' or 'subscription'! ").lower()

    expense_type = input("Expense Type (Recurring/One-time): ").lower()
    while expense_type != "recurring" and expense_type != "one-time":
        expense_type = input("Please enter 'recurring' or 'one-time'! ").lower()
    
    bill_type = "none"
    if expense_type == "recurring":
        bill_type = input("Is this bill paid weekly or monthly? ").lower()
        while bill_type != "weekly" and bill_type != "monthly":
            bill_type = input("Please enter 'weekly' or 'monthly'! ").lower()

    date = datetime.now().strftime("%m/%d/%Y")
    item = {"name" : name,
            "price" : price,
            "category" : category,
            "expense_type" : expense_type,
            "bill_type": bill_type,
            "date" : date
    }

    expense_list.append(item)
    print("The expense had been added!")
    print()

def delete_expense():
    global expense_list

    req_entity = input("What is the name of the expense you'd like to delete? ").lower()

    if len(expense_list) == 0:
        print("There are no items to be deleted!")
    
    found = False

    for item in expense_list:
        if item["name"] == req_entity:
            expense_list.remove(item)
            found = True
            break

    if found:
        print("Item deleted.")
    else:
        print("Item not found.")

    print()

def clear_expenses():
    global expense_list
    
    confirm = input("Are you sure you want to clear your expense history (y/n)? ").lower()

    while confirm != "y" and confirm != "n":
        confirm = input("Please enter 'y' or 'n'! ").lower()

    if confirm == "y":
        expense_list.clear()
        print("Expense history cleared.")
    elif confirm == "n":
        print("Expense history still active")

    print()

def next_billing_payment():
    global expense_list

    req_entity = input("What is the name of the bill you'd like to find the next payment date of? ").lower()

    if len(expense_list) == 0:
        print("You have no expenses!")
        return
    
    found = False
    recurring = False

    for item in expense_list:
        if item["name"] == req_entity:
            base_date = datetime.strptime(item["date"], "%m/%d/%Y")
            if item["bill_type"] == "monthly":
                next_date = base_date + timedelta(days=30)
                recurring = True
            elif item["bill_type"] == "weekly":
                next_date = base_date + timedelta(days=7)
                recurring = True
            elif item["bill_type"] == "none":
                print("This item is not a recurring bill.")
                recurring = False

            found = True
            break

    if found and recurring:
        print(f"The next payment date is {next_date}.")
    elif found == False:
        print("Item not found.")

    print()

def calculate_total():
    total = 0

    if len(expense_list) == 0:
        print("No expenses have been added yet!")
    else:
        for item in expense_list:
            total += item["price"]
    
    print(f'The total is ${total}.')
    print()

def categorical_search():
    global expense_list

    req_category = input("What is the name of the category you'd like to search? ").lower()

    if len(expense_list) == 0:
        print("You have no expenses!")
        return
    
    req_items = []

    for item in expense_list:
        if item["category"] == req_category:
            req_items.append(item["name"])

    if req_items:
        print(f"The items in your requested category are {req_items}.")
    else:
        print("There are either no items in that category or that category does not exist!")

    print()


def view_history():
    print("History: ")
    print(expense_list)
    print()


decision = overview()
while decision != "8":
    if decision == "1":
        add_expense()
    elif decision == "2":
        delete_expense()
    elif decision == "3":
        clear_expenses()
    elif decision == "4":
        next_billing_payment()
    elif decision == "5":
        calculate_total()
    elif decision == "6":
        categorical_search()
    elif decision == "7":
        view_history()
    decision = overview()

if decision == "8":
    with open("data.json", "w") as f:
        json.dump(expense_list, f)

print("Have a nice day!")
