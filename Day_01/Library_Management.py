class Library:
    def __init__(self, name:str):
        self.name = name
        self.books = []        
        self.lend_data = {}

    def add_book(self, book_name:str):
        self.books.append(book_name)
        print(f"'{book_name}' has been added to the library.")
        print()

    def display_books(self):
        print(f"\nBooks available in {self.name}:")
        if len(self.books) == 0:
            print("No books available.")
        else:
            for index, book in enumerate(self.books, start=1):  
                print(f"Book: {index} - {book}")
        print()

    def lend_book(self, book_name:str,user:str):
        if book_name in self.lend_data:
            print(f"Sorry, '{book_name}' is already lent to {self.lend_data[book_name]}.")
        elif book_name not in self.books:
            print(f"The book '{book_name}' is not available in the library.")
        else:
            self.lend_data[book_name] = user
            print(f"'{book_name}' has been lent to {user}.")

    def return_book(self, book_name:str):
        if book_name in self.lend_data:
            del self.lend_data[book_name]
            print(f"'{book_name}' has been returned to the library.")
        else:
            print(f"'{book_name}' was not borrowed.")

    def show_lent_books(self):
        print("\nCurrently lent books:")
        if len(self.lend_data) == 0:
            print("No books are currently lent out.")
        else:
            for book, user in self.lend_data.items():
                print(f"'{book}' borrowed by {user}")
        print()



my_library = Library("My Library Management System")

while True:
        print(f"\n===== LIBRARY MENU =====\nWelcome to {my_library.name}")
        print("1. Display all books")
        print("2. Add a new book")
        print("3. Lend a book")
        print("4. Return a book")
        print("5. Show lent books")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            my_library.display_books()

        elif choice == '2':
            book_name = input("Enter the name of the book to add: ")
            my_library.add_book(book_name)

        elif choice == '3':
            book_name = input("Enter the name of the book to lend: ")
            user = input("Enter the name of the borrower: ")
            my_library.lend_book(book_name, user)

        elif choice == '4':
            book_name = input("Enter the name of the book to return: ")
            my_library.return_book(book_name)

        elif choice == '5':
            my_library.show_lent_books()

        elif choice == '6':
            print("\nExiting Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")