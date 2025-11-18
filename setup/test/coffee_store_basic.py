# Beginner-friendly Coffee Store script.
# Teaches: print, input, variables, data types & operations, if/else, while loop,
# lists, for loops, and dictionary basics.
# This simple version: no try/except, no discounts. Type 'quit' to finish ordering.

# 1) print - show a welcome message
print("Welcome to the Simple Coffee Store!")

# 2) input and variable - get customer's name (input returns a string)
customer_name = input("What is your name? ").strip()
print("Hello,", customer_name)

# 3) dictionary - menu using item name -> price
#    This shows how dictionaries store pairs (key -> value).
menu = {
    "Espresso": 2.50,
    "Americano": 3.00,
    "Latte": 3.50,
    "Cappuccino": 3.75,
    "Tea": 2.00
}

# 4) show the menu (for loop + enumerate) - list of (key, value) from dict.items()
print("\nToday's menu:")
menu_items = list(menu.items())   # list of (name, price) tuples
for i, (name, price) in enumerate(menu_items, start=1):
    print(f"{i}. {name} - ${price:.2f}")

# 5) prepare an empty order (list) and a total (float)
#    The order list will hold dictionaries (one per distinct item).
order = []       # list to hold order lines (each line is a dict)
total = 0.0      # running total (float)

# 6) while loop - keep asking what the customer wants until they type 'quit'
while True:
    choice = input("\nWhat would you like to buy? (enter item number, name, or 'quit'): ").strip()
    if choice.lower() == "quit":
        break

    # Decide which menu item the user selected.
    item_name = None
    # If input is digits, treat as menu number
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(menu_items):
            item_name = menu_items[idx - 1][0]  # get name from tuple
        else:
            print("That item number is not on the menu. Try again.")
            continue
    else:
        # Try to match by name (case-insensitive exact match)
        for name in menu.keys():
            if choice.lower() == name.lower():
                item_name = name
                break
        if item_name is None:
            print("Couldn't find that item name. Try again.")
            continue

    # Ask for quantity (no try/except; use isdigit to check numeric)
    qty_input = input(f"How many {item_name}(s) would you like? ").strip()
    if not qty_input.isdigit():
        print("Please enter a whole number for quantity. Try again.")
        continue
    qty = int(qty_input)
    if qty <= 0:
        print("Quantity must be at least 1. Try again.")
        continue

    # Get unit price from the menu dictionary (dictionary lookup)
    unit_price = menu[item_name]    # data type: float
    line_total = unit_price * qty   # arithmetic operation (multiplication)

    # Update order list:
    # If item already in order list, update its quantity and line total.
    found = False
    for line in order:
        if line["name"].lower() == item_name.lower():
            line["qty"] += qty
            line["line_total"] = round(line["qty"] * line["price"], 2)
            found = True
            break

    if not found:
        # Append a new dictionary to the list (list append + dict)
        order.append({
            "name": item_name,
            "price": unit_price,
            "qty": qty,
            "line_total": round(line_total, 2)
        })

    # Update running total (addition)
    total += line_total
    print(f"Added {qty} x {item_name}. Current subtotal: ${total:.2f}")

# 7) If nothing ordered, exit politely
if len(order) == 0:
    print("\nNo items ordered. Thank you!")
    raise SystemExit

# 8) print receipt (for loop over list)
print("\n--- Receipt ---")
print("Customer:", customer_name)
for line in order:
    # each line is a dictionary - show name, qty, unit price and line total
    print(f"{line['name']} x{line['qty']} @ ${line['price']:.2f} = ${line['line_total']:.2f}")

# Show final total (rounded)
final_total = round(total, 2)
print(f"Total due: ${final_total:.2f}")
print("-----------------")

# 9) short summary of types and structure to reinforce learning
print("\n(For learning) Data types and collections:")
print("Type of customer_name:", type(customer_name))   # str
print("Type of final_total:", type(final_total))       # float
print("Menu keys (item names):", list(menu.keys()))     # list of keys from dict
print("Order is a list with", len(order), "distinct items.")  # len() on list
print("First order line (example):", order[0])         # list element is a dict

print("\nThank you! Goodbye!")
