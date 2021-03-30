#! /usr/bin/python3

# Cli program that performs SUID functions on a auto-generated to do list item SQLite3 embedded Database (in local fs)

import sqlite3
import texttable
import time
from colorama import Fore, Back, Style, init


# style_format variable-definitions
b = Fore.BLUE
r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE
c = Fore.CYAN
m = Fore.MAGENTA
lb = Fore.LIGHTBLUE_EX
ly = Fore.LIGHTYELLOW_EX
reset = Style.RESET_ALL


m_dashband = (m + "------------------------------------------------------------------------------------------" + reset)


# Function-definitions

def buffer_animation(process, rate, color, repititions):
    if color == "RED":
        color = Fore.RED
    elif color == "GREEN":
        color = Fore.GREEN
    elif color == "YELLOW":
        color = Fore.YELLOW
    elif color == "CYAN":
        color = Fore.CYAN
    elif color == "LY":
        color = Fore.LIGHTYELLOW_EX
    i = 0
    while i < repititions:
        print(color + " " + str(process) + ".   " + Style.RESET_ALL, end='\r')
        time.sleep(rate)
        print(color + " " + str(process) + "..  " + Style.RESET_ALL, end='\r')
        time.sleep(rate)
        print(color + " " + str(process) + "... " + Style.RESET_ALL, end='\r')
        time.sleep(rate)
        i += 1


def generate_table_object(row_list, color, completed):
    if completed == True:
        table_obj = texttable.Texttable(0) # Generate texttable object
        table_obj.set_cols_align(["l", "l", "l", "l"]) # Column alignment
        table_obj.set_cols_valign(["t", "t", "t", "t"]) # Column vertical alignment
        table_obj.add_row(["id", "Task", "Details", "Completion Date"]) # Add header row
        for item in row_list:
            table_obj.add_row([str(item[0]), str(item[1]), str(item[2]), str(item[5])]) # Add individual rows
        print_texttable_object(table_obj, color)
    elif completed == False:
        table_obj = texttable.Texttable(0) # Generate texttable object
        table_obj.set_cols_align(["l", "l", "l", "l"]) # Column alignment
        table_obj.set_cols_valign(["t", "t", "t", "t"]) # Column vertical alignment
        table_obj.add_row(["id", "Task", "Details", "Creation Date"]) # Add header row
        for item in row_list:
            table_obj.add_row([str(item[0]), str(item[1]), str(item[2]), str(item[3])]) # Add individual rows
        print_texttable_object(table_obj, color)
    elif completed == None: # option allows indiscriminate search of entreies with REGEX for task and details
        print("Reached else if condition in generate_table_object function")
        pass


def print_texttable_object(texttable_object, color):
    print(color)
    print(texttable_object.draw())
    print(reset)


def select_statement_function(select_all, regex):
    cursor = connection.cursor()
    if select_all == True:
        # Calling incomplete task-rows
        rows = cursor.execute("SELECT id, task_name, details, creation_date FROM to_do_list WHERE completed=0;").fetchall()
        print(r + "\n\nUNCOMPLETED ENTRIES" + reset)
        generate_table_object(rows, ly, False)
        # Calling completed task-rows
        rows = cursor.execute("SELECT id, task_name, details, completion_date FROM to_do_list WHERE completed=1;")
        print(g + "\n\nCOMPLETED ENTRIES" + reset)
        generate_table_object(rows, lb, True)
    elif select_all == False:
        rows = cursor.execute("SELECT id, task_name, details, completed FROM to_do_list WHERE task_name LIKE ? ;", (regex,)).fetchall()
        generate_table_object(rows, ly, None)


def insert_statement_function(tsk, details):
    connection.execute("INSERT INTO to_do_list(task_name, details, creation_date, completed, completion_date) VALUES (?, ?, DATE(), 0, NULL", (tsk, details))
    connection.commit()

def update_statement_function():
    pass

def delete_statement_function():
    pass

connection = sqlite3.connect('to_do_list_items.db')

# create 'to_do_list' table if not already created
try:
    connection.execute("CREATE TABLE to_do_list(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, details TEXT, creation_date DATE, completed BOOL, completion_date DATE)")
    connection.commit()
except sqlite3.OperationalError: # error if table already created
    print(r + "Existing 'to_do_list' table found" + reset)


# main event loop
runvar = True
while runvar == True:
    print(m_dashband)
    print(ly + "Operations:\n" + reset)
    option = input(r + "1) " + g + "INSERT\n" + r + "2) " + g + "SELECT\n" + r + "3) " + g + "UPDATE\n" + r + "4) " + g +  "DELETE\n" + r + "5) " + g + "QUIT\n" + lb + "\n-------> " + reset)
    if option == str(5) or option == "quit":
        runvar = False
        buffer_animation("Quitting", .2, "RED", 5)
    
    elif option == str(2): # SELECT
        select_statement_option = input(ly + "View all entries:" + reset + c + " (y/n) " + reset)
        if select_statement_option == "y" or select_statement_option == "Y":
            select_statement_function(True, None)
        elif select_statement_option == "n" or select_statement_option == "N":
            search_term = input(r + "SQL REGEX" + lb + " --> " + reset)
            select_statement_function(False, search_term)

    elif option == str(1): # INSERT 
        buffer_animation("Loading", .2, "GREEN", 2)
        task_name = input(b + "Task Name: " + reset)
        description = input(b + "Details: " + reset)
        insert_statement_function(task_name, description)
    elif option == str(3): # UPDATE
        print("Update list items...")
    elif option == str(4): # DELETE
        print("Delete list item(s)...")





connection.close()












