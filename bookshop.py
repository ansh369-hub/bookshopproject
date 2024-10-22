# CREATE DATABASE BookStore;

# USE BookStore;

# CREATE TABLE books_stock (
# book_id INT PRIMARY KEY,
# title VARCHAR(100),
# author VARCHAR(100),
# price DECIMAL(10, 2),
# stock INT default 0);


# CREATE TABLE purchase_book (
# purchase_id INT PRIMARY KEY,
# book_id INT,
# quantity INT,
# purchase_date DATE,
# total_cost_price decimal(10,2),
# FOREIGN KEY (book_id) REFERENCES books_stock(book_id));

# CREATE TABLE book_sales (
# sale_id INT PRIMARY KEY,
# book_id INT,
# quantity INT,
# sale_date DATE,
# total_selling_price DECIMAL(10, 2),
# FOREIGN KEY (book_id) REFERENCES books_stock(book_id));


import mysql.connector
from datetime import datetime

# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='bookstore',
            )
        
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to add a new book
def add_book(conn):
    try:
        cursor = conn.cursor()
        book_id= int(input("Enter Book Id:"))
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        price = float(input("Enter book price: "))
        
        cursor.execute(
            "INSERT INTO books_stock (book_id,title, author, price) VALUES (%s,%s, %s, %s)",
            (book_id,title, author, price,)
        )
        conn.commit()
        print("Book added successfully!")
    except Exception as e:
        print(f"Error adding book: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to add a new book purchase
def add_purchase(conn):
    try:
        cursor = conn.cursor()
        purchase_id= int(input("Enter Purchase Id: "))
        book_id = int(input("Enter book ID of the purchased book: "))
        quantity = int(input("Enter quantity purchased: "))
        purchase_date_input = input("Enter date of purchase (YYYY-MM-DD):")
        purchase_date = datetime.strptime(purchase_date_input,"%Y-%m-%d").date()
        total_cost_price= float(input("Enter total cost price:"))

        # Check if the book exists in the books_stock table
        cursor.execute("SELECT * FROM books_stock WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        
        if book:
            cursor.execute("UPDATE books_stock set stock = stock + %s where book_id = %s",(quantity,book_id))
        
            cursor.execute("INSERT INTO purchase_book (purchase_id, book_id, quantity, purchase_date,total_cost_price) VALUES (%s,%s, %s, %s,%s)",
            (purchase_id, book_id, quantity, purchase_date, total_cost_price)
            )
            conn.commit()
            print("Purchase details recorded successfully!")
            
        else:
            # If the book does not exist, prompt for details
            print("Book not found in BOOK TABLE. Add the details about new book")


    except Exception as e:
        print(f"Error adding purchase details: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to edit book stock
def edit_stock(conn):
    while True:
        print("\n----------- Edit Book Records -----------")
        print("1. Update Book Quantity")        
        print("2. Update Book Price")
        print("3. Delete Book Record")
        print("4. Return to Main Menu")


        choice = input("Choose an option: ")

        if choice == '1':
            update_quantity(conn)
        elif choice == '2':
            update_price(conn)
        elif choice == '3':
            delete_book(conn)
        
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

# Function to update book quantity
def update_quantity(conn):
    try:
        cursor = conn.cursor()
        book_id = int(input("Enter book ID to update quantity: "))
        new_stock = int(input("Enter new stock quantity: "))

        cursor.execute("UPDATE books_stock SET stock = %s WHERE book_id = %s",(new_stock, book_id))
        conn.commit()
        if cursor.rowcount == 0:
            print("No book found with that ID.")
        else:
            print("Stock updated successfully!")
    except Exception as e:
        print(f"Error updating stock: {e}")
        
    finally:
        if cursor:
            cursor.close()

# Function to delete a book record
def delete_book(conn):
    try:
        cursor = conn.cursor()
        book_id = int(input("Enter book ID to delete: "))

        cursor.execute("DELETE FROM books_stock WHERE book_id = %s", (book_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print("No book found with that ID.")
        else:
            print("Book deleted successfully!")
    except Exception as e:
        print(f"Error deleting book: {e}")
    finally:
        if cursor:
            cursor.close()
        
def update_price(conn):
    try:
        cursor=conn.cursor()
        book_id=int(input("Enter Book Id to update price:"))
        new_price=float(input("Enter new Price:"))
        
        cursor.execute("UPDATE books_stock SET price = %s WHERE book_id = %s",(new_price, book_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            print("No book found with that ID.")
        else:
            print("Price updated successfully!")
    
    except ValueError:
        print("Invalid input. Please enter numeric values for Book ID and Price.")       
    except Exception as e:
        print(f"Error updating price: {e}")
        
    finally:
        if cursor:
            cursor.close()
        
# Function to enter new sales
def enter_sale(conn):
    try:
        cursor = conn.cursor()
        sale_id = int(input("Enter SalesId:"))
        book_id = int(input("Enter book ID sold: "))
        quantity = int(input("Enter quantity sold: "))
        sale_date_input = input("Enter Date of Sales(yyyy-MM-dd):")
        sale_date = datetime.strptime(sale_date_input,"%Y-%m-%d").date()

        # Fetch stock and price of the book
        cursor.execute("SELECT stock, price FROM books_stock WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()

        if result is None:
            print("No book found with that ID.")
            return

        stock, price = result

        if stock < quantity:
            print("Not enough stock available!")
            return

        # Calculate total sell price
        total_selling_price = price * quantity

        # Insert sale record

        cursor.execute("INSERT INTO book_sales (sale_id, book_id, quantity, sale_date, total_selling_price) VALUES (%s, %s, %s, %s, %s)",(sale_id, book_id, quantity, sale_date, total_selling_price))
        

        cursor.execute("UPDATE books_stock SET stock = stock - %s WHERE book_id = %s",(quantity, book_id))
        
        conn.commit()
        print("Sale recorded successfully!")
    except Exception as e:
        print(f"Error recording sale: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to view all books in stock
def view_books(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books_stock")
        books = cursor.fetchall()
        print("\nBooks in Stock:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Price: {book[3]}, Stock: {book[4]}")
    except Exception as e:
        print(f"Error retrieving books: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to search for books by title or author
def search_books(conn):
    try:
        cursor = conn.cursor()
        search_term = input("Enter title or author to search: ")
        cursor.execute(
            "SELECT * FROM books_stock WHERE title LIKE %s OR author LIKE %s",
            (f'%{search_term}%', f'%{search_term}%')
        )
        results = cursor.fetchall()
        if results:
            print("\nSearch Results:")
            for book in results:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Price: {book[3]}, Stock: {book[4]}")
        else:
            print("No books found matching that term.")
    except Exception as e:
        print(f"Error searching for books: {e}")
    finally:
        cursor.close()

# Function to generate sales report
def generate_sales_report(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_sales")
        sales = cursor.fetchall()
        print("\nSales Report:")
        for sale in sales:
            print(f"Sale ID: {sale[0]}, Book ID: {sale[1]}, Quantity: {sale[2]}, Selling Price:{sale[4]}, Sale Date: {sale[3]}")
    except Exception as e:
        print(f"Error retrieving sales report: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to display menu
def menu():
    conn = connect_db()
    if conn is None:
        return

    while True:
        print("\n-----------------------* Welcome To Our BookStore *---------------------------")
        
        print("1. Add a new book")
        print("2. Add new book purchase")
        print("3. Edit book records")
        print("4. Enter new sale")
        print("5. View all books")
        print("6. Search for books")
        print("7. Generate sales report")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book(conn)
        elif choice == '2':
            add_purchase(conn)
        elif choice == '3':
            edit_stock(conn)
        elif choice == '4':
            enter_sale(conn)
        elif choice == '5':
            view_books(conn)
        elif choice == '6':
            search_books(conn)
        elif choice == '7':
            generate_sales_report(conn)
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please try again.")

    conn.close()

# Entry point of the program
if __name__ == "__main__":
    menu()

