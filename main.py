import json
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def check_inventory():
    data_inventory = sparepart_entry.get().title()
    if data_inventory == "":
        messagebox.showerror(
            message="Please Don't leave any fields empty!",
            title="Error Message"
        )
    else:
        try:
            with open("data.json", 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(
                title='Error',
                message=f'{data_inventory} not in data inventory!'
            )
        else:
            if data_inventory in data:
                search_data = data[data_inventory]
                messagebox.showinfo(
                    title=f'Inventory',
                    message=f'Record for {data_inventory}:\nBalance = {search_data["amount"]}{search_data["units"]}'
                )
            else:
                messagebox.showinfo(
                    title="Inventory Not Found!",
                    message=f"No Inventory record for {data_inventory}"
                )

def check_balance(inventory, amount):
    data_inventory = inventory.get().title()
    data_amount = amount.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            try:
                if int(data_amount) <= int(data[data_inventory]["amount"]):
                    return True
                else:
                    return False
            except KeyError:
                return True
    except FileNotFoundError:
        return True


def check_unit(inventory, unit):
    data_inventory = inventory.get().title()
    data_unit = unit.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            try:
                if data_unit == data[data_inventory]["units"]:
                    return True
                else:
                    return False
            except KeyError:
                return True
    except FileNotFoundError:
        return True

def update_data(data, new_data):
    data.update(new_data)
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

def check(inventory, amount, unit):
    data_inventory = inventory.get().title()
    data_amount = amount.get().title()
    data_unit = unit.get().lower()
    new_data = {
        data_inventory: {
            "amount": data_amount,
            "units": data_unit
        }
    }
    condition = [
        data_inventory == '',
        data_amount == '',
    ]
    if any(condition):
        messagebox.showerror(
            title="Error!",
            message="Please Don't leave any fields empty!"
        )
    else:
        if data_amount.isdigit():
            if check_unit(inventory, unit):
                ask_ok = messagebox.askokcancel(
                    title="Inventory",
                    message=f"Inventory: {data_inventory}\nAmount: {data_amount}{data_unit}\n\nClick 'Ok' to save, click 'CANCEL' to return"
                )
                if ask_ok:
                    try:
                        with open("data.json", "r") as data_file:
                            data = json.load(data_file)
                    except FileNotFoundError:
                        with open("data.json", "w") as data_file:
                            json.dump(new_data, data_file, indent=4)
                    else:
                        if data_inventory in data:
                            json_data = int(data[data_inventory]["amount"])
                            input_data = int(data_amount)
                            if data_amount == sparepart_in_entry_amount.get():
                                new_data[data_inventory]["amount"] = str(json_data + input_data)
                                update_data(data, new_data)
                                clear_all(inventory, amount, unit)
                                if sparepart_out_entry_amount.get() != '':
                                    sparepart_out_entry_amount.delete(0, END)
                            elif data_amount == sparepart_out_entry_amount.get() and check_balance(inventory, amount):
                                new_data[data_inventory]["amount"] = str(json_data - input_data)
                                update_data(data, new_data)
                                clear_all(inventory, amount, unit)
                                if sparepart_in_entry_amount.get() != '':
                                    sparepart_in_entry_amount.delete(0, END)
                            else:
                                messagebox.showerror(
                                    title="Data Error!",
                                    message=f"Balance not enough to take out!"
                                )
                        else:
                            if sparepart_in_entry_amount.get() != '':
                                update_data(data, new_data)
                                clear_all(inventory, amount, unit)
                                if sparepart_out_entry_amount.get() != '':
                                    sparepart_out_entry_amount.delete(0, END)
                            elif sparepart_out_entry_amount.get() != '':
                                messagebox.showerror(
                                    title="Data Error!",
                                    message=f"Stock not available to takeout!"
                                )
                            # else:
                            #     update_data(data, new_data)
                            #     clear_all(inventory, amount, unit)
            else:
                messagebox.showerror(
                    title="Value Error!",
                    message=f"Please change unit type!"
                )
        else:
            messagebox.showerror(
                title="Type Error!",
                message="Please enter an amount!"
            )

def check_in():
    check(sparepart_entry, sparepart_in_entry_amount, in_units)
    refresh()

def check_out():
    check(sparepart_entry, sparepart_out_entry_amount, out_units)
    refresh()

def clear_all(inventory, amount, unit):
    data_inventory = inventory.get().title()
    data_unit = unit.get().lower()
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
    messagebox.showinfo(
        title="Inventory Updated!",
        message=f'{data_inventory} was updated and the current balance is:\n{data[data_inventory]["amount"]}{data_unit}'
    )
    inventory.delete(0, END)
    amount.delete(0, END)

def refresh():
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
    stock = [list for list in data ]
    sparepart_entry['values'] = stock
    return sparepart_entry['values']

def json_to_excel():
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)
    dataframe = pd.DataFrame(json_data)
    dataframe.to_excel("storekeeper.xlsx", index=False)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Maintenance Inventory")
window.config(background="white")
window.geometry("500x380")

canvass = Canvas(width=375, height=200, bg="white", highlightthickness=0)
inv_logo = PhotoImage(file="img/inv.png")
canvass.create_image(250, 100, image=inv_logo)
canvass.grid(column=0, row=0, pady=5, columnspan=4)

sparepart = Label(text="Inventory:", bg="white", font=("arial", "10"), pady=10, padx=5)
sparepart.grid(column=0, row=2)
sparepart_in = Label(text="Amount In:", bg="white", font=("arial", "10"))
sparepart_in.grid(column=0, row=3)
sparepart_out = Label(text="Amount Out:", bg="white", font=("arial", "10"), pady=10, padx=5)
sparepart_out.grid(column=0, row=4)

# sparepart_entry =Entry(width=43, highlightthickness=3)
# sparepart_entry.grid(column=1, row=2, columnspan=3)
sparepart_in_entry_amount =Entry(width=25, highlightthickness=3, justify="right")
sparepart_in_entry_amount.grid(column=1, row=3)
sparepart_out_entry_amount =Entry(width=25, highlightthickness=3, justify="right")
sparepart_out_entry_amount.grid(column=1, row=4)

check_button = Button(text="Check", highlightthickness=0, width=12, command=check_inventory)
check_button.grid(column=4, row=2, padx=10)
check_button = Button(text="Check-in", highlightthickness=0, width=12, command=check_in)
check_button.grid(column=4, row=3, padx=10)
check_button = Button(text="Check-out", highlightthickness=0, width=12, command=check_out)
check_button.grid(column=4, row=4, padx=10)
check_button = Button(text="Print Out Balance", highlightthickness=0, width=52, command=json_to_excel)
check_button.grid(column=1, row=5, columnspan=4)
# check_button = Button(text="Refresh", highlightthickness=0, width=52, command=refresh)
# check_button.grid(column=1, row=5, columnspan=4, pady=10)

sparepart_entry = ttk.Combobox(window, width=40)
refresh()
sparepart_entry.grid(column=1, row=2, columnspan=3)

in_units = ttk.Combobox(window, width=10)
in_units.insert(0, "units")
in_units['values'] = ('units',
                   'kg',
                   'meter',
                   'pcs',
                   )
in_units.grid(column=3, row=3)

out_units = ttk.Combobox(window, width=10)
out_units.insert(0, "units")
out_units['values'] = ('units',
                   'kg',
                   'meter',
                   'pcs',
                   )
out_units.grid(column=3, row=4)



window.mainloop()

#
#
#
#
# import json
# import pandas as pd
# from tkinter import *
# from tkinter import ttk, messagebox, filedialog
# import os
#
# # data_search = [data[i]['type'] for i in range(len(data)) if data[i]['type'] == "Lampu 10W"]
#
# def check(inventory, amount, unit):
#     data_inventory = inventory.get().title()
#     data_amount = amount.get().title()
#     data_unit = unit.get().lower()
#     # new_data = {
#     #     data_inventory: {
#     #         "amount": data_amount,
#     #         "units": data_unit
#     #     }
#     # }
#     entry = {"type": data_inventory, "amount": data_amount, "unit": data_unit}
#     condition = [
#         data_inventory == '',
#         data_amount == '',
#     ]
#     if any(condition):
#         messagebox.showerror(
#             title="Error!",
#             message="Please Don't leave any fields empty!"
#         )
#     else:
#         if data_amount.isdigit():
#             if check_unit(inventory, unit):
#                 ask_ok = messagebox.askokcancel(
#                     title="Inventory",
#                     message=f"Inventory: {data_inventory}\nAmount: {data_amount}{data_unit}\n\nClick 'Ok' to save, click 'CANCEL' to return"
#                 )
#                 if ask_ok:
#                     try:
#                         with open("data.json", "r") as data_file:
#                             data = json.load(data_file)
#                     except FileNotFoundError:
#                         update_data(data, entry)
#                     else:
#                         data_search = [True for i in range(len(data)) if data[i]['type'] == data_inventory]
#                         if data_search:
#                             data_search_inventory = [i for i in data if i['type'] == data_inventory][0]
#                             data_amount_json = [i['amount'] for i in data if i['type'] == data_inventory][0]
#                             input_data = int(data_amount)
#                             if data_amount == sparepart_in_entry_amount.get():
#                                 data_search_inventory["amount"] = str(int(data_amount_json) + input_data)
#                                 with open("data.json", "w") as feedjson:
#                                     json.dump(data, feedjson, indent=4)
#                                 clear_all(inventory, amount)
#                                 if sparepart_out_entry_amount.get() != '':
#                                     sparepart_out_entry_amount.delete(0, END)
#                             elif data_amount == sparepart_out_entry_amount.get() and check_balance(inventory, amount):
#                                 data_search_inventory["amount"] = str(int(data_amount_json) - input_data)
#                                 with open("data.json", "w") as feedjson:
#                                     json.dump(data, feedjson, indent=4)
#                                 clear_all(inventory, amount)
#                                 if sparepart_in_entry_amount.get() != '':
#                                     sparepart_in_entry_amount.delete(0, END)
#                             else:
#                                 messagebox.showerror(
#                                     title="Data Error!",
#                                     message=f"Balance not enough to take out!"
#                                 )
#                         else:
#                             if sparepart_in_entry_amount.get() != '':
#                                 update_data(data, entry)
#                                 clear_all(inventory, amount)
#                                 if sparepart_out_entry_amount.get() != '':
#                                     sparepart_out_entry_amount.delete(0, END)
#                             elif sparepart_out_entry_amount.get() != '':
#                                 messagebox.showerror(
#                                     title="Data Error!",
#                                     message=f"Stock not available to takeout!"
#                                 )
#                             # else:
#                             #     update_data(data, new_data)
#                             #     clear_all(inventory, amount, unit)
#             else:
#                 messagebox.showerror(
#                     title="Value Error!",
#                     message=f"Please change unit type!"
#                 )
#         else:
#             messagebox.showerror(
#                 title="Type Error!",
#                 message="Please enter an amount!"
#             )
#
# def open_excel():
#     variable = "data inventory.xlsx"
#     os.system('"%s"' % variable)
#
# def check_unit(inventory, unit):
#     data_inventory = inventory.get().title()
#     data_unit = unit.get().lower()
#     try:
#         with open("data.json", "r") as data_file:
#             data = json.load(data_file)
#             try:
#                 data_unit_json = [i['unit'] for i in data if i['type'] == data_inventory][0]
#                 if data_unit == data_unit_json:
#                     return True
#                 else:
#                     return False
#             except IndexError:
#                 return True
#     except FileNotFoundError:
#         return True
#
# def check_balance(inventory, amount):
#     data_inventory = inventory.get().title()
#     data_amount = amount.get().lower()
#     try:
#         with open("data.json", "r") as data_file:
#             data = json.load(data_file)
#             try:
#                 data_amount_json = [i['amount'] for i in data if i['type'] == data_inventory][0]
#                 if int(data_amount) <= int(data_amount_json):
#                     return True
#                 else:
#                     return False
#             except KeyError:
#                 return True
#     except FileNotFoundError:
#         return True
#
# def check_in():
#     check(sparepart_entry, sparepart_in_entry_amount, in_units)
#     list_inventory()
#     sorted_json_data()
#
# def check_out():
#     check(sparepart_entry, sparepart_out_entry_amount, out_units)
#     list_inventory()
#     sorted_json_data()
#
# def update_data(data, entry):
#     with open("data.json", "w") as feedjson:
#         data.append(entry)
#         json.dump(data, feedjson, indent=4)
#
# def clear_all(inventory, amount):
#     data_inventory = inventory.get().title()
#     with open("data.json", "r") as data_file:
#         data = json.load(data_file)
#     data_amount_json = [i['amount'] for i in data if i['type'] == data_inventory][0]
#     data_unit_json = [i['unit'] for i in data if i['type'] == data_inventory][0]
#     messagebox.showinfo(
#         title="Inventory Updated!",
#         message=f'{data_inventory} was updated and the current balance is:\n{data_amount_json}{data_unit_json}'
#     )
#     inventory.delete(0, END)
#     amount.delete(0, END)
#     with open("data.json") as new_data_file:
#         data_refresh = json.load(new_data_file)
#     inventory.delete(0, END)
#     sorted_json_data()
#     dataframe = pd.DataFrame(data_refresh)
#     dataframe.to_excel('data inventory.xlsx', index=False)
#
# def list_inventory():
#     with open("data.json", 'r') as data_file:
#         data = json.load(data_file)
#     stock = [list["type"] for list in data]
#     sparepart_entry['values'] = stock
#     return sparepart_entry['values']
#
# def check_inventory():
#     data_inventory = sparepart_entry.get().title()
#     if data_inventory == "":
#         messagebox.showerror(
#             message="Please Don't leave any fields empty!",
#             title="Error Message"
#         )
#     else:
#         try:
#             with open("data.json", 'r') as data_file:
#                 data = json.load(data_file)
#         except FileNotFoundError:
#             messagebox.showerror(
#                 title='Error',
#                 message=f'{data_inventory} not in data inventory!'
#             )
#         else:
#             data_search = [True for i in range(len(data)) if data[i]['type'] == data_inventory]
#             if data_search != []:
#                 if data_search:
#                     data_amount_json = [data[i]['amount'] for i in range(len(data)) if data[i]['type'] == data_inventory][0]
#                     data_unit_json = [data[i]['unit'] for i in range(len(data)) if data[i]['type'] == data_inventory][0]
#                     messagebox.showinfo(
#                         title='Inventory',
#                         message=f'Record for {data_inventory}:\nBalance = {data_amount_json}{data_unit_json}'
#                     )
#             else:
#                 messagebox.showinfo(
#                     title="Inventory Not Found!",
#                     message=f"No Inventory record for {data_inventory}"
#                 )
#
# def sorted_json_data():
#     try:
#         with open("data.json") as data_file:
#             data = json.load(data_file)
#             rearrange = sorted(data, key=lambda k: k["type"], reverse=False)
#         with open("data.json", 'w') as trial:
#             json.dump(rearrange, trial, indent=4)
#     except FileNotFoundError:
#         data = []
#         with open("data.json", "w") as new_data:
#             json.dump(data, new_data)
#
# def delete_inventory(inventory):
#     data_inventory = inventory.get().title()
#     ask_ok = messagebox.askokcancel(
#         title="Delete Inventory!",
#         message=f"Are you sure want to remove '{data_inventory}' in the inventory list?"
#     )
#     if ask_ok:
#         new_data = []
#         with open("data.json") as data_file:
#             data = json.load(data_file)
#         for i in data:
#             if i["type"] == data_inventory:
#                 pass
#             else:
#                 new_data.append(i)
#         with open("data.json", "w") as delete_data:
#             json.dump(new_data, delete_data, indent=4)
#         with open("data.json") as new_data_file:
#             data_refresh = json.load(new_data_file)
#         inventory.delete(0, END)
#         list_inventory()
#         sorted_json_data()
#         dataframe = pd.DataFrame(data_refresh)
#         dataframe.to_excel('data inventory.xlsx', index=False)
#
# # ---------------------------- UI SETUP ------------------------------- #
#
# sorted_json_data()
# window = Tk()
# window.title("Maintenance Inventory")
# window.config(background="white")
# window.geometry("500x400")
#
# canvass = Canvas(width=375, height=200, bg="white", highlightthickness=0)
# inv_logo = PhotoImage(file="img/inv.png")
# canvass.create_image(250, 100, image=inv_logo)
# canvass.grid(column=0, row=0, pady=5, columnspan=4)
#
# sparepart = Label(text="Inventory:", bg="white", font=("arial", "10"), pady=10, padx=5)
# sparepart.grid(column=0, row=2)
# sparepart_in = Label(text="Amount In:", bg="white", font=("arial", "10"))
# sparepart_in.grid(column=0, row=3)
# sparepart_out = Label(text="Amount Out:", bg="white", font=("arial", "10"), pady=10, padx=5)
# sparepart_out.grid(column=0, row=4)
#
# # sparepart_entry =Entry(width=43, highlightthickness=3)
# # sparepart_entry.grid(column=1, row=2, columnspan=3)
# sparepart_in_entry_amount =Entry(width=25, highlightthickness=3, justify="right")
# sparepart_in_entry_amount.grid(column=1, row=3)
# sparepart_out_entry_amount =Entry(width=25, highlightthickness=3, justify="right")
# sparepart_out_entry_amount.grid(column=1, row=4)
#
# check_button = Button(text="Check", highlightthickness=0, width=12, command=check_inventory)
# check_button.grid(column=4, row=2, padx=10)
# check_button = Button(text="Check-in", highlightthickness=0, width=12, command=check_in)
# check_button.grid(column=4, row=3, padx=10)
# check_button = Button(text="Check-out", highlightthickness=0, width=12, command=check_out)
# check_button.grid(column=4, row=4, padx=10)
# check_button = Button(text="Delete Inventory", highlightthickness=0, width=52, command=lambda: delete_inventory(sparepart_entry))
# check_button.grid(column=1, row=5, columnspan=4, pady=10)
# check_button = Button(text="Open in Excel", highlightthickness=0, width=52, command=open_excel)
# check_button.grid(column=1, row=6, columnspan=4)
#
#
# sparepart_entry = ttk.Combobox(window, width=40)
# list_inventory()
# sparepart_entry.grid(column=1, row=2, columnspan=3)
#
# in_units = ttk.Combobox(window, width=10)
# in_units.insert(0, "units")
# in_units['values'] = ('units',
#                    'kg',
#                    'meter',
#                    'pcs',
#                    )
# in_units.grid(column=3, row=3)
#
# out_units = ttk.Combobox(window, width=10)
# out_units.insert(0, "units")
# out_units['values'] = ('units',
#                    'kg',
#                    'meter',
#                    'pcs',
#                    )
# out_units.grid(column=3, row=4)
#
#
# window.mainloop()
#


