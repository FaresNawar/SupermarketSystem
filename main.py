"""
This is the main project file which should be run.
"""
from classes import Settings
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Ensure file is only ran directly and not imported
if __name__ != '__main__':
    print("This file should not be imported.")
    exit(0)

# Imports
from graphics import SupermarketApplication
from classes import Item, Cart
from error_handling import error, success


def validate_int_input(acceptable_range: tuple):
    while True:
        try:
            result = int(input())
            if result not in acceptable_range:
                raise ValueError(f"{result} is out of range")
            break
        except ValueError as err:
            print("Invalid value encountered: (" + str(err) + ")")
            print("Please try again")
    return result

# Ensure program only runs when called by user
# and not another file
if __name__ == '__main__':
    # Define application settings
    program_settings = Settings("program_settings.txt")
    program_settings.load()
    Settings.clear_console()

    # Get mode value and validate it
    print('''
    Application mode:
    [1] GUI (Graphical User Interface)
    [2] CLI (Command Line Interface)
    Please make your choice now:
    ''')
    mode = validate_int_input((1, 2))

    if mode == 1:
        # GUI Mode
        myapp = SupermarketApplication()
    else:
        # CLI Mode
        choice = 0
        selected_cart = None
        carts = {}
        product_catalog = program_settings.load_products("data.json")

        options = {
            1: "Create Cart",
            2: "Select Cart",
            3: "List Carts",
            4: "List Products",
            5: "Add Product",
            6: "Remove Product",
            7: "View Receipt",
            8: "Print Receipt",
            9: "Exit"
        }
        while choice != len(options):
            Settings.clear_console()
            for index in options.keys():
                print(f"[{index}] {options[index]}")

            choice = validate_int_input(tuple(range(1, len(options) + 1)))
            Settings.clear_console()

            if choice in [5, 6, 7, 8] and not selected_cart:
                error("You have not selected a cart!")
                continue

            if choice in [6, 7, 8] and selected_cart.is_empty():
                error(f"The selected cart '{selected_cart.get_name()}' is empty!")
                continue

            if choice == 1:
                while True:
                    try:
                        new_cart_name = input("Give the cart a unique name: ")
                        if new_cart_name in carts.keys():
                            raise KeyError("This cart already exists! Try a different name")
                        break
                    except KeyError as e:
                        error(e)

                new_cart_index = program_settings.get_receipt_number()
                new_cart = Cart(new_cart_index, new_cart_name)
                carts.update({new_cart_name: new_cart})
                program_settings.increment_receipt_number()
                selected_cart = new_cart
                success(f"Created and selected cart {new_cart_name} successfully!")

            elif choice == 2:
                if not carts:
                    error("No carts in system. Create some carts first")
                    continue

                try:
                    cart_name = input("Input the name of a cart: ")
                    if cart_name not in carts.keys():
                        raise KeyError
                except KeyError:
                    error("This cart doesn't exist! Try checking the list of carts")
                    continue

                selected_cart = carts[cart_name]
                success(f"Selected cart {cart_name} successfully!")

            elif choice == 3:
                if not carts:
                    error("No carts in system. Create some carts first")
                    continue

                print("CART ID".ljust(10) + " | " + "CART NAME".ljust(20))
                for cart in carts.keys():
                    print(f"{carts[cart].get_index():,}".rjust(10, '0') + " | " + carts[cart].get_name().ljust(20))
                success()

            elif choice == 4:
                print("IDENTIFIER".ljust(5) + " | " + "PRODUCT NAME".ljust(40) + " | " + "PRICE".ljust(10))
                for product in product_catalog:
                    print(str(product["product_identifier"]).rjust(5, '0') + " | " + product["product_name"].ljust(40) + " | " + str(product["price"]).ljust(10) + " | ")
                success()

            elif choice == 5:
                identifier = int(input("Input product identifier: "))

                product: dict = {}
                for product in product_catalog:
                    if identifier == product["product_identifier"]:
                        break

                if product == {}:
                    error("Product doesn't exist")
                    break

                print("Adding product:", product["product_name"])

                # amt = int(input("Input amount: "))
                print("Input amount: ")
                amt = validate_int_input(tuple(range(1, 101)))

                selected_cart.insert_item(product["product_name"], product["price"], amt)
                success(f"Successfully added {amt} {product["product_name"]} to cart {selected_cart.get_name()}!")

            elif choice == 6:
                name = input("Input product identifier: ").upper()
                item = selected_cart.find_item(name)
                if item is None:
                    error("Item does not exist in cart.")
                    continue

                print("Input amount to remove: ")
                amount = validate_int_input(tuple(range(0, selected_cart.get_item_amount(name) + 1)))
                selected_cart.remove_item(name, amount)

            elif choice == 7:
                selected_cart.view_receipt()
                success()

            elif choice == 8:
                selected_cart.write_receipt_to_file("receipt.txt")
                success("Your receipt has been printed to a file 'receipt.txt'!")