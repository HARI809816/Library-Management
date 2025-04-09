import csv
import os
import json

if not os.path.exists('books.csv'):
    with open('books.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Book Name"])

def main_menu():
    try:
        global role
        print("=========================================")
        print("Welcome to the Library Management System")
        print("1. admin\n2. student\n3. exit")
        role = int(input("Choose your role: "))
        if role not in [1, 2, 3]:
            print("Invalid choice. Please select 1 for admin or 2 for student.\n")
            main_menu()
        else:
            print("=========================================")
            print("Loading...\n")
            main()
    except NameError:
        print("Invalid input. Please enter a number.\n")
        main_menu()
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        main_menu()


def add_book():
    book_name = input("Enter book name to add: ")
    
    
    if os.path.exists("books_count.json"):
        with open("books_count.json", "r") as file:
            book_counts = json.load(file)
    else:
        book_counts = {}
    with open('books.csv', 'r') as file:
        books = list(csv.reader(file))
    
    found = False
    for row in books:       
        if row and row[0] == book_name:
            found = True
    
    if found:
            book_counts[book_name] += 1
            print(f"Book '{book_name}' already exists. Count updated to {book_counts[book_name]}.\n")

    else:
        
        book_counts[book_name] = 1
        with open('books.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([book_name])
            print(f"Book '{book_name}' added to the library.\n")

    
    with open("books_count.json", "w") as file:
        json.dump(book_counts, file, indent=4)
    


def remove_book():
    global book_counts

    book_to_remove = input("Enter book name to remove: ")
    with open("books_count.json", "r") as file:
            book_counts = json.load(file)
            book_counts.pop(book_to_remove, None)
   
    with open('books.csv', 'r') as file:
        books = list(csv.reader(file))

    found = False
    with open('books.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in books:
            if row and row[0] != book_to_remove:
                writer.writerow(row)
            else:
                found = True
    print("Book removed.\n" if found else "Book not found.\n")

def borrow_book():
    view_books()
    book_to_borrow = input("Enter the name of the book you want to borrow: ")
    with open('books.csv', 'r') as file:
        books = list(csv.reader(file))

    found = False
    with open('books.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in books:
            if row and row[0] == book_to_borrow and not found:
                writer.writerow(row) 
                found = True
                
                with open("books_count.json", "r") as count_file:
                    book_counts = json.load(count_file)
                if book_to_borrow in book_counts:
                    if book_counts[book_to_borrow] == 0:
                        print("Book will available Soon.\n")
                        return
                    else:
                        print(f"Book '{book_to_borrow}' borrowed.\n")
                        book_counts[book_to_borrow] -= 1
                with open("books_count.json", "w") as count_file:
                    json.dump(book_counts, count_file, indent=4)
            else:
                writer.writerow(row)

    if found:
        with open('borrowed.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([book_to_borrow])
        print(f"You have borrowed '{book_to_borrow}'.\n")
    else:
        print("Book not available or not found.\n")

def return_book():
    book_to_return = input("Enter the name of the book you want to return: ")
    with open('borrowed.csv', 'r') as file:
        borrowed_books = list(csv.reader(file))

    found = False
    with open('borrowed.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in borrowed_books:
            if row and row[0] == book_to_return and not found:
                found = True
                with open("books_count.json", "r") as count_file:
                    book_counts = json.load(count_file)
                if book_to_return in book_counts:
                    book_counts[book_to_return] += 1
                with open("books_count.json", "w") as count_file:
                    json.dump(book_counts, count_file, indent=4)
            else:
                writer.writerow(row)

    if found:
        #with open('books.csv', 'a', newline='') as file:
         #   writer = csv.writer(file)
         #   writer.writerow([book_to_return])
        with open('returned.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([book_to_return])
        print(f"You have returned '{book_to_return}'.\n")
    else:
        print("Book not found in borrowed list.\n")



# ---------- COMMON FUNCTION ----------
def view_books():
    print("\nAvailable Books:")
    
    with open("books_count.json", "r") as file:
        book_counts = json.load(file)


    with open('books.csv', 'r') as file:
        books = [row[0] for row in csv.reader(file) if row]
        books.sort()
        if books:
            for i, book in enumerate(books, 1):
                print(f"{i}. {book} -- {book_counts.get(book, 0)} copies available")
        else:
            print("No books available.")
    print()



# ---------- MAIN MENU ----------
def main():
    while True:
        if role == 1:
            print("\nADMIN MENU")
            print("1. Add Book\n2. Remove Book\n3. View Books\n4. Mainmenu")
            choice = input("Choose an option: ")
            print()
            print("=========================================")
            
            if choice == '1':
                add_book()
            elif choice == '2':
                remove_book()
            elif choice == '3':
                view_books()
            elif choice == '4':
                print()
                main_menu()
            else:
                print("Invalid choice.\n")

        elif role == 2:
            print("\nSTUDENT MENU")
            print("1. View Books\n2. Borrow Book\n3. Return Book\n4. Mainmenu ")
            choice = input("Choose an option: ")
            print()
            print("=========================================")
            if choice == '1':
                view_books()
            elif choice == '2':
                borrow_book()   
            elif choice == '3':
                return_book() 
            elif choice == '4':
                print()
                main_menu()
            else:
                print("Invalid choice.\n")
        elif role==3:
            print("Exiting the program.")
            break

main_menu()