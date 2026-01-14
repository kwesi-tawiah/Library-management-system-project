class Book:
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author
        self.borrowed = False

    def book_state(self):
        status = "borrowed" if self.borrowed else "not borrowed"
        print(
            f"{self.title} was published in the ({self.year}) by {self.author} - {status}")

    def borrow(self):
        self.borrowed = True

    def return_book(self):
        self.borrowed = False


book1 = Book("About", "1777", "James Brown")

book2 = Book("Planes", "2777", "Bruce")

book3 = Book("Quantum Physics", "1990", "Adjoa Kwartemaa Appiah")


class Library:

    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print("Book added to library.")

    def show_books(self):
        if self.books:
            for book in self.books:
                book.book_state()
        else:
            print("No book in the library.")

    def borrow_book(self, book):
        if self.books:
            if book in self.books and book.borrowed == False:
                book.borrow()
                print("Book borrowed.")
            elif book.borrowed == True:
                print("Book has been borrowed and is not available.")
            elif book not in self.books:
                print("Book is not in the library.")

    def return_books(self, book):
        if book not in self.books and book.borrowed == True:
            book.return_book()
            print("Book returned to library.")
        elif book in self.books:
            print("Book available in library.")


library = Library()

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.borrow_book(book1)
library.borrow_book(book1)
library.show_books()
