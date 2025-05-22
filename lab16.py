#task 1

class Author:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Book:
    def __init__(self, title, author: Author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"'{self.title}' by {self.author}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def search_books(self, keyword):
        return [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.name.lower()]


if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("1984", Author("George Orwell")))
    lib.add_book(Book("Brave New World", Author("Aldous Huxley")))

    print(lib.search_books("world"))  
    lib.remove_book("1984")           
    print(lib.books)               


#task 2

from datetime import datetime

class Book:
    def __init__(self, title):
        self.title = title
        self.is_available = True
        self.borrowed_by = None
        self.borrow_date = None

    def __repr__(self):
        status = "Available" if self.is_available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} ({status})"


class Library:
    def __init__(self):
        self.books = []
        self.history = []

    def add_book(self, book: Book):
        self.books.append(book)

    def borrow_book(self, title, user):
        for book in self.books:
            if book.title == title and book.is_available:
                book.is_available = False
                book.borrowed_by = user
                book.borrow_date = datetime.now()
                self.history.append({
                    "title": title,
                    "user": user,
                    "borrow_date": book.borrow_date.strftime("%Y-%m-%d")
                })
                return f"{user} borrowed '{title}'"
        return "Book not available"

    def return_book(self, title, user):
        for book in self.books:
            if book.title == title and book.borrowed_by == user:
                return_date = datetime.now()
                reading_days = (return_date - book.borrow_date).days
                book.is_available = True
                book.borrowed_by = None
                book.borrow_date = None
                self.history.append({
                    "title": title,
                    "user": user,
                    "return_date": return_date.strftime("%Y-%m-%d"),
                    "reading_days": reading_days
                })
                return f"{user} returned '{title}' after {reading_days} days"
        return "Return failed"

if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("Dune"))

    print(lib.borrow_book("Dune", "Alice"))
    print(lib.return_book("Dune", "Alice"))
    print(lib.history)


#task 3

import json


class Book:
    def __init__(self, title):
        self.title = title
        self.total_borrowed = 0
        self.total_reading_days = 0

    def borrow(self, days_read):
        self.total_borrowed += 1
        self.total_reading_days += days_read

    def get_statistics(self):
        if self.total_borrowed == 0:
            return None
        return {
            "title": self.title,
            "borrow_count": self.total_borrowed,
            "average_reading_days": round(self.total_reading_days / self.total_borrowed, 2)
        }


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def export_statistics(self, filename="statistics.json"):
        data = [book.get_statistics() for book in self.books if book.total_borrowed > 0]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    lib = Library()
    b1 = Book("Dune")
    b1.borrow(5)
    b1.borrow(7)

    b2 = Book("1984")
    b2.borrow(3)

    lib.add_book(b1)
    lib.add_book(b2)

    lib.export_statistics()
    print("Statistics exported.")
