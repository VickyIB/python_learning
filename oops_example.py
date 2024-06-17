class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"'{self.title}' by {self.author}"
    
class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available:
            book.is_available = False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed {book}.")
        else:
            print(f"Sorry, {book} is not available.")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.is_available = True
            self.borrowed_books.remove(book)
            print(f"{self.name} returned {book}.")
        else:
            print(f"{self.name} does not have {book}.")

    def __str__(self):
        return self.name
    
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added {book} to the library.")

    def list_books(self):
        for book in self.books:
            status = "available" if book.is_available else "not available"
            print(f"{book} is {status}.")

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        print(f"Book '{title}' not found in the library.")
        return None
    
# Create library instance
my_library = Library()

# Create book instances
book1 = Book("Five Point Someone", "Chetan Bhagat")
book2 = Book("One Night @ the Call Center", "Chetan Bhagat")
book3 = Book("The 3 Mistakes of My Life", "Chetan Bhagat")

# Add books to the library
my_library.add_book(book1)
my_library.add_book(book2)
my_library.add_book(book3)

# List all books in the library
print("\nListing all books in the library:")
my_library.list_books()

# Create member instance
member1 = Member("Vicky")

# Borrow and return books
print("\nBorrowing books:")
member1.borrow_book(book1)  # Vicky borrows "Five Point Someone"
member1.borrow_book(book2)  # Vicky borrows "One Night @ the Call Center"

print("\nListing all books in the library after borrowing:")
my_library.list_books()

print("\nReturning books:")
member1.return_book(book1)  # Vicky returns "Five Point Someone"

print("\nListing all books in the library after returning:")
my_library.list_books()