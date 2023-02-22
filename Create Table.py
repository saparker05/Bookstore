'''
This code creates the table 'books' in the database 'ebookstore' and populates the table 
with some initial values. 
'''

import sqlite3

db = sqlite3.connect('ebookstore_db')   

cursor = db.cursor()

try:

    # Create the books table if it does not exist already. 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books( id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')

    db.commit()                           

    # Populate the initial rows of the table. 
    id1 = 3001
    title1 = 'A Tale of Two Cities'
    author1 = 'Charles Dickens'
    qty1 = 30

    id2 = 3002
    title2 = 'Harry Potter and the Philosopher\'s Stone'
    author2 = 'J.K. Rowling'
    qty2 = 40

    id3 = 3003
    title3 = 'The Lion, the Witch and the Wardrobe'
    author3 = 'C.S. Lewis'
    qty3 = 25

    id4 = 3004
    title4 = 'The Lord of the Rings'
    author4 = 'J.R.R. Tolkien'
    qty4 = 37

    id5 = 3005
    title5 = 'Alice in Wonderland'
    author5 = 'Lewis Carroll'
    qty5 = 12

    book_details = [(id1, title1, author1, qty1), 
                    (id2, title2, author2, qty2),
                    (id3, title3, author3, qty3),
                    (id4, title4, author4, qty4),
                    (id5, title5, author5, qty5) ]
    
    cursor.executemany('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', book_details)

    db.commit()


except Exception as e:    

    db.rollback()

finally:

    db.close()