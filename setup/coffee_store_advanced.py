# Advanced, function-based Coffee Store script with input validation (try/except).
# Teaches: functions, print, input, variables, data types, if/else, while, list, for, dictionaries.


def display_welcome():
    """Print a short welcome message."""
    print("Welcome to the Advanced Coffee Store (function-based)!")


def get_customer_name():
    """Ask for customer's name and return a stripped string."""
    name = input("What is your name? ").strip()
    return name or "Guest"  # default if empty


def build_menu():
    """Return the menu as a dictionary: name -> {price, category}."""
    return {
        "Espresso": {"price": 2.50, "category": "Coffee"},
        "Americano": {"price": 3.00, "category": "Coffee"},
        "Latte": {"price": 3.50, "category": "Coffee"},
        "Cappuccino": {"price": 3.75, "category": "Coffee"},
        "Tea": {"price": 2.00, "category": "Hot Drink"},
    }


def display_menu(menu):
    """Show menu items enumerated. Demonstrates dict iteration and enumerate (list-like view)."""
    print("\nToday's menu:")
    items = list(menu.items())  # list of (name, info)
    for idx, (name, info) in enumerate(items, start=1):
        print(f"{idx}. {name} - ${info['price']:.2f} ({info['category']})")


def parse_choice(choice, menu):
    """
    Interpret user input as item number or name.
    Returns the canonical item name or None if not found.
    """
    choice = choice.strip()
    if choice == "":
        return None

    # numeric selection
    if choice.isdigit():
        idx = int(choice) - 1
        keys = list(menu.keys())
        if 0 <= idx < len(keys):
            return keys[idx]
        return None

    # exact name (case-insensitive)
    for name in menu.keys():
        if choice.lower() == name.lower():
            return name

    # partial match (first match)
    for name in menu.keys():
        if choice.lower() in name.lower():
            return name

    return None


def get_quantity(prompt="Quantity: "):
    """
    Ask for a quantity and validate using try/except.
    Returns integer qty or None if user cancels (empty input).
    """
    raw = input(prompt).strip()
    if raw == "":
        return None
    try:
        qty = int(raw)
        if qty <= 0:
            print("Please enter a whole number greater than 0.")
            return None
        return qty
    except ValueError:
        print("Invalid number. Please enter a whole number (e.g., 1, 2).")
        return None


def add_to_order(order, menu, name, qty):
    """Add or update an item in the order list. Demonstrates list of dicts and mutation."""
    price = menu[name]["price"]
    # check existing lines (list traversal)
    for line in order:
        if line["name"].lower() == name.lower():
            line["qty"] += qty
            line["line_total"] = round(line["qty"] * line["price"], 2)
            return
    # append new line (list append + dict)
    order.append({"name": name, "price": price, "qty": qty, "line_total": round(price * qty, 2)})


def calculate_totals(order, tax_rate=0.13, discount_threshold=0.0, discount_rate=0.0):
    """
    Calculate subtotal, discount, tax, and final total.
    This shows arithmetic on floats and conditional logic (if/else).
    """
    subtotal = round(sum(line["line_total"] for line in order), 2)
    if discount_threshold > 0 and subtotal > discount_threshold:
        discount = round(subtotal * discount_rate, 2)
    else:
        discount = 0.0
    after_discount = round(subtotal - discount, 2)
    tax = round(after_discount * tax_rate, 2)
    total = round(after_discount + tax, 2)
    return {"subtotal": subtotal, "discount": discount, "after_discount": after_discount, "tax": tax, "total": total}


def print_receipt(customer, order, totals):
    """Print a neat receipt using for loop over the order list and showing totals."""
    print("\n--- Receipt ---")
    print(f"Customer: {customer}")
    for line in order:
        print(f"{line['name']} x{line['qty']} @ ${line['price']:.2f} = ${line['line_total']:.2f}")
    print(f"Subtotal: ${totals['subtotal']:.2f}")
    if totals["discount"] > 0:
        print(f"Discount: -${totals['discount']:.2f}")
    print(f"Tax: ${totals['tax']:.2f}")
    print(f"Total due: ${totals['total']:.2f}")
    print("-----------------")


def main():
    """Main program flow: build menu, take orders until 'quit', then compute and print receipt."""
    display_welcome()
    customer = get_customer_name()
    menu = build_menu()
    display_menu(menu)

    order = []

    try:
        while True:
            raw = input("\nEnter item number or name (or type 'quit' to finish): ")
            if raw.strip().lower() == "quit":
                break
            item = parse_choice(raw, menu)
            if item is None:
                print("Item not found. Try again.")
                continue

            qty = get_quantity(f"How many {item}(s)? ")
            if qty is None:
                # user entered invalid qty or empty -> ask again
                continue

            add_to_order(order, menu, item, qty)
            current_sub = round(sum(line["line_total"] for line in order), 2)
            print(f"Added {qty} x {item}. Current subtotal: ${current_sub:.2f}")

    except KeyboardInterrupt:
        # graceful exit on Ctrl+C
        print("\nOrder interrupted by user. Proceeding to checkout...")

    if not order:
        print("\nNo items ordered. Goodbye!")
        return

    # advanced settings: show how function parameters control behaviour (discount optional)
    totals = calculate_totals(order, tax_rate=0.13, discount_threshold=15.0, discount_rate=0.10)
    print_receipt(customer, order, totals)

    # brief data-type summary to reinforce learning
    print("\n(Types demonstration) customer:", type(customer), ", order:", type(order), ", totals:", type(totals))


if __name__ == "__main__":
    main()
