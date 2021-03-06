#! /usr/bin/python3

# Cli program that performs SUID functions on a auto-generated to do list item SQLite3 embedded Database (in local fs)

import os
import sqlite3
import texttable
import time
from colorama import Fore, Back, Style, init


# DEFINITIONS

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


m_dashband = (ly + "+--------------+" + reset)


# FUNCTION DEFINITIONS

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
    print("                             ") # overwriting-white space as a catch-all to remove any process-animation-remnants


def generate_table_object(row_list, color, completed):
    if completed == True:
        table_obj = texttable.Texttable(0) # Generate texttable object
        table_obj.set_cols_align(["l", "l", "l", "l"]) # Column alignment
        table_obj.set_cols_valign(["t", "t", "t", "t"]) # Column vertical alignment
        table_obj.add_row(["id", "Task", "Details", "Completion Date"]) # Add header row
        for item in row_list:
            table_obj.add_row([str(item[0]), str(item[1]), str(item[2]), str(item[3])]) # Add individual rows
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
        table_obj = texttable.Texttable(0) # Generate texttable object
        table_obj.set_cols_align(["l", "l", "l", "l", "l", "l"]) # Column alignment
        table_obj.set_cols_valign(["t", "t", "t", "t", "t", "t"]) # Column vertical alignment
        table_obj.add_row(["id", "Task", "Details", "Creation Date", "Completed", "Completion Date"]) # Add header row
        for item in row_list:
            table_obj.add_row([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5])]) # Add individual rows
        print_texttable_object(table_obj, color)
    

def generate_table_object_prompt(options_list, color):
    prompt_table = texttable.Texttable(0) # instantiate table object from Texttable class
    align_list = ["c", "c"]
    valign_list = ["t", "t"]
    header_list = ["Option", "Operation"]
    prompt_table.set_cols_align(align_list)
    prompt_table.set_cols_valign(valign_list)
    prompt_table.add_row(header_list)
    i=1
    for item in options_list:
        prompt_table.add_row([str(i), item])
        i+=1
    print_texttable_object(prompt_table, color)



def print_texttable_object(texttable_object, color):
    print(color)
    print(texttable_object.draw())
    print(reset)


def select_statement_uncompleted():
    # Calling incomplete task-rows
    cursor = connection.cursor()
    rows = cursor.execute("SELECT id, task_name, details, creation_date FROM to_do_list WHERE completed=0;").fetchall()
    print(r + "\n\n  UNCOMPLETED ENTRIES" + reset)
    generate_table_object(rows, ly, False)

def select_statement_completed():
    # Calling completed task-rows
    cursor = connection.cursor()
    rows = cursor.execute("SELECT id, task_name, details, completion_date FROM to_do_list WHERE completed=1;").fetchall()
    print(r + "\n\n  COMPLETED ENTRIES" + reset)
    generate_table_object(rows, lb, True)


def select_statement_function(select_all, regex):
    os.system('clear')
    cursor = connection.cursor()
    if select_all == True:
        # Calling incomplete task-rows
        select_statement_uncompleted()
        # Calling completed task-rows
        select_statement_completed()
    elif select_all == False:
        buffer_animation("Loading", .2, "GREEN", 0)
        rows = cursor.execute("SELECT id, task_name, details, creation_date, completed, completion_date FROM to_do_list WHERE task_name LIKE ? ;", (regex,)).fetchall()
        generate_table_object(rows, ly, None)
    buffer_animation("Loading", .2, "GREEN", 0)


def insert_statement_function():
    os.system('clear')
    while True:
        select_statement_uncompleted()
        print(lb + "Enter task info" + reset + " (0 to return to main menu)")
        task_name = input(lb + "Task Name: " + reset)
        if task_name == "0":
            os.system('clear')
            break
            
        description = input(lb + "Details: " + reset)
        if description == "0":
            os.system('clear')
            break
        connection.execute("INSERT INTO to_do_list(task_name, details, creation_date, completed, completion_date) VALUES (?, ?, DATE(), 0, NULL)", (task_name, description))
        connection.commit()
        os.system('clear')
    os.system('clear')
    

def update_statement_function():
    os.system('clear')
    while True:
        select_statement_function(True, None)
        print("\n  UPDATE MENU  ")
        update_menu_prompt = ["MARK COMPLETED", "MARK UNCOMPLETED", "EDIT TASK NAME", "EDIT TASK DETAILS", "QUIT"]
        generate_table_object_prompt(update_menu_prompt, ly)
        option = input(lb + "--------> " + reset)
        option = int(option)
        os.system('clear')
        if option == 5:
            break
        elif option == 1:
            while True:
                select_statement_uncompleted()
                print(lb + "Enter id: " + reset + "(0 to return to previous menu)")
                task_id = input(lb + "Task id: " + reset)
                if task_id == "0":
                    break
                task_id = int(task_id)
                try:
                    connection.execute("UPDATE to_do_list set completed = 1, completion_date = DATE() WHERE id = ? ;", (task_id,))
                    connection.commit()
                except: 
                    print(r + "Error:" + reset + " Invalid task ID entry")
                os.system('clear')
        elif option == 2:
            while True:
                select_statement_completed()
                print(lb + "Enter id: " + reset + "(0 to return to previous menu)")
                task_id = input(lb + "Task id: " + reset)
                if task_id == "0":
                    break
                task_id = int(task_id)
                try:
                    connection.execute("UPDATE to_do_list set completed = 0, completion_date = NULL WHERE id = ? ;", (task_id,))
                    connection.commit()
                except:
                    print(r + "Error:" + reset + " Invalid task ID entry")
                os.system('clear')
        elif option == 3: # edit existing task name
            select_statement_function(True, None) # display all tasks regardless of completion status
            try:
                task_alter_id = input("ID of row task-name to alter (0 to return to previous menu)\n" + lb + "--------> " + reset)
                if task_alter_id == "0":
                    continue
                else:
                    task_alter_id = int(task_alter_id)
                    new_task_name = input("Enter new task name: ")
                    connection.execute("UPDATE to_do_list SET task_name = ? WHERE id = ?", (new_task_name, task_alter_id))
                    connection.commit()
            except:
                print(r + "Error: " + reset + "InvalidDataEntry")
                os.system('sleep 2')
        
        elif option == 4: # edit task details
            select_statement_function(True, None) # display all tasks regardless of completion status
            try:
                task_alter_id = input("ID of row details-column to alter (0 to return to previous menu)\n" + lb + "--------> " + reset)
                if task_alter_id == "0":
                    continue
                else:
                    task_alter_id = int(task_alter_id)
                    new_details_text = input("Enter new details section: ")
                    connection.execute("UPDATE to_do_list SET details = ? WHERE id = ?", (new_details_text, task_alter_id))
                    connection.commit()
            except:
                print(r + "Error: " + reset + "InvalidDataEntry")
                os.system('sleep 2')
            
        else:
            buffer_animation("Error: incorrect option", .2, "RED", 4)
        os.system('clear')
        


def delete_statement_function():
    # Display all entries
    os.system('clear')
    while True:
        print(r + "ALL LIST ENTRIES" + reset)
        select_statement_function(False, '%')
        # Select by ID which one to delete from the list
        print(lb + "Enter ID of row to delete" + reset + " (0 to return to main menu)")
        option = input(lb + "Task ID: " + reset)
        try:
            if int(option) == 0:
                break
            else:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM to_do_list WHERE id = ?", (option,))
                    connection.commit()
                    buffer_animation("DELETEING ROW", .2, "RED", 1)
        except ValueError:
            print(r + "Error: " + reset + "Invalid entry")
            os.system('sleep 2')
    os.system('clear')


# EXECUTIONS

# Form connection with datebase (create if non-existant) and create connection object
connection = sqlite3.connect('to_do_list_items.db')

# create 'to_do_list' table if not already created
try:
    connection.execute("CREATE TABLE to_do_list(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, details TEXT, creation_date DATE, completed BOOL, completion_date DATE)")
    connection.commit()
except sqlite3.OperationalError: # error if table already created
    print(r + "Existing 'to_do_list' table found\n\n" + reset)



# main event loop
runvar = True
while runvar == True:
    os.system('clear')
    select_statement_uncompleted()
    print(" MAIN MENU  ")
    main_menu_prompt = ["INSERT", "SELECT", "UPDATE", "DELETE", "QUIT"]
    generate_table_object_prompt(main_menu_prompt, ly)
    option = input(lb + "\n------------> " + reset)
    if option == str(5) or option == "quit":
        runvar = False
        buffer_animation("Quitting", .2, "RED", 4)
    elif option == str(2): # SELECT
        select_statement_option = input(ly + "View all entries:" + reset + c + " (y/n) " + reset)
        if select_statement_option == "y" or select_statement_option == "Y":
            select_statement_function(True, None)
        elif select_statement_option == "n" or select_statement_option == "N":
            search_term = input(r + "SQL REGEX" + lb + " --> " + reset)
            select_statement_function(False, search_term)

    elif option == str(1): # INSERT 
        buffer_animation("Loading", .2, "GREEN", 1)
        insert_statement_function()
    elif option == str(3): # UPDATE
        buffer_animation("Loading", .2, "GREEN", 1)
        update_statement_function()
    elif option == str(4): # DELETE
        buffer_animation("Loading deletion menu", .2, "RED", 1)
        delete_statement_function()



# ls directory contents so that immedediately after program terminates, it sets you on the path to accomplishing other tasks
os.system('clear && ls --color=auto')
connection.close()














