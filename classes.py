"""
classes.py
This file will hold all classes used for products, carts, etc.
"""
import json
import os
from cmath import inf

# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)


class Item:
    def __init__(self, identifier: int, product_name: str, price: float, amount: int = 0):
        self.identifier = identifier
        self.product_name = product_name
        self.price = price
        self.amount = amount

    def get_name(self) -> str:
        return self.product_name

    def get_amount(self) -> int:
        return self.amount

    def get_price(self) -> float:
        return self.price

    def identify(self) -> int:
        return self.identifier

    def add(self, amount: int):
        if amount < 0:
            raise ValueError("Can't add negative products")
        self.amount += amount

    def remove(self, amount: int):
        if amount < 0:
            raise ValueError("Can't add negative products")

        if amount > self.amount:
            amount = self.amount

        self.amount -= amount


class Cart:
    def __init__(self, cart_index, cart_name):
        self.index = cart_index
        self.name = cart_name
        self.items = []  # [ Item() ]
        self.item_count = 0
        self.cart_total = 0

    def insert_item(self, item: Item, count: int):
        if count <= 0:
            return

        found_item = self.find_item(item.identify())
        if found_item is None:
            item.amount = count
            self.items.append(item)
        else:
            found_item.add(count)

        self.update()

    def __update_item_count__(self, item_id, offset):
        for item in self.items:
            if item.identify() == item_id:
                item.add(offset)
                self.update()

    def remove_item(self, item: Item, count: int = inf):
        try:
            item: Item | None = self.find_item(item.identify())
            if item is None:
                raise KeyError("Item not found in cart")
            if count >= item.get_amount():
                self.items.remove(item)
                return
            item.remove(count)
        except KeyError as e:
            print(e)

    def get_items(self):
        return self.items

    def find_item(self, item_identifier: int):
        for s_item in self.items:
            if s_item.identify() == item_identifier:
                return s_item
        return None

    def get_item_amount(self, item_identifier):
        item = self.find_item(item_identifier)
        if item is None:
            return 0
        return item.get_amount()

    def calculate_subtotal(self):
        self.cart_total = 0
        for item in self.items:
            self.cart_total += (item.get_amount() * item.get_price())
        self.cart_total = round(self.cart_total, 2)

    def calculate_item_amount(self):
        self.item_count = 0
        for item in self.items:
            self.item_count += item.get_amount()

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
        if not self.items:
            return True
        return False

    def generate_receipt(self) -> str:
        columns = {"ID": 5, "ITEM": 50, "PRICE": 5, "QTY": 5, "TOTAL": 10}
        total_width = 3 * (len(columns) - 1)
        for width in columns.items():
            total_width += width[1]

        self.calculate_subtotal()

        result = ""
        result += f"{("[ CART ID: " + f"{self.get_index():,}" + " | " + " CART NAME: " + self.get_name() + "] ").center(total_width, "-")}" + "\n"
        result += ("=" * total_width) + "\n"

        for idx, column in enumerate(columns.keys()):
            result += f"{column.ljust(columns[column])}" + (" | " if idx < len(columns) - 1 else "\n")

        for item in self.items:
            result += (
                          f"{str(item.identify()).rjust(columns["ID"], '0')}"
                          f" | {item.get_name().upper().ljust(columns["ITEM"])}"
                          f" | {str(f"{item.get_price():,}").ljust(columns["PRICE"])}"
                          f" | {str(item.get_amount()).ljust(columns["QTY"])}"
                          f" | {str(f"{round(item.get_price() * item.get_amount(), 2):,}").ljust(columns["TOTAL"])}") + "\n"

        result += ("=" * total_width) + "\n"
        result += f"{("TOTAL: " + str(f"{round(self.get_total(), 2):,}")).ljust(total_width)}" + "\n"
        result += f"{"THANK YOU FOR SHOPPING! ^_^".ljust(total_width)}" + "\n"
        result += (" SUPERMARKET EL MEHABEDATEYA ".center(total_width, "=")) + "\n"
        return result

    def view_receipt(self):
        if not self.items:
            print("Cart is empty")
            return
        print(self.generate_receipt())

    def write_receipt_to_file(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.generate_receipt())


class Settings:
    def __init__(self, file_path: str, carts: list):
        self.receipt_counter = 0
        self.file_path = file_path
        self.carts = carts
        self.load()

    def get_receipt_number(self):
        return self.receipt_counter

    def increment_receipt_number(self):
        self.receipt_counter += 1

    def save(self, carts):
        while True:
            try:
                with open(self.file_path, "w") as file:
                    carts_list = []
                    for cart in carts:
                        items_list = []
                        for item in cart.get_items():
                            items_list.append({"identifier": item.identify(), "name": item.get_name(), "price": item.get_price(), "amount": item.get_amount()})
                        cart_json = {"index": cart.get_index(), "name": cart.get_name(), "total": cart.get_total(), "items": [item for item in items_list], "count": cart.item_count}
                        carts_list.append(cart_json)
                    json.dump({"receipt_count": self.receipt_counter, "carts": carts_list}, file)
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
                raw = json.load(file)

                if not raw or raw == "":
                    raise ValueError("Settings file is empty.")

                self.receipt_counter = raw["receipt_count"]
                self.carts = []
                for cart in raw["carts"]:
                    load_cart = Cart(cart["index"], cart["name"])
                    for item in cart["items"]:
                        load_item = Item(item["identifier"], item["name"], item["price"], item["amount"])
                        load_cart.insert_item(load_item, item["amount"])
                    self.carts.append(load_cart)

        except FileNotFoundError:
            print("No settings file found, creating an empty one...")
            with open(self.file_path, "x"):
                pass
            return {"error": "Couldn't find or load settings file."}
        except ValueError:
            print("Settings file is empty.")
            return {"error": "Settings file is empty."}

    @staticmethod
    def load_products(file_path: str) -> list[Item] | None:
        try:
            with open(file_path, 'r') as file:
                products_catalog = json.load(file)
            item_list = []
            for product in products_catalog:
                item_list.append(Item(product["identifier"], product["name"], product["price"]))
            return item_list

        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found. Please check the file path.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file. The file content might be malformed.")

    @staticmethod
    def save_products(file_path: str, products: list):
        try:
            items_list = []
            with open(file_path, 'w') as file:
                for item in products:
                    items_list.append({"identifier": item.identify(), "name": item.get_name(), "price": item.get_price(), "amount": item.get_amount()})

                json.dump(items_list, file)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found. Please check the file path.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file. The file content might be malformed.")

    @staticmethod
    def clear_console():
        os.system('cls')
