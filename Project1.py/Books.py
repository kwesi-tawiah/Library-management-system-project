def zone_time(borrow_time):
    import datetime
    import pytz
    timezone = pytz.timezone("Africa/Accra")
    current_time = datetime.datetime.now(timezone)
    future = (current_time + datetime.timedelta(days=borrow_time)
              ).strftime('%Y-%m-%d %H:%M:%S')
    # future = now.replace(microsecond=0)
    return current_time.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S'), future


class Book:
    def __init__(self, title, year, author, borrow_time):
        self.id = None
        self.title = title
        self.year = year
        self.author = author
        self.borrowed = False
        self.borrow_time = borrow_time
        self.return_time = 0
        self.datetime_borrowed = 0
        self.returned_time = 0

    def book_state(self):
        status = f"Borrowed, due in {self.return_time}" if self.borrowed else "Not borrowed"
        print(f"""
Title: {self.title}
Year: {self.year}
Author: {self.author}
Borrow_time: {self.borrow_time}
Status: {status}
""")

    def borrow(self):
        self.datetime_borrowed, self.return_time = zone_time(self.borrow_time)
        self.borrowed = True
        self.returned_time = 0

    def return_book(self):
        self.returned_time, _ = zone_time(self.borrow_time)
        self.borrowed = False
