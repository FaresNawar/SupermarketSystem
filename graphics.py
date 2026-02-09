"""
graphics.py
This file is responsible for handling the GUI components of the project.
Windows, buttons, labels, frames, etc.
"""
import os

# Ensure file is only imported and not ran
if __name__ == '__main__':
    print("This is a library file. Please run 'main.py' instead.")
    exit(0)

from typing import Any, Literal
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes import Cart, Settings, Item


class Frame(tk.Frame):
    """
    Wrapper for the ttk.Frame class
    """

    def __init__(self, master: tk.Tk | tk.Toplevel | ttk.Frame | tk.Frame | Any, padding: int, background: str = None):
        super().__init__(master=master, padx=padding, pady=padding, bg=background)

        if background is None:
            try:
                self.configure(bg=self.master["bg"])
            except tk.EXCEPTION:
                print("Couldn't make label transparent")

class Label(tk.Label):
    def __init__(self, parent, text: str = "", font: str = "Arial", font_size: int = 5, width: int = 15, padding: int = 0,
                 foreground: str = "#FFFFFF", background: str = None, anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "center", text_var: tk.Variable = None):
        super().__init__(parent, text=text, font=(font, font_size), padx=padding, pady=padding, foreground=foreground,
                         background=background, width=width, anchor=anchor, textvariable=text_var)

        self.parent = parent
        self.text = text
        self.font = font
        self.font_size = font_size,
        self.padding = padding
        self.foreground = foreground
        self.background = background

        if background is None:
            try:
                self.configure(bg=parent["bg"])
            except tk.EXCEPTION:
                print("Couldn't make label transparent")

    def set_text(self, text):
        self.text = text
        self.configure(text=text)
        self.update()


class Separator(Frame):
    def __init__(self, master: tk.Tk | tk.Toplevel | ttk.Frame | tk.Frame | Any, width, foreground: str = None, thickness: float = 1):
        super().__init__(master=master, padding=0)
        self.configure(width=width, height=thickness, highlightcolor=foreground, background=foreground)


class Window:
    """
    Wrapper for tk.Tk() and tk.Toplevel()
    """

    def __init__(self, width: int, height: int, master: tk.Tk | None = None, title: str = None, pos: tuple[int, int] = None, resizable: bool = False,
                 toplevel: bool = False):
        w = tk.Toplevel(master) if toplevel else tk.Tk()

        if toplevel:
            w.bind('<Escape>', lambda x: self.obj.destroy())
            w.config(bg=master["bg"])
            w.grab_set()

        self.obj = w
        self.toplevel = toplevel
        self.width = width
        self.height = height
        self.title = title or "Untitled"

        if not pos:
            pos = ((w.winfo_screenwidth() // 2) - (width // 2), (w.winfo_screenheight() // 2) - (height // 2) - 25)

        self.obj.geometry("%dx%d+%d+%d" % (width, height, pos[0], pos[1]))
        self.obj.title(self.title)

        self.pos = pos
        self.obj.resizable(width=resizable, height=resizable)

    def set_parent(self, master):
        if self.toplevel:
            self.obj.master = master
        else:
            raise Exception("This window is not a toplevel")

    def update_geometry(self, width: int = None, height: int = None, center: bool = True):
        pos = ((self.obj.winfo_screenwidth() // 2) - ((width if width else self.width) // 2), (self.obj.winfo_screenheight() // 2) - ((height if height else self.height) // 2) - 25)
        self.obj.geometry(f"{width if width else self.width}x{height if height else self.height}" + (f"+{pos[0]}+{pos[1]}" if center else ""))

class SupermarketApplication(Window):
    """
    Where all hell breaks loose
    """
    def __init__(self):
        self.__setup_parameters__()
        self.__setup_design_attributes__()

        super().__init__(width=self.width, height=self.height, title="My Supermarket System", resizable=False)

        self.__build__()
        self.obj.mainloop()

    def __setup_design_attributes__(self):
        # Window / frame
        self.window_background_color = "#52408f"
        self.frame_background_color = "white"

        # Text
        self.text_color = "white"
        self.font = "Alexandria"
        self.display_font = "Aqila - Demo Version"
        self.font_large = 30
        self.font_medium = 20
        self.font_small = 15
        self.font_tiny = 10

        # Buttons
        self.button_text_color = "black"
        self.button_background_color = "#B6ABDB"
        self.button_highlight_color = "#736B8E"
        self.button_width_small = 15
        self.button_width_tiny = 15
        self.button_width_large = 30

        self.confirm_color = "#599e5e"
        self.cancel_color = "#c94f4f"

        # Combobox
        self.combo_background_color = "#52408f"
        self.combo_text_color = "white"
        self.combo_font_size = self.font_small
        self.combo_font = self.font
        self.combo_width = 30

        # Separator
        self.separator_thickness = 1.5
        self.separator_width = 500
        self.separator_color = "white"

    def __setup_parameters__(self):
        self.selected_cart: Cart | None = None
        self.carts = {}
        self.settings = Settings(file_path="program_settings.txt", carts=[])
        self.product_catalog = self.settings.load_products("data.json")
        self.__refresh_products__()
        self.width, self.height = 720, 550

        # Attempt to load settings
        self.settings.load()
        for cart in self.settings.carts:
            self.carts.update({cart.get_index(): cart})

    def __build__(self):
        self.obj.config(bg=self.window_background_color)
        self.cframe = Frame(self.obj, 20)
        self.cframe.place(relx=0.5, rely=0.5, anchor='center')

        Separator(self.cframe, self.separator_width, self.separator_color, self.separator_thickness).pack()
        Label(self.cframe, "MY SUPERMARKET", font=self.display_font, font_size=self.font_large, foreground="white", width=35).pack()
        Separator(self.cframe, self.separator_width, self.separator_color, self.separator_thickness).pack()

        selected_frame = Frame(self.cframe, 0)
        selected_frame.pack()

        Label(selected_frame, "Selected:", font=self.font, font_size=self.font_medium, foreground=self.text_color, width=9).grid(row=0, column=0)

        self.cart_selector = ttk.Combobox(selected_frame, font=(self.combo_font, self.combo_font_size), background=self.combo_background_color, foreground=self.combo_background_color, state="readonly")
        self.cart_selector.grid(row=0, column=1)
        self.__update_cart_list__()
        self.cart_selector.bind("<<ComboboxSelected>>", lambda x: self.__set_selected_cart__(None))

        buttons = [
            {"id": "CART_NEW", "button_text": "New Cart", "width": 15, "row": 0, "column": 0, "column_span": 1},
            {"id": "CART_OVERVIEW", "button_text": "Cart Overview", "width": 15, "row": 0, "column": 1, "column_span": 1},
            {"id": "PRODUCT_VIEW", "button_text": "View Product", "width": 15, "row": 1, "column": 0, "column_span": 1},
            {"id": "CART_MODIFY", "button_text": "Edit Cart", "width": 15, "row": 1, "column": 1, "column_span": 1},
            {"id": "CART_RECEIPT", "button_text": "View Receipt", "width": 15, "row": 2, "column": 0, "column_span": 1},
            {"id": "CART_TO_FILE", "button_text": "Print Receipt", "width": 15, "row": 2, "column": 1, "column_span": 1},
            {"id": -1, "color": "#1a1a25", "width": 300, "row": 3, "column_span": 2},
            {"id": "PRODUCT_NEW", "button_text": "New Product", "row": 4, "width": 15, "column": 0, "column_span": 1},
            {"id": "PRODUCT_MODIFY", "button_text": "Edit Product", "row": 4, "width": 15, "column": 1, "column_span": 1},
            {"id": -1, "color": "#1a1a25", "width": 300, "row": 5, "column_span": 2},
            {"id": "EXIT", "button_text": "Exit", "row": 6, "width": 32, "column": 0, "column_span": 2},
        ]

        button_frame = Frame(self.cframe, padding=5, background=self.frame_background_color)
        button_frame.configure(border=2, relief="solid", padx=7)
        button_frame.pack()
        Separator(self.cframe, self.separator_width, self.separator_color, self.separator_thickness).pack(pady=10)

        for button in buttons:
            if button["id"] == -1:
                b = Separator(button_frame, button["width"], button["color"], self.separator_thickness)
                b.grid(row=button["row"] + 1, columnspan=button["column_span"], padx=5, pady=5)
                continue
            b = Button(button_frame, text=button["button_text"], padding=0, width=button["width"], foreground=self.button_text_color, background=self.button_background_color, highlight=self.button_highlight_color, font=self.font, font_size=self.font_small)
            b.bind_function(lambda x=button["id"]: self.__handler__(x))
            b.grid(row=button["row"] + 1, column=button["column"], columnspan=button["column_span"], padx=5, pady=5)

        self.__focus__()

    def __update_cart_list__(self):
        for cart in self.carts.values():
            cart.update()
        self.cart_selector.configure(values=[cart.get_index() for cart in self.carts.values()])

    def __set_selected_cart__(self, cart: Cart | None):
        if cart is None:
            cart = self.carts[int(self.cart_selector.get())]
        if cart not in self.carts.values():
            print("Cart not found.")
            print(cart)
            return
        self.selected_cart = cart

    def __handler__(self, option):
        self.cframe.place_forget()
        self.cframe.place(relx=0.5, rely=0.5, anchor="center")
        match option:
            case "CART_NEW":  # New Cart
                new_cart_id = self.settings.get_receipt_number()
                new_cart: Cart = Cart(new_cart_id, "")

                self.carts.update({new_cart_id: new_cart})
                self.settings.increment_receipt_number()
                self.__set_selected_cart__(new_cart)

                Mb.showinfo(title="Success", text=f"Successfully added cart [{new_cart.get_index()}] {new_cart.get_name()}", parent=self.obj)

            case "CART_OVERVIEW":  # Check Cart
                self.cframe.place_forget()
                self.update_geometry(width=500, height=350, center=False)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                Label(f, "Check Cart", self.font, 20, 10).pack()
                Separator(f, 400, self.separator_color, self.separator_thickness).pack(pady=5)

                cart_selector = ttk.Combobox(f, foreground=self.button_text_color, background=self.button_background_color, font=(self.font, self.font_small), values=[cart.get_index() for cart in self.carts.values()], state="readonly")
                cart_selector.pack()

                header_row = ["ID", "Products", "Total"]
                widths = [5, 10, 10]

                holder = Frame(f, 10)
                holder.focus_force()
                holder.pack()

                Separator(f, 400, self.separator_color, self.separator_thickness).pack(pady=5)

                back_button = Button(f, "Back", 10, 0, self.button_text_color, self.button_background_color, self.button_highlight_color, self.font, self.font_small)
                back_button.bind_function(__exit__)
                back_button.pack()

                for idx, header in enumerate(header_row):
                    Label(holder, text=header, font=self.font, font_size=self.font_small, width=widths[idx], anchor="w").grid(row=0, column=idx, padx=5)

                def __update__():
                    if cart_selector.get() == "":
                        return

                    cart = self.carts[int(cart_selector.get())]
                    Label(holder, text=header, font=self.font, font_size=self.font_small, width=widths[idx], anchor="w").grid(row=0, column=idx, padx=5)
                    Label(holder, text=cart.get_index(), font=self.font, font_size=self.font_small, width=widths[0], anchor="w").grid(row=idx + 1, column=0, padx=5)
                    Label(holder, text=cart.item_count, font=self.font, font_size=self.font_small, width=widths[1], anchor="w").grid(row=idx + 1, column=1, padx=5)
                    Label(holder, text=cart.get_total(), font=self.font, font_size=self.font_small, width=widths[2], anchor="w").grid(row=idx + 1, column=2, padx=5)

                cart_selector.set(self.selected_cart.get_index()) if self.check_selected_cart(False) else ...
                __update__()
                cart_selector.bind("<<ComboboxSelected>>", lambda x: __update__())

            case "PRODUCT_VIEW": # View Product
                self.cframe.place_forget()
                self.update_geometry(750, 300, center=False)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                top = Frame(f, 10)
                top.pack()

                Label(top, "View Product", self.font, 20, 20, anchor="w").grid(row=0, column=0)
                Separator(f, 700, self.separator_color, self.separator_thickness).pack()

                product_selector = ttk.Combobox(top, foreground=self.button_text_color, background=self.button_background_color, font=(self.font, self.font_small), values=[product.get_name() for product in self.product_catalog], state="readonly")
                product_selector.grid(row=0, column=1)

                header_row = ["ID", "Product Name", "Price"]
                widths = [5, 30, 10]

                holder = Frame(f, 10)
                holder.focus_force()
                holder.pack()

                Separator(f, 700, self.separator_color, self.separator_thickness).pack(pady=10)
                back_button = Button(f, "Back", 10, 0, self.button_text_color, self.button_background_color, self.button_highlight_color, self.font, self.font_small)
                back_button.bind_function(__exit__)
                back_button.pack()

                for idx, header in enumerate(header_row):
                    Label(holder, text=header, font=self.font, font_size=self.font_small, width=widths[idx], anchor="w").grid(row=0, column=idx, padx=5)

                def __update__():
                    if product_selector.get() == "":
                        return

                    product_name = product_selector.get()
                    product = None
                    for s_product in self.product_catalog:
                        if s_product.get_name() == product_name:
                            product = s_product

                    Label(holder, text=str(product.identify()), font=self.font, font_size=self.font_small, width=widths[0], anchor="w").grid(row=1, column=0, padx=5)
                    Label(holder, text=product_name, font=self.font, font_size=self.font_small, width=widths[1], anchor="w").grid(row=1, column=1, padx=5)
                    Label(holder, text=str(product.get_price()), font=self.font, font_size=self.font_small, width=widths[2], anchor="w").grid(row=1, column=2, padx=5)

                product_selector.bind("<<ComboboxSelected>>", lambda x: __update__())
                product_selector.set(self.product_catalog[0].get_name())
                __update__()

            case "CART_MODIFY":  # Edit Cart
                if not self.check_selected_cart():
                    return

                def __find_product__(name: str):
                    for s_product in self.product_catalog:
                        if s_product.get_name() == name:
                            return s_product
                    return None

                def __update_price__():
                    product = __find_product__(product_selector.get())
                    if product is None:
                        return True
                    price.set_text(product.get_price())
                    if amount_field.get() == "":
                        return True
                    total.set_text(round(product.get_price() * int(amount_field.get()), 2))
                    return True

                def __numbers_only__(val):
                    try:
                        int(val)
                        return True
                    except ValueError:
                        return False

                self.cframe.place_forget()
                self.update_geometry(750, 400, center=False)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                header = Frame(f, 00)
                Label(header, "Edit Cart", self.font, 20, 20, anchor="w").grid(row=0, column=0)
                Label(header, str(self.selected_cart.get_index()), self.font, self.font_medium, 10, anchor="e").grid(row=0, column=1)
                header.pack()

                Separator(f, 600, self.separator_color, self.separator_thickness).pack()

                fields_frame = Frame(f, 0)
                fields_frame.pack()

                Label(fields_frame, font=self.font, font_size=self.font_small, text="Product", foreground=self.text_color).grid(row=1, column=0, padx=5, pady=10)

                product_selector = ttk.Combobox(master=fields_frame, font=(self.combo_font, self.combo_font_size), values=[product.get_name() for product in self.product_catalog], width=24)
                product_selector.grid(row=1, column=1, padx=5, pady=10)
                product_selector.focus()

                price_label = Label(fields_frame, font=self.font, font_size=self.font_small, text="Price", foreground=self.text_color)
                price_label.grid(row=2, column=0)

                price = Label(fields_frame, font=self.font, font_size=self.font_small, foreground=self.text_color, width=20)
                price.grid(row=2, column=1)

                amount_label = Label(fields_frame, font=self.font, font_size=self.font_small, text="Amount", foreground=self.text_color)
                amount_label.grid(row=3, column=0, padx=5, pady=10)
                amount_label.focus()

                amount = tk.IntVar()
                amount.set(1)
                amount.trace_add(mode="write", callback=lambda x, y, z: __update_price__())
                amount_field = ttk.Entry(master=fields_frame, font=(self.font, self.font_small), width=25, validatecommand=(self.obj.register(__numbers_only__), '%S'), validate="key", textvariable=amount)
                amount_field.grid(row=3, column=1, padx=5, pady=10)
                amount_field.focus()

                total_label = Label(fields_frame, font=self.font, font_size=self.font_small, text="Total", foreground=self.text_color)
                total_label.grid(row=4, column=0)

                total = Label(fields_frame, font=self.font, font_size=self.font_small, foreground=self.text_color, width=20)
                total.grid(row=4, column=1)

                Separator(f, 600, self.separator_color, self.separator_thickness).pack(pady=5)

                button_frame = Frame(f, padding=10)
                button_frame.pack()

                add_button = Button(button_frame, text="Add", width=15, background=self.button_background_color, foreground=self.button_text_color, highlight=self.confirm_color, font=self.font, font_size=self.font_small)
                add_button.grid(row=0, column=0, padx=5)

                remove_button = Button(button_frame, text="Remove", width=15, background=self.button_background_color, foreground=self.button_text_color, highlight=self.cancel_color, font=self.font, font_size=self.font_small)
                remove_button.grid(row=0, column=1, padx=5)

                back_button=Button(button_frame, text="Back", width=15, background=self.button_background_color, foreground=self.button_text_color, highlight=self.button_highlight_color, font=self.font, font_size=self.font_small)
                back_button.grid(row=0, column=2, padx=5)
                back_button.bind_function(__exit__)

                def _(remove = False):
                    if not product_selector.get() or not amount_field.get():
                        Mb.showerror("Missing Field", "Did you forget to fill out a field?", self.obj)
                        return

                    product = __find_product__(product_selector.get())
                    if int(amount_field.get()) <= 0 or product is None:
                        Mb.showerror("Invalid Value", "One of the parameters entered is invalid!\nPlease check and try again", self.obj)
                        return

                    product_selector.set("")
                    amount.set(1)
                    price.set_text("")
                    total.set_text("")

                    if not remove:
                        self.selected_cart.insert_item(product, int(amount_field.get()))
                        Mb.showinfo("Success", f"Added {amount_field.get()}x {product.get_name()} to cart!", self.obj)

                        return

                    self.selected_cart.remove_item(product, int(amount_field.get()))
                    Mb.showinfo("Success", f"Removed {amount_field.get()}x {product.get_name()} from cart!", self.obj)
                    return

                product_selector.bind("<<ComboboxSelected>>", lambda x: __update_price__())
                add_button.bind_function(lambda x = False: _(x))
                remove_button.bind_function(lambda x = True: _(x))
                self.obj.mainloop()

            case "CART_RECEIPT":  # View Receipt
                if not self.selected_cart_empty():
                    return

                self.cframe.place_forget()
                self.update_geometry(width=900, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                labels = []
                current_page = tk.IntVar()
                current_page.set(0)
                pages = []

                c_page = list()
                for idx, x_item in enumerate(self.selected_cart.get_items(), 1):
                    c_page.append(x_item)
                    if idx % 5 == 0 or idx > len(self.selected_cart.get_items()) - 1:
                        pages.append(c_page.copy())
                        c_page.clear()
                del c_page

                def __list_products__():
                    if len(labels) != 0:
                        for label in labels:
                            for inner_label in label:
                                inner_label.grid_forget()
                    labels.clear()

                    for row, item in enumerate(pages[current_page.get()]):
                        labels.append([Label(holder, text=str(item.identify()), font=self.font, font_size=self.font_small, width=widths[0], anchor="w"),
                                       Label(holder, text=item.get_name(), font=self.font, font_size=self.font_small, width=widths[1], anchor="w"),
                                       Label(holder, text=str(item.get_amount()), font=self.font, font_size=self.font_small, width=widths[2], anchor="w"),
                                       Label(holder, text=str(item.get_price()), font=self.font, font_size=self.font_small, width=widths[3], anchor="w"),
                                       Label(holder, text=str(round(item.get_price() * item.get_amount(), 2)), font=self.font, font_size=self.font_small, width=widths[4], anchor="w")])

                    for row, label in enumerate(labels):
                        for column, inner_label in enumerate(label):
                            inner_label.grid(row=row + 1, column=column, padx=5)

                def __paginate__(offset: Literal[1, -1, 0]):
                    if (current_page.get() + offset) >= len(pages):
                        Mb.showerror("Final Page", "No more items to show", self.obj)
                        return
                    if (current_page.get() + offset) < 0:
                        Mb.showerror("Final Page", "No more items to show", self.obj)
                        return

                    current_page.set(current_page.get() + offset)
                    cart_label.set_text(f"Viewing Cart {self.selected_cart.get_index()} | Page {current_page.get() + 1}")
                    __list_products__()

                cart_label = Label(f, f"Viewing Cart {self.selected_cart.get_index()} | Page {current_page.get() + 1}", self.font, 20, 30)
                cart_label.pack()
                Separator(f, 800, self.separator_color, self.separator_thickness).pack()
                header_row = ["ID", "Product", "Qty", "Price", "Total"]
                widths = [5, 25, 5, 10, 10]

                holder = Frame(f, 10)
                holder.focus_force()

                for idx, header in enumerate(header_row):
                    Label(holder, text=header, font=self.font, font_size=self.font_small, width=widths[idx], anchor="w").grid(row=0, column=idx, padx=5)
                __paginate__(0)

                holder.pack()
                Label(f, text=f"Subtotal: {self.selected_cart.get_total()}", font_size=self.font_small, font=self.font, width=30, anchor="center").pack()

                Separator(f, 800, self.separator_color, self.separator_thickness).pack(pady=5)
                button_frame = Frame(f, 0)
                button_frame.pack()

                prev_button = Button(button_frame, text="Prev", width=5, background=self.button_background_color, foreground=self.button_text_color, highlight=self.button_highlight_color, font=self.font, font_size=self.font_small)
                prev_button.grid(row=3, column=0, padx=5)
                prev_button.bind_function(lambda: __paginate__(-1))

                back_button = Button(button_frame, text="Back", width=15, background=self.button_background_color, foreground=self.button_text_color, highlight=self.button_highlight_color, font=self.font, font_size=self.font_small)
                back_button.grid(row=3, column=1, padx=5)
                back_button.bind_function(__exit__)

                next_button = Button(button_frame, text="Next", width=5, background=self.button_background_color, foreground=self.button_text_color, highlight=self.button_highlight_color, font=self.font, font_size=self.font_small)
                next_button.grid(row=3, column=2, padx=5)
                next_button.bind_function(lambda: __paginate__(1))

            case "CART_TO_FILE":  # Print Receipt
                if not self.selected_cart_empty():
                    return

                self.selected_cart.write_receipt_to_file("receipt.txt")
                Mb.showinfo("Success", "Receipt printed to 'receipt.txt'!", self.obj)
                os.startfile("receipt.txt")

            case "PRODUCT_NEW": # New product
                self.cframe.place_forget()
                self.update_geometry(750, 350, center=False)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                top = Frame(f, 10)
                top.pack()

                Label(top, "New Product", self.font, 20, 20, anchor="center").grid(row=0, column=0)
                Separator(f, 700, self.separator_color, self.separator_thickness).pack()

                holder = Frame(f, 0)
                holder.pack()

                Label(holder, "Product ID", self.font, self.font_small, 20).grid(row=0, column=0, pady=5)
                Label(holder, "Product Name", self.font, self.font_small, 20).grid(row=1, column=0)
                Label(holder, "Price", self.font, self.font_small, 20).grid(row=2, column=0)

                identifier = tk.IntVar()
                identifier.set(self.product_catalog[-1].identify() + 1)
                name = tk.StringVar()
                price = tk.DoubleVar()

                Separator(f, 700, self.separator_color, self.separator_thickness).pack(pady=10)

                Label(holder, str(identifier.get()), self.font, self.font_small, 20).grid(row=0, column=1)
                name_field = ttk.Entry(holder, font=(self.font, self.font_small), width=20, textvariable=name)
                name_field.grid(row=1, column=1, pady=5)

                price_field = ttk.Entry(holder, font=(self.font, self.font_small), width=20, textvariable=price)
                price_field.grid(row=2, column=1, pady=5)

                def _():
                    if price.get() < 0 or name.get() == "":
                        Mb.showerror("Forgetting Something?", "One or more fields is empty", self.obj)
                        return

                    new_product = Item(identifier.get(), name.get(), price.get())
                    self.product_catalog.append(new_product)
                    Mb.showinfo("Success", "New product added successfully!", self.obj)
                    __exit__()

                button_frame = Frame(f, 0)
                button_frame.pack()

                confirm_button = Button(button_frame, "Add Product", 15, 0, self.button_text_color, self.button_background_color, self.confirm_color, self.font, self.font_small)
                confirm_button.bind_function(_)
                confirm_button.grid(row=0, column=0, padx=5)

                back_button = Button(button_frame, "Back", 10, 0, self.button_text_color, self.button_background_color, self.button_highlight_color, self.font, self.font_small)
                back_button.bind_function(__exit__)
                back_button.grid(row=0, column=1, padx=5)


            case "PRODUCT_MODIFY": # Edit product
                self.cframe.place_forget()
                self.update_geometry(750, 350, center=False)

                def __exit__():
                    f.place_forget()
                    self.cframe.place(relx=0.5, rely=0.5, anchor="center")
                    self.update_geometry(width=self.width, height=self.height, center=False)

                f = Frame(self.obj, 10)
                f.place(relx=0.5, rely=0.5, anchor="center")
                f.configure(highlightcolor="white", highlightthickness=3)

                top = Frame(f, 10)
                top.pack()

                Label(top, "Edit Product", self.font, 20, 20, anchor="w").grid(row=0, column=0)
                Separator(f, 700, self.separator_color, self.separator_thickness).pack()

                product_selector = ttk.Combobox(top, foreground=self.button_text_color, background=self.button_background_color, font=(self.font, self.font_small), values=[product.get_name() for product in self.product_catalog], state="readonly")
                product_selector.grid(row=0, column=1)

                header_row = ["ID", "Product Name", "Price"]

                holder = Frame(f, 10)
                holder.focus_force()
                holder.pack()

                button_frame = Frame(f, 0)
                button_frame.pack()

                Separator(f, 700, self.separator_color, self.separator_thickness).pack(pady=10)
                back_button = Button(button_frame, "Back", 10, 0, self.button_text_color, self.button_background_color, self.button_highlight_color, self.font, self.font_small)
                back_button.bind_function(__exit__)
                back_button.grid(row=0, column=2, padx=5)

                def _(remove: bool = False):
                    for product in self.product_catalog:
                        if product.identify() == product_id.get():
                            if remove:
                                self.product_catalog.remove(product)
                                for cart in self.carts.values():
                                    cart.remove_item(product)
                                Mb.showinfo("Success!", "Product removed successfully", self.obj)
                                return

                            product.product_name = name.get()
                            product.price = price.get()
                            Mb.showinfo("Success!", "Product edited successfully!", self.obj)
                            return

                    Mb.showerror("uh oh..", "product wasnt found.", self.obj)
                    return

                confirm_button = Button(button_frame, "Modify", 10, 0, self.button_text_color, self.button_background_color, self.confirm_color, self.font, self.font_small)
                confirm_button.bind_function(lambda: _(False))
                confirm_button.grid(row=0, column=0, padx=5)

                remove_button = Button(button_frame, "Remove", 10, 0, self.button_text_color, self.button_background_color, self.cancel_color, self.font, self.font_small)
                remove_button.bind_function(lambda: _(True))
                remove_button.grid(row=0, column=1, padx=5)

                product_id = tk.IntVar()
                name = tk.StringVar()
                price = tk.DoubleVar()

                for idx, header in enumerate(header_row):
                    Label(holder, text=header, font=self.font, font_size=self.font_small, width=20, anchor="w").grid(row=idx, column=0)

                def __update__():
                    if product_selector.get() == "":
                        return

                    product_name = product_selector.get()
                    product = None
                    for s_product in self.product_catalog:
                        if s_product.get_name() == product_name:
                            product = s_product

                    product_id.set(product.identify())
                    name.set(product.get_name())
                    price.set(product.get_price())

                    Label(holder, text=str(product.identify()), font=self.font, font_size=self.font_small, width=20, anchor="w").grid(row=0, column=1, padx=5)
                    name_field = ttk.Entry(holder, font=(self.font, self.font_small), width=20, textvariable=name)
                    name_field.grid(row=1, column=1, padx=5)

                    price_field = ttk.Entry(holder, font=(self.font, self.font_small), width=20, textvariable=price)
                    price_field.grid(row=2, column=1, padx=5)

                product_selector.bind("<<ComboboxSelected>>", lambda x: __update__())
                product_selector.set(self.product_catalog[0].get_name())
                __update__()

            case _:  # Exit
                self.settings.save([cart for cart in self.carts.values()])
                self.obj.destroy()
                return

        self.settings.save([cart for cart in self.carts.values()])
        self.__refresh_products__()
        self.settings.save_products("data.json", [product for product in self.product_catalog])
        self.__update_cart_list__()

    def __refresh_products__(self):
        for idx, product in enumerate(self.product_catalog, 1):
            product.identifier = idx

    def __focus__(self):
        self.obj.grab_set()
        self.obj.grab_release()
        self.obj.wm_attributes('-topmost', True)
        self.obj.update_idletasks()
        self.obj.wm_attributes('-topmost', False)
        self.obj.lift()
        self.cframe.focus_force()

    def check_selected_cart(self, warn: bool = True) -> bool:
        if self.selected_cart is None:
            Mb.showerror("Error", "You must select a cart!", self.obj) if warn else ...
            return False
        return True

    def selected_cart_empty(self, warn: bool = True) -> bool:
        if not self.check_selected_cart(warn):
            return False
        if self.selected_cart.is_empty():
            Mb.showerror("Error", "Cart is empty!", self.obj) if warn else ...
            return False
        return True


class Mb:
    @staticmethod
    def showinfo(title: str, text: str, parent, detail: str = None):
        return messagebox.showinfo(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def showerror(title: str, text: str, parent, detail: str = None):
        return messagebox.showerror(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def showwarning(title: str, text: str, parent, detail: str = None):
        return messagebox.showwarning(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askyesno(title: str, text: str, parent, detail: str = None):
        return messagebox.askyesno(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askyesnocancel(title: str, text: str, parent, detail: str = None):
        return messagebox.askyesnocancel(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askquestion(title: str, text: str, parent, detail: str = None):
        return messagebox.askquestion(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askokcancel(title: str, text: str, parent, detail: str = None):
        return messagebox.askokcancel(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askretrycancel(title: str, text: str, parent, detail: str = None):
        return messagebox.askretrycancel(title, text, parent=parent, detail=detail, icon="question")


class Button(tk.Button):
    def __init__(self, parent, text: str = "", width: int = 1, padding: int = 1, foreground: str = "#FFFFFF",
                 background: str = "#000000", highlight: str = None, font: str = "Arial", font_size: int = 15):
        super().__init__(master=parent, text=text, width=width, padx=padding, pady=padding, foreground=foreground,
                         background=background, font=(font, font_size), activeforeground=foreground, activebackground=background, relief="flat")
        self.parent = parent
        self.text = text
        self.width = width
        self.padding = padding
        self.foreground = foreground
        self.background = background
        self.highlight = highlight

        if background is None:
            self.configure(bg=self.parent["bg"])

        self.bind("<Enter>", lambda x: self.__enter__())
        self.bind("<Leave>", lambda x: self.__leave__())
        # self.bind("<Button-1>", lambda x: self.__onclick__())

    def bind_function(self, function):
        self.configure(command=function)

    def __enter__(self):
        self.configure(background=self.highlight, foreground="white")

    def __leave__(self):
        self.configure(background=self.background, foreground=self.foreground, text=self.text)

    def __onclick__(self):
        self.configure(background="#888888")

