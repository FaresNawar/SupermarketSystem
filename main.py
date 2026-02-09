"""
main.py
This is the main project file which should be run.
"""
import time

# Ensure file is only ran directly and not imported
if __name__ != '__main__':
    print("This file should not be imported.")
    exit(0)

# Imports
from classes import Settings
from graphics import SupermarketApplication
from classes import Item, Cart
from error_handling import error, success


def validate_int_input(acceptable_range: tuple = None):
    while True:
        try:
            result = int(input())
            if acceptable_range and result not in acceptable_range:
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
    program_settings = Settings("program_settings.txt", [])
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
        Settings.clear_console()
        print("*" * 100)
        print("*" + "GUI MODE SELECTED - THIS TERMINAL WILL BE USED FOR LOGGING".center(98) + "*")
        print("*" + "MADE BY FARES MOSTAFA MOHAMED AL-SAYED NAWAR".center(98) + "*")
        print("*" + "THANK YOU FOR USING THIS PROGRAM :]".center(98) + "*")
        print("*" * 100)
        myapp = SupermarketApplication()
    else:
        # CLI Mode
        choice = 0
        selected_cart = None
        carts = {}
        for cart in program_settings.carts:
            carts.update({cart.get_index(): cart})
        product_catalog: list[Item] = program_settings.load_products("data.json")

        options = {
            1: "Create Cart",
            2: "Select Cart",
            3: "List Products",
            4: "Add Product",
            5: "Remove Product",
            6: "View Receipt",
            7: "Print Receipt",
            8: "Exit"
        }

        while choice != len(options):
            Settings.clear_console()
            program_settings.save(cart for cart in carts.values())

            print(f"[Selected cart: ({selected_cart.get_index()}) {selected_cart.get_name()}]" if selected_cart else "[No cart selected]")
            for index in options.keys():
                print(f"[{index}] {options[index]}")

            choice = validate_int_input(tuple(range(1, len(options) + 1)))
            Settings.clear_console()

            if choice in [4, 5, 6, 7] and not selected_cart:
                error("You have not selected a cart!")
                continue

            if choice in [5, 6, 7] and selected_cart.is_empty():
                error(f"The selected cart '{selected_cart.get_name()}' is empty!")
                continue

            if choice == 1:
                new_cart_name = input("Give the cart a name (Can be left empty): ")
                new_cart_index = program_settings.get_receipt_number()
                new_cart = Cart(new_cart_index, new_cart_name)
                carts.update({new_cart_index: new_cart})
                program_settings.increment_receipt_number()
                selected_cart = new_cart
                success(f"Created and selected cart {new_cart_name} successfully!")

            elif choice == 2:
                if not carts:
                    error("No carts in system. Create some carts first")
                    continue

                try:
                    print("CART ID".ljust(5) + " | " + "CART NAME".ljust(20))
                    for cart in carts.keys():
                        print(f"{carts[cart].get_index():,}".rjust(5, '0') + " | "
                              + carts[cart].get_name().ljust(20))

                    print("Input the index of a cart: ", end="")
                    cart_index = validate_int_input()
                    if cart_index not in carts.keys():
                        raise KeyError
                except KeyError:
                    error("This cart doesn't exist! Try checking the list of carts")
                    continue

                selected_cart = carts[cart_index]
                success(f"Selected cart {carts[cart_index].get_name()} successfully!")

            elif choice == 3:
                print("ID".ljust(5) + " | " + "PRODUCT NAME".ljust(50) + " | " + "PRICE".ljust(10))
                for product in product_catalog:
                    print(str(product.identify()).rjust(5, '0') + " | "
                          + (product.get_name() if len(product.get_name()) <= 50 else product.get_name()[0: 47] + "...").ljust(50) + " | " + str(product.get_price()).ljust(10) + " | ")
                success()

            elif choice == 4:
                inner_choice = None

                while inner_choice != 2:
                    Settings.clear_console()
                    identifier = int(input("Input product identifier: "))

                    product: Item | None = None
                    for product in product_catalog:
                        if identifier == product.identify():
                            break

                    if product is None:
                        error("Product doesn't exist")
                        break

                    print("Adding product:", product.get_name())

                    print("Input amount: ", end="")
                    amt = validate_int_input(tuple(range(1, 101)))

                    new_item = Item(product.identify(), product.get_name(), product.get_price(), amt)

                    selected_cart.insert_item(new_item, amt)
                    print(f"Successfully added {amt} {product.get_name()} to cart {selected_cart.get_name()}!")

                    print("[1] Add another product\n[2] Return to menu")
                    inner_choice = validate_int_input((1, 2))

            elif choice == 5:
                item_id = int(input("Input product identifier: "))
                item = selected_cart.find_item(item_id)
                if item is None:
                    error("Item does not exist in cart.")
                    continue

                print("Removing product:", item.get_name())
                print("Input amount to remove: ", end="")
                amount = validate_int_input(tuple(range(0, selected_cart.get_item_amount(item_id) + 1)))
                selected_cart.remove_item(item, amount)
                success(f"Successfully removed {amount} of {item.get_name()} from cart {selected_cart.get_name()}")

            elif choice == 6:
                selected_cart.view_receipt()
                success()

            elif choice == 7:
                selected_cart.write_receipt_to_file("receipt.txt")
                success("Your receipt has been printed to a file 'receipt.txt'!")
