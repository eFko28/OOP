# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram
"""_summary_
OOP_Books_Library_02.py

# Možnosti rozšíření lekce – Knihovna
---

## 1️⃣ Přidání více tříd (dědičnost) – rozšíření knihovny
- Doplnění tříd **Ebook** a **AudioBook**, které budou dědit z `Book`.
- Každá z těchto tříd bude mít nové atributy:
  - `Ebook` → atribut `file_format` (PDF, EPUB, MOBI).
  - `AudioBook` → atribut `duration` (délka audioknihy v minutách).

### **Nové zadání pro studenty**
- Rozšířit třídu `Book` o podtřídy `Ebook` a `AudioBook`.
- Přepsat metodu `__str__()` tak, aby zobrazovala i nové atributy.

---

## 2️⃣ Implementace statických metod a metod třídy
- Přidání **statické metody** `is_valid_year(year)`, která ověří, zda je rok vydání knihy validní.
- Přidání **metody třídy** `from_string()`, která umožní vytvořit knihu z textového řetězce `"Název;Autor;Rok"`.

### **Nové zadání pro studenty**
- Implementovat statickou metodu `is_valid_year(year)`, která ověří, že zadaný rok je větší než 1440 (první tištěná kniha).
- Implementovat metodu třídy `from_string()`, která vytvoří knihu z textového řetězce.

---
## 3️⃣ Použití kompozice – Knihovna jako objekt
- Místo obyčejného seznamu `library` vytvořit **novou třídu `Library`**, která bude obsahovat seznam knih.
- Přidat metody pro:
  - `add_book(book)`: Přidání knihy do knihovny.
  - `remove_book(title)`: Odstranění knihy podle názvu.
  - `list_books()`: Výpis všech knih v knihovně.

### **Nové zadání pro studenty**
- Vytvořit třídu `Library` a do ní přesunout správu seznamu knih.
- Implementovat metody pro přidání, odstranění a vypsání knih.

---

## 4️⃣ Ukládání a načítání dat – Práce se soubory
- Implementace **ukládání knih do souboru** ve formátu CSV nebo JSON.
- Implementace **načítání knih při startu programu**.

### **Nové zadání pro studenty**
- Rozšířit `Library`, aby uměla ukládat knihy do souboru `books.csv` a načítat je zpět.
- Použít modul `csv` nebo `json` pro serializaci.

---

## 5️⃣ Interaktivní menu pro správu knihovny
- Přidání cyklu s uživatelskými příkazy (`input()`).
- Možnost vybrat, zda chce uživatel přidat, zobrazit, vypůjčit nebo vrátit knihu.

### **Nové zadání pro studenty**
- Přidat textové rozhraní, kde si uživatel vybere akci:
  - `[1] Zobrazit knihy`
  - `[2] Přidat knihu`
  - `[3] Vypůjčit knihu`
  - `[4] Vrátit knihu`
  - `[5] Uložit a ukončit program`

---

## Co by tato rozšíření přinesla?
✔ Upevnění **dědičnosti** a vytváření podtříd.  
✔ Seznámení se s **metodami třídy a statickými metodami**.  
✔ Pochopení **kompozice** (třída `Library` obsahující `Book`).  
✔ Základy **práce se soubory** – čtení a zápis knih do souboru.  
✔ Práce s **uživatelským vstupem a interaktivním programem**.  

"""
class Book:
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

        self.available = True

    def borrow(self):
        if self.available == True:
            self.available = False
            print(f"Kniha {self.title} je nyní vypůjčena.")
        if self.available == False:
            print(f"Kniha {self.title} už je bohužel vypůjčena.")

    def return_book(self):
        if self.available == False:
            self.available = True
            print(f"Kniha {self.title} byla vrácena.")
        if self.available == True:
            print(f"Kniha již byla dostupná.")


    def __str__(self):
        status = "Dostupná" if self.available else "Vypůjčená"
        return f"{self.title} - {self.author} ({self.year}) | Stav: {status}"
    
    @staticmethod
    def is_valid_year(year: int):
        if year <= 1440:
            return False
        else: 
            return True

    @classmethod
    def from_string(cls, usr_string: str):
        parsed_string = usr_string.split(";")
        title, author, year = parsed_string
        return cls(title, author, year)
    

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, media_type: str):
        super().__init__(self, title, author, year)
        self.media_type = media_type

    def __str__(self):
        status = "Dostupná" if self.available else "Vypůjčená"
        return f"{self.title} - {self.author} ({self.year}) | Formát: {self.media_type} | Stav: {status}"

class AudioBook(Book):
    def __init__(self, title: str, author: str, year: int, duration: str):
        super().__init__(self, title, author, year)
        self.duration = duration

    def __str__(self):
        status = "Dostupná" if self.available else "Vypůjčená"
        return f"{self.title} - {self.author} ({self.year}) | Délka trvání: {self.duration} | Stav: {status}"

 
library = [
    Book("1984", "George Orwell", 1949),
    Book("To Kill a Mockingbird", "Harper Lee", 1960),
    Book("Mistr a Markétka", "Michail Bulgakov", 1967),
    Book("Malý princ", "Antoine de Saint-Exupéry", 1943)
]
"""
## 3️⃣ Použití kompozice – Knihovna jako objekt
- Místo obyčejného seznamu `library` vytvořit **novou třídu `Library`**, která bude obsahovat seznam knih.
- Přidat metody pro:
  - `add_book(book)`: Přidání knihy do knihovny.
  - `remove_book(title)`: Odstranění knihy podle názvu.
  - `list_books()`: Výpis všech knih v knihovně.
"""
  
class Library:
    def __init__(self, books_list: list):
        self.books_list = books_list


    def add_book(book):
        