# from inspect import AGEN_CLOSED

from second import librarian


class User():
    def __init__(self, name, age, sex):
        self.borrowed_books = []
        self.name = name
        self.age = age
        self.sex = sex
        self.borrowed = False

    def display_info(self):
        if self.borrow == True:
            if len(self.borrowed_books) > 1:
                status = "Has borrowed books"
            else:
                status = "Has borrowed a book"
        else:
            status = "Has not borrowed anything"
        print(f"""
Name: {self.name}
Age: {self.age}
Sex: {self.sex}
Status: {status}
No. of books borrowed: {self.borrowed_books.length()}
Books borrowed: {self.borrowed_books}""")

    def books_available(self):
        librarian.show_books()

    def borrow_a_book(self, title):
        if len(self.borrowed_books) == 5:
            print("The maximum books you can borrow has been reached.")
        else:
            if librarian.bookes:
                print("Waiting for permission....")
                if librarian.borrow_notifications(self.name, title):
                    print("Permission grated.")
                    for book in librarian.bookes:
                        if book.title == title and book.borrowed == False:
                            book.borrow()
                            print(f"Book borrowed from library.")
                            break
                        elif book.borrowed == True:
                            print("Book has been borrowed and is not available.")
                            break
                    else:
                        print("Book is not in the library.")
                else:
                    print("Permission denied.")
            else:
                print("No books in library.")
            self.borrowed_books.append(title)
            self.borrowed = True

    def return_a_book(self, title):
        if title not in self.borrowed_books:
            print("You did not borrow this book from this library.")
        else:
            if librarian.bookes:
                for book in librarian.bookes:
                    if book.title == title and book.borrowed == True:
                        book.return_book()
                        librarian.return_notifications()
                        print(f"Book returned to library.")
                    else:
                        print("Book not borrowed.")
                    print("Book is not in library.")
            else:
                print("No book in library.")
                self.borrowed_books.remove(title)
                self.borrowed = False


user1 = User("Bruce", "15", "male")
# ser3 = User("Adjoa Appiah", "17", "female")
# user4 = User("Ama", "19", "female")


# user1.borrow_a_book("About")
user1.books_available()
user1.borrow_a_book("About")
