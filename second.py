import books


class Library:
    def __init__(self):
        self.bookes = []
        self.users = []

    def add_book(self, title, year, author, borrow_time):
        book = books.Book(title, year, author, borrow_time)
        self.bookes.append(book)
        print("Book added to library.")

    def show_books(self):
        if self.bookes:
            for book in self.bookes:
                book.book_state()
        else:
            print("No book in the library.")

    def show_users(self):
        for user in self.users:
            print(user)

    def borrow_notifications(self, name, title):
        while True:
            permission = input(
                f"A user named {name} want to borrow {title}. Do you permit?(YES/NO) ")
            if permission.lower() == "yes":
                self.users.append(title)
                return True
            elif permission.lower() == "no":
                return False
            else:
                print("Invalid input. Please try again.")
                continue

    def return_notifications(self, name, title):
        print(
            f"A user named {name.capitalize()} has returned the book, {title.capitalize()}.")


librarian = Library()

librarian.add_book("About", "1777", "James Brown", 8)
librarian.add_book("Planes", "2777", "Bruce", 9)
librarian.add_book("Quantum Physics", "1990", "Adjoa Kwartemaa Appiah", 10)
librarian.show_users()
