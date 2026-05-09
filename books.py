def zone_time(borrow_time):
    import datetime  # import datetime
    import pytz
    timezone = pytz.timezone("Africa/Accra")
    current_time = datetime.datetime.now(timezone)
    future = (current_time + datetime.timedelta(days=borrow_time,
              hours=9)).replace(microsecond=0)
    now = future.strftime('%Y-%m-%d %H:%M:%S')
    return now


class Book:
    def __init__(self, title, year, author, borrow_time):
        self.title = title
        self.year = year
        self.author = author
        self.borrowed = False
        self.borrow_time = 0
        self.return_time = 0

    def book_state(self):
        status = f"Borrowed, due in {self.return_time}" if self.borrowed else "Not borrowed"
        print(
            f"{self.title} was published in the ({self.year}) by {self.author} - {status}")

    def borrow(self):
        self.return_datetime = zone_time(self.borrow_time)
        self.borrowed = True

    def return_book(self):
        self.return_datetime = 0
        self.borrowed = False
