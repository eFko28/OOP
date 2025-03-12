# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram

import datetime
import json
import os



class Book:
    def __init__(self, title: str, author: str, year: int, available: bool = True):
        self.title = title
        self.author = author
        self.year = year
        self.available = available

    def borrow(self):
        # Check if the book is already borrowed
        if self.available == False:
            error_message = f"Kniha '{self.title}' je již vypůjčená."
            raise ValueError(error_message)
        # Change the state to indicate the book is now borrowed
        self.available = False

    def return_book(self):
        # Check if the book is already available
        if self.available == True:
            error_message = f"Kniha '{self.title}' již byla dostupná."
            raise ValueError(error_message)
        # Change the state to indicate the book has been returned
        self.available = True

    def __str__(self):
        # Determine the availability status as a string
        if self.available:
            status = "Dostupná"
        else:
            status = "Nedostupná"
        # Construct the descriptive string for the book
        book_str = f"{self.title} - {self.author} ({self.year}) | Stav: {status}"
        return book_str

    def to_dict(self):
        # Convert the book object to a dictionary representation
        book_dictionary = {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self.available,
        }
        return book_dictionary

    @staticmethod
    def is_valid_year(year):
        # Get the current year from the system clock
        current_year = datetime.datetime.now().year
        # Check if the year is within the valid range
        if year >= 1440 and year <= current_year:
            return True
        else:
            return False

    @staticmethod
    def parse_from_string(str_book: str):
        # Split the string by the semicolon character
        parts = str_book.split(";")
        if len(parts) != 3:
            raise ValueError("Neplatný řetězec pro inicializaci knihy.")
        # Clean up each part of the string
        title_part = parts[0].strip()
        author_part = parts[1].strip()
        year_part_str = parts[2].strip()
        try:
            year_part = int(year_part_str)
        except Exception as e:
            raise ValueError("Rok knihy musí být číslo.") from e
        # Create and return a new Book instance
        new_book = Book(title=title_part, author=author_part, year=year_part)
        return new_book


class Ebook(Book):
    def __init__(self, title: str, author: str, year: int, file_format: str):
        # Initialize the parent Book class
        super().__init__(title, author, year)
        self.file_format = file_format

    def __str__(self):
        # Get the string from the parent class
        base_description = super().__str__()
        # Append Ebook-specific information
        extended_description = base_description + f" | Formát: {self.file_format}"
        return extended_description


class AudioBook(Book):
    def __init__(self, title: str, author: str, year: int, duration: float):
        # Initialize the parent Book class
        super().__init__(title, author, year)
        self.duration = duration

    def __str__(self):
        # Get the string from the parent class
        base_description = super().__str__()
        # Append AudioBook-specific information
        extended_description = base_description + f" | Délka: {self.duration}"
        return extended_description


class Library:
    def __init__(self):
        # Initialize the internal list to store books
        self.__books = []

    def add_book(self, book: Book):
        # Add a new book to the library
        self.__books.append(book)

    def remove_book(self, book: Book):
        # Remove a book from the library if it exists
        if book in self.__books:
            self.__books.remove(book)
        else:
            print("Kniha se nenašla v knihovně.")

    def list_books(self):
        # Enumerate and print all books in the library
        index = 1
        for i in self.__books:
            # Convert each book to its string representation
            book_info = str(i)
            print(f"{index}. {book_info}")
            index += 1

    def save_in_json(self, file_path: str):
        # Prepare a list to hold all book dictionaries
        books_dictionaries = []
        for book in self.__books:
            book_dict = book.to_dict()
            books_dictionaries.append(book_dict)
        # Write the list of books to a JSON file with formatting options
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(books_dictionaries, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def parse_from_json(file_path: str):
        # Create an empty library instance
        new_library = Library()
        # Open and read the JSON file content
        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                loaded_books = json.load(json_file)
            except json.JSONDecodeError as err:
                raise ValueError("Chyba při načítání JSON dat.") from err
            # Process each book dictionary and add it to the library
            for book_entry in loaded_books:
                title_value = book_entry.get("title", "")
                author_value = book_entry.get("author", "")
                year_value = book_entry.get("year", 0)
                available_value = book_entry.get("available", True)
                created_book = Book(title_value, author_value, year_value, available_value)
                new_library.add_book(created_book)
        # Return the populated library instance
        return new_library


# Define the JSON file path for storing and reading book data
JSON_FILE_PATH = "json/library.json"


if __name__ == "__main__":
    # Clear the console screen based on the operating system
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    #Added a book so that library.json has something
    """
    new_book = Book("Broučci", "Jan Karafiát", 1876, True)
    new_library = Library()    
    
    new_library.add_book(new_book)
    new_library.save_in_json(JSON_FILE_PATH)
    """

    # Load books from the JSON file into the library instance
    library = Library.parse_from_json(JSON_FILE_PATH)

    print("\033[1;32m--- Seznam knih v knihovně: ---\033[0m\n")
    
    # List all books currently in the library
    library.list_books()

    # Save the current library state back to the JSON file
    library.save_in_json(JSON_FILE_PATH)