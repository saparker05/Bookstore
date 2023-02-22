'''
This program is designed to be used by a bookstore clerk. The code allows them to: add new books to the database,
update book information, delete books from the database and search the database. 

Note: the code in the file 'Capstone V - create table' needs to be executed first to set up the table 'books' 
and populate it with initial values. 

'''

import sqlite3   


# Define a function to print the details of a book from the database in a user friendly manner. 
# The function takes in a list containing either the details of one book or multiple books.    
def print_books(book_details):    

    # Check if there is only one book to print. 
    if len(book_details) == 4 and isinstance(book_details[0], int):  

        print(f'''
Id:         {book_details[0]}
Title:      {book_details[1]}
Author:     {book_details[2]}
Quantity:   {book_details[3]}

        ''')

    # If there are multiple books, use a for loop to print the details of each book. 
    else:

        for each_book in book_details:  

            print(f'''
Id:         {each_book[0]}
Title:      {each_book[1]}
Author:     {each_book[2]}
Quantity:   {each_book[3]}

        ''')


# Define a function which allows the user to add a book to the database. 
def enter_book():

    # Check the current max id in the database so that a new id can be allocated. 
    cursor.execute('''SELECT MAX(id) FROM books''')
    max_id = cursor.fetchone()[0]

    # Allocate the new id to be one more than the current max id. 
    enter_id = max_id + 1   

    # Request the title and author of the book from the user and check that it doesn't already exist in the database. 
    enter_title = input("\nPlease enter the title of the book: ").strip()

    enter_author = input("\nPlease enter the author of the book: ").strip()   

    cursor.execute('''SELECT * FROM books WHERE Title = ? and Author = ?''', (enter_title, enter_author))
    book_check = cursor.fetchall()

    # If the book already exists, print an error message and return. 
    if book_check != []:
        print("\nERROR") 
        print("A book with the same title and author already exists in the database:")
        print_books(book_check)
        print("\nPlease select 'Update book' from the main menu instead if required. ")
        return

    # Use a while loop to request the quantity from the user and validate the input. 
    while True:

        try:
            enter_qty = int(input("\nPlease enter the quantity in stock: "))
            break

        except ValueError:
            print("Input Error: quantity entered should be a positive intger. Please try again.")

    # Add the book to the database. 
    try:

        cursor.execute('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', (enter_id, enter_title, enter_author, enter_qty))

        db.commit()

        print(f"{enter_title} by {enter_author} has been added to the database with unique id = {enter_id}")

    except Exception as e:
        print("Error: changes have not been made.")
        print(f"Error details: {e}")
        db.rollback()


# Define a function which allows the user to update the details of a book in a database. 
def update_book():          
    
    # Check the user has the book id. 
    update_check = input('''
    The id number of the book is required to update the details of a book in the database. If you have the id number please
    press enter to continue. Alternatively, enter r to return to the main menu and search for the id number. ''').strip().lower()

    if update_check == 'r':
        return
    
    else:

        # Use a while loop to request the book id from the user and validate the input. 
        while True:

            try:
                update_id = int(input("\nPlease enter the id number of the book you wish to update: "))
                cursor.execute('''SELECT * FROM books WHERE id = ?''', (update_id,))
                update_book = cursor.fetchone()
                break

            except ValueError:
                print("\nInput error: the book id number should be an integer greater than 3000. Please try again.")

        # If the book is found in the database, display a menu for the user to select which details need to be updated. 
        if update_book is not None:

            # Display the details of the book the user has selected to update.
            print_books(update_book)

            while True:
                
                update_choice = input('''
Please select from the following:

        1. Update the title of the book
        2. Update the author of the book
        3. Update the quantity in stock
        0. Return to the main menu

            ''')
                
                # If the user selects to update the title, request the new title and update this in the database. 
                if update_choice == '1':
                    
                    update_title = input("\nPlease enter the updated title: ")

                    try:
                        cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (update_title, update_id))
                        db.commit()
                        print(f"\nConfirmation: title has been updated to {update_title}.")

                    except Exception as e:
                        print("Error: changes have not been made.")
                        print(f"Error details: {e}")
                        db.rollback()

                # If the user selects to update the author, request the new author and update this in the database. 
                elif update_choice == '2':
                    
                    update_author = input("\nPlease enter the updated author: ")

                    try:
                        cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (update_author, update_id))
                        db.commit()
                        print(f"\nConfirmation: author has been updated to {update_author}.")

                    except Exception as e:
                        print("Error: changes have not been made.")
                        print(f"Error details: {e}")
                        db.rollback()

                # If the user selects to update the quantity in stock, request the new quantity and update this in the database. 
                elif update_choice == '3':

                    # Use a while loop to validate the user's input for the updated quantity. 
                    while True:
                    
                        try:
                            update_qty = int(input("\nPlease enter the updated quantity in stock: ").strip())
                            
                            try:
                                cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (update_qty, update_id))
                                db.commit()
                                print(f"\nConfirmation: quantity in stock has been updated to {update_qty}.")

                            except Exception as e:
                                print("Error: changes have not been made.")
                                print(f"Error details: {e}")
                                db.rollback()

                            break

                        except ValueError:
                            print("\nQuantity entered should be an integer, please try again.")

                elif update_choice == '0':
                    return
                
                else: 
                    print("\nError: selection not made. Please try again.")

        # Print an error message if the book cannot be found in the database. 
        else:
            print("\nBook ID not found. Please select 'Search books' from the main menu to check the ID of a book if required.")


# Define a function which allows the user to delete a book from the database. 
def delete_book():

    # Check that the user has the id number of the book. 
    delete_check = input('''
    The id number of the book is required to delete the book from the database. If you have the id number please
    press enter to continue. Alternatively, enter r to return to the main menu and search for the id number. ''').strip().lower()

    if delete_check == 'r':
        return
    
    else:

        # Use a while loop to request the book id from the user and validate the input. 
        while True:

            try:
                delete_id = int(input("\nPlease enter the id of the book you wish to delete: "))
                break

            except ValueError:
                print("Input error: the book id number should be an integer greater than 3000. Please try again.")

        cursor.execute('''SELECT * FROM books WHERE id = ?''', (delete_id,))
        delete_book_check = cursor.fetchone()

        # If the book is found, first ask the user to confirm they want to delete it. 
        if delete_book_check is not None:

            while True:
                print(f"\nIs this the book you wish to delete: ")
                print_books(delete_book_check)
                delete_confirmation = input("Please enter Y to confirm or N to return to the main menu: ").lower().strip()

                if delete_confirmation == 'y':

                    try:
                        cursor.execute('''DELETE FROM books WHERE id = ?''', (delete_id,))
                        print("Delete confirmed.")
                        db.commit()

                    except Exception as e:
                        print("Error: changes have not been made.")
                        print(f"Error details: {e}")
                        db.rollback()

                    break

                # Cancel the delete if required by the user. 
                elif delete_confirmation == 'n':
                    print("Delete cancelled.")
                    break

                else:
                    print("Input error: please try again.")

        # Display an error message if the book was not found in the database. 
        else:
            print("\nBook ID not found. Please select 'Search books' from the main menu to check the ID of a book if required.")

    
# Define a function which allows the user to search the database for books. 
def search_books():

    # Display a menu to the user where they can select how they would like to search for the book. 
    while True:
        
        search_menu = input('''
Please select how you would like to search for the book:
        
1. by id 
2. by Title
3. by Author

Please enter 1, 2, or 3 to make your selection: ''')
        
        # If the user selects to search by id, use a while loop to request the id and validate the input. 
        if search_menu == '1':

            while True:
                try:
                    search_id = int(input("\nPlease enter the id of the book: "))

                    if search_id > 3000:
                        break
                    else:
                        print("Input error: the book id should be an intger greater than 3000. Please try again")

                except ValueError:

                    print("Input error: the book id should be an intger greater than 3000. Please try again")

            # Once a valid id has been entered, search for the book and call the print_books function to display the results to the user.
            cursor.execute('''SELECT * FROM books WHERE id = ?''', (search_id,))    
            book = cursor.fetchone()

            if book is not None:
                print_books(book)    

            else:
                print(f"\nBook with id = {search_id} not found.")
            
            break

        # If the user selects to search by title, request the title, search the database and call the print_books function to display the results to the user.
        elif search_menu == '2':

            search_title = input("Please enter the title of the book: ").strip()

            cursor.execute('''SELECT * FROM books WHERE Title = ?''', (search_title,))
            book = cursor.fetchall()

            if book is not None:
                print_books(book)   

            else:
                print(f"\nBook with title = {search_title} not found.")

            break

        # # If the user selects to search by title, request the title, search the database and call the print_books function to display the results to the user.
        elif search_menu == '3':

            search_author = input("Please enter the author of the book: ").strip()

            cursor.execute('''SELECT * FROM books WHERE Author = ?''', (search_author,))
            book = cursor.fetchall()
            
            if book is not None:
                print_books(book)

            else:
                print(f"\nBook with author = {search_author} not found.")

            break

        else:
            print("\nError: selection not made. Please try again.\n")


# Define a function which displays a main menu to the user and calls the appropriate function based on their selection. 
def main_menu():

    while True:

        menu = input('''

        MAIN MENU

Please select from the following options:

        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit 

Enter 1, 2, 3, 4, or 0 to make your selection: ''').strip()

        # If the user selects 'Enter book' call the function enter_book. 
        if menu == '1':  
            enter_book()   

        # If the user selects 'Update book' call the function update_book.
        elif menu == '2':
            update_book()

        # If the user selects 'Delete book' call the function delete_book.
        elif menu == '3':
            delete_book()

        # If the user selects 'Search books' call the function search_books.
        elif menu == '4':
            search_books()

        elif menu == '0': 
            print('\nGoodbye!!!\n')
            exit()

        else: 
            print("You have made a wrong choice, please try again.")


try: 
    # Connect to the ebookstore database and call the main_menu function. 
    db = sqlite3.connect('ebookstore_db')   
    cursor = db.cursor()
    main_menu()

except Exception as e:
    print(e)
    db.rollback()

finally:
    db.close()
