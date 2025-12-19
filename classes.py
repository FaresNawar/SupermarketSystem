"""
This file will hold all classes used for products, carts, etc.
"""
import os
import json

# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)

class Item:
    def __init__(self, identifier: int, product_name: str, price: float):
        self.identifier = identifier
        self.product_name = product_name
        self.price = price

    def get_name(self) -> str:
        return self.product_name

    def get_price(self) -> float:
        return self.price

    def identify(self) -> int:
        return self.identifier


class Cart:
    def __init__(self, cart_index, cart_name):
        self.index = cart_index
        self.name = cart_name
        self.items = {}
        self.item_count = 0
        self.cart_total = 0

    def insert_item(self, item_name: str, price: float, count: int):
        if count <= 0:
            return

        item = self.find_item(item_name)
        if item is None:
            item = Item(1, item_name, price)
            self.items.update({item: count})
        else:
            self.items[item] += count

        self.update()

    def remove_item(self, item_name: str, count: int):
        try:
            item = self.find_item(item_name)
            if item is None:
                raise KeyError("Item not found in cart")
            if count >= self.items[item]:
                self.items.pop(item)
            else:
                self.items[item] -= count
            self.update()
        except KeyError as e:
            print(e)

    def get_items(self):
        return self.items

    def find_item(self, item_name):
        for item in self.items.keys():
            if item_name == item.get_name():
                return item
        return None

    def get_item_amount(self, item_name):
        item = self.find_item(item_name)
        if item is None:
            return 0
        return self.items[item]

    def calculate_subtotal(self):
        self.cart_total = 0
        for item in self.items.keys():
            self.cart_total += (item.get_price() * self.items[item])

    def calculate_item_amount(self):
        self.item_count = 0
        for item in self.items:
            self.item_count += self.items[item]

    def update(self):
        self.calculate_subtotal()
        self.calculate_item_amount()

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_index(self):
        return self.index

    def get_total(self):
        return self.cart_total

    def is_empty(self) -> bool:
        if self.items == {}:
            return True
        return False

    def generate_receipt(self) -> str:
        col_width = 20
        total_width = (col_width * 4) + 9
        self.calculate_subtotal()

        result = ""
        result += f"{(" " + self.get_name() + " ").center(total_width, "-")}" + "\n"
        result += f"{(" CART ID: " + f"{self.get_index():,}".rjust(10, "0") + " ").center(total_width, "-")}" + "\n"
        result += f"{"ITEM".ljust(col_width)} | {"PRICE".ljust(col_width)} | {"QTY".ljust(col_width)} | {"TOTAL".ljust(col_width)}" + "\n"
        for key in self.items.keys():
            result += (
                f"{key.get_name().upper().ljust(col_width)} | {str(f"{key.get_price():,}").ljust(col_width)} | {str(self.items[key]).ljust(col_width)} | {str(f"{key.get_price() * self.items[key]:,}").ljust(col_width)}") + "\n"
        result += ("-" * total_width) + "\n"
        result += f"{("SUBTOTAL: " + str(f"{self.get_total():,}")).ljust(total_width)}" + "\n"
        result += f"{"THANK YOU FOR SHOPPING! ^_^".ljust(total_width)}" + "\n"
        result += (" SUPERMARKET AL-FARES ".center(total_width, "-")) + "\n"
        return result

    def view_receipt(self):
        if tuple(self.items.keys()) == ():
            print("Cart is empty")
            return
        print(self.generate_receipt())

    def write_receipt_to_file(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.generate_receipt())

class Settings:
    def __init__(self, file_path: str):
        self.receipt_counter = 0
        self.file_path = file_path
        self.load()

    def get_receipt_number(self):
        return self.receipt_counter

    def increment_receipt_number(self):
        self.receipt_counter += 1
        self.save()

    def save(self):
        while True:
            try:
                print("Attempting to open and write to file...")
                with open(self.file_path, "w") as file:
                    file.write(str(self.receipt_counter))
                print("Success!")
                break
            except FileNotFoundError:
                print("No settings file found, creating a new one...")
                with open(self.file_path, "x"):
                    pass
            except Exception as e:
                print("Couldn't save settings.")
                print("Details: " + str(e))

    def load(self):
        try:
            with open(self.file_path, "r") as file:
                raw = file.read()

                if not raw or raw == "":
                    raise ValueError("Settings file is empty.")

                self.receipt_counter = int(raw)
        except FileNotFoundError:
            print("No settings file found, creating an empty one...")
            with open(self.file_path, "x"):
                pass
            return {"error": "Couldn't find or load settings file."}
        except ValueError:
            print("Settings file is empty.")
            return {"error": "Settings file is empty."}

    @staticmethod
    def load_products(file_path: str) -> list[dict] | None:
        try:
            with open(file_path, 'r') as file:
                products_catalog = json.load(file)
            print("Product catalog successfully imported")
            return products_catalog
        except FileNotFoundError:
            print("Error: The file 'data.json' was not found. Please check the file path.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file. The file content might be malformed.")


    @staticmethod
    def clear_console():
        os.system('cls')