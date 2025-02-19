# Studijní materiál: Úvod do objektově orientovaného programování (OOP) v Pythonu  
Tento studijní materiál poskytuje teoretický základ pro pochopení konceptů, které budou studenti implementovat v praktické části. 😊

---

## 1. Co je objektově orientované programování (OOP)?  
Objektově orientované programování je způsob organizace kódu, kde program tvoří objekty, které mají své vlastnosti (atributy) a schopnosti (metody).  

### Hlavní principy OOP
- **Encapsulation (zapouzdření)** 
    – Chrání data uvnitř objektu, verifikace, práce s daty pomocí metod, setter, getter.
- **Inheritance (dědičnost)** 
    – Vytváření nových tříd na základě existujících tříd.  
- **Polymorphism (polymorfismus)** 
    – Možnost volání stejné metody různými způsoby.  
- **Abstraction (abstrakce)** 
    – Skrytí nepotřebných detailů, složitosti, práce jen s podstatnými vlastnostmi objektu - veřejné metody.  

---

## 2. Třídy a objekty  
Třída je šablona pro objekt. Objekt je konkrétní instance třídy.  

### Definice třídy a vytvoření objektu  
```python
class Auto:
    def __init__(self, znacka, model):
        self.znacka = znacka
        self.model = model

    def info(self):
        return f"Auto: {self.znacka} {self.model}"

# Vytvoření objektu
moje_auto = Auto("Škoda", "Octavia")
print(moje_auto.info())  # Výstup: Auto: Škoda Octavia
```

---

## 3. Dědičnost
Dědičnost umožňuje vytvořit novou třídu, která přebírá vlastnosti a metody jiné třídy.

```python
class ElektrickeAuto(Auto):
    def __init__(self, znacka, model, kapacita_baterie):
        super().__init__(znacka, model)
        self.kapacita_baterie = kapacita_baterie

    def dojezd(self):
        return f"{self.znacka} {self.model} má dojezd {self.kapacita_baterie * 5} km"

# Vytvoření objektu
tesla = ElektrickeAuto("Tesla", "Model 3", 75)
print(tesla.info())  # Výstup: Auto: Tesla Model 3
print(tesla.dojezd())  # Výstup: Tesla Model 3 má dojezd 375 km
```

---

## 4. Dunder (magické) metody
Dunder metody (double underscore methods) začínají a končí dvěma podtržítky a umožňují definovat speciální chování tříd.
**Magické metody se volají automaticky** při určitých akcích – nemusíme je explicitně volat v kódu.

**Některé klíčové dunder metody**

- **`__init__`** – Konstruktor, volá se při vytvoření objektu.
- **`__str__`** – Vrací čitelný textový popis objektu pro uživatele.
- **`__repr__`** – Vrací oficiální textovou reprezentaci objektu (pro vývojáře).
- **`__len__`** – Definuje, co se stane při volání `len(objekt)`.
- **`__eq__`, `__lt__`, `__gt__`** – Porovnávací operátory (`==`, `<`, `>`).
- **`__add__`, `__sub__`, `__mul__`** – Aritmetické operace (`+`, `-`, `*`).
- **`__getitem__`, `__setitem__`** – Přístup k prvkům pomocí `obj[index]`.
- **`__call__`** – Umožňuje volat instanci jako funkci (`obj()`).


```python
from datetime import datetime    # pouze kvůli LOGu, který použijeme níže

class Osoba:
    def __init__(self, jmeno, vek):  # inicializace, volání setterů, vytváření instancí
        self.jmeno = jmeno
        self.vek = vek

    def __str__(self):         # výstup pro uživatele, uživatelsky příjemný, smysluplný
        return f"{self.jmeno} má {self.vek} let"

    def __add__(self, other):  # součet dvou instancí
        return f"{self.jmeno} a {other.jmeno} jsou tým."

    def __repr__(self):        # Vrací oficiální reprezentaci objektu, užitečné pro ladění/debugování. Výstup do souboru.
        return f"LOG {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}: Osoba('{self.jmeno}', '{self.vek}')"

    def __call__(self):        # Umožňuje volat instanci jako funkci, která pak vrací následující.
        print(f"Osoba {self.jmeno} má aktuálně {self.vek} let. Zavoláním dojde ke změně.")
        self.vek +=1
        print(f"Zvýšíme věk o 1 rok na: {self.vek}")

os1 = Osoba("Jan", 25)
os2 = Osoba("Pavel", 30)

print(str(os1))         # Výstup: Jan, 25 let
print(os1 + os2)        # Výstup: Jan a Pavel jsou tým.
print(os2.__repr__())   # LOG 10.02.2025 14:41:04: Osoba('Pavel', '30')
os1()                   # Osoba Jan má aktuálně 25 let. Zavoláním dojde ke změně.        
                        # Zvýšíme věk o 1 rok na: 26
```

---

## 5. Dekorátory
Dekorátory umožňují upravit chování funkcí bez jejich změny. Dekorátory se aplikují odspodu nahoru.

```python
def zvys_vystup(func):
    """Dekorátor, který zvýší výstup funkce o 10."""
    def wrapper(*args, **kwargs):
        vystup = func(*args, **kwargs)
        return vystup + 10
    return wrapper

def vynasob_vystup(func):
    """Dekorátor, který výstup funkce vynásobí 2."""
    def wrapper(*args, **kwargs):
        vystup = func(*args, **kwargs)
        return vystup * 2
    return wrapper

@vynasob_vystup
@zvys_vystup
def sila_utoku():
    return 20

@zvys_vystup
@vynasob_vystup
def sila_utoku2():
    return 20

print(sila_utoku())   # Výstup: 60 (20 + 10) * 2
print(sila_utoku2())  # Výstup: 50 (20 * 2) + 10
```

---
---

# Pokročilejší koncepty OOP v Pythonu
V této lekci navážeme na základní principy OOP a rozšíříme je o další důležité koncepty, které nám pomohou lépe strukturovat a organizovat náš kód.

---

## 1. Viditelnost atributů (Public, Protected, Private)
Python nemá striktní modifikátory přístupu jako `private`, `protected`, `public`, ale konvence říká:
- **Public (`bez podtržítka`)** – Atributy/metody jsou volně dostupné.
- **Protected (`_jmeno`)** – Konvence, že atribut nemá být přístupný přímo. Getter, setter - viz dále.
- **Private (`__jmeno`)** – Atribut je "soukromý" a nelze k němu přímo přistupovat (name mangling).

```python
class Postava:
    def __init__(self, jmeno, sila):
        self.jmeno = jmeno  # Public - neupravujeme vstup, nečekáme problémy
        self._energie = 100  # Protected - dohoda, očekáváme nějaké ověření, možné problémy
        self.__tajná_schopnost = "Neviditelnost"  # Private, name mangling, nelze zvenčí

    # Veřejná, zobrazení informací, nic nemění, kumulace setterů (viz dále)
    def ukaz_info(self):
        return f"{self.jmeno}, Energie: {self._energie}, superschopnost: {self.__tajná_schopnost}"

    # Protected metoda, v podtřídách lze volat, zvenčí lze, ale nemělo by se.
    def _sniž_energii(self, hodnota):
        self._energie -= hodnota

    # Privátní metoda - nelze volat mimo tuto třídu, pouze uvnitř třídy.
    # vhodnější by byla ukázka, kde se v rámci metody provede moře změn a úprav
    def __aktivuj_tajnou_schopnost(self):
        self.__tajná_schopnost = "Super-neviditelnost nastavena!"

    # Veřejná metoda - pokud param true, zavolá se privátní/tajná metoda
    def výhra(self, výsledek: bool) -> None:
        if výsledek:
            self.__aktivuj_tajnou_schopnost()
        else:    # alternativní metoda, pokud je třeba změnit jen jednu vlastnost
            self.__tajná_schopnost = "nic"
            return print("To nevadí.")

p = Postava("Hrdina", 50)

# užití je v pořádku, proměnnou považujeme už z definice jako public
p.jmeno = "Zupaman"        # OK - Public
print(p.jmeno)             # OK - Public

# neskončí chybou, ALE není to vhodné ani doporučené
p._energie = 500           # změna parametru, který je veden jako protected
print(p._energie)          # ani toto není správně

# Chyba - atribut je privátní, skončí chybou: 
# print(p.__tajná_schopnost) # AttributeError: 'Postava' object has no attribute '__tajná_schopnost'
print (p.ukaz_info())    # Zupaman, Energie: 500, superschopnost: Neviditelnost
p.výhra(True)
print (p.ukaz_info())    # Zupaman, Energie: 500, superschopnost: Super-neviditelnost nastavena!
p.výhra(False)
print (p.ukaz_info())    # Zupaman, Energie: 500, superschopnost: nic
```

---

## 2. Property - getter, setter
V Pythonu se často používají vlastnosti (properties) k tomu, aby umožnily řízený přístup k atributům třídy. To znamená, že můžeme kontrolovat, co se děje při čtení nebo změně hodnoty atributu.

**Getter**
Metoda, která umožňuje přečíst hodnotu atributu.
Používá se dekorátor @property.

**Setter**
Metoda, která umožňuje změnit hodnotu atributu s určitými podmínkami.
Používá se dekorátor @nazev_metody.setter.

Díky těmto metodám můžeme: 
- ✅ Skrýt vnitřní implementaci atributu (například ho přejmenovat, aniž by to ovlivnilo uživatele třídy).
- ✅ Přidat kontrolu vstupních hodnot (např. zajistit, že věk nebude záporný).
- ✅ Zajistit, že atribut bude mít vždy platnou hodnotu.

```python
class Kruh:
    def __init__(self, polomer):
        self._polomer = polomer  # Volá setter, kontroluje vstup, pokud OK, nastaví _polomer

    @property   # getter - když chceme u instance polomer, zavolá se getter a vrací _polomer
    def polomer(self):
        return self._polomer    # lze libolně modifikovat, např. *1000 v milimetrech, nemění _polomer

    @polomer.setter  # setter - kontroluje vstup, posléze nastaví _polomer na NOVA_hodnota
    def polomer(self, NOVA_hodnota):
        if NOVA_hodnota <= 0:
            raise ValueError("Poloměr musí být větší než 0")
        self._polomer = NOVA_hodnota  # POZOR!!! ZDE MUSÍ BÝT _, jinak nastane nekonečná rekurze!

    @polomer.deleter  # deleter - kontrolované smazání vlastnosti, využívá se, pokud je potřeba více akcí
    def polomer(self):
        self._minuly_polomer = self._polomer    # uložena předchozí hodnota
        print("Poloměr vymazán.")     # oznam pro uživatele
        del self._polomer

    def __str__(self):
        return f"Str na instanci: volá polomer, ten vrací _polomer: {self.polomer}"
    

kr = Kruh(5)            # v init se zavolá setter, zkontroluje vstupní polomer, nastaví _polomer
print (kr)              # Str na instanci: volá polomer, ten vrací _polomer: 5

kr.polomer = 100        # voláme setter, ověří vstup, nastaví do _polomer číslo na vstupu
print (kr)              # Str na instanci: volá polomer, ten vrací _polomer: 100

kr._polomer = -50       # i přes vizuální varování jsme obešli vstupní kontrolu a nastavili _polomer - HNUS!
print (kr)              # Str na instanci: volá polomer, ten vrací _polomer: -50   ZÁPORNÝ POLOMĚR, SVĚTE DIV SE!

del kr.polomer
# print(kr.polomer)     # AttributeError: 'Kruh' object has no attribute '_polomer'.
```

---

## 3. Abstraktní třídy a metody
Pokud chceme vynutit, aby určité třídy měly implementované metody, můžeme použít **abstraktní třídy** (`ABC` - Abstract Base Class).

```python
from abc import ABC, abstractmethod

class Bojovník(ABC):  # Abstraktní třída
    @abstractmethod
    def útok(self):
        """Tuto metodu MUSÍ dědit všechny podtřídy"""
        pass

class Rytíř(Bojovník):
    def útok(self):
        return "Rytíř útočí mečem!"

class Mág(Bojovník):
    def útok(self):
        return "Mág sesílá kouzlo!"

r = Rytíř()
m = Mág()
print(r.útok())  # Výstup: Rytíř útočí mečem!
print(m.útok())  # Výstup: Mág sesílá kouzlo!
```

---

## 4. Statické metody a metody třídy
Python podporuje **statické metody** (bez `self`) a **metody třídy** (s `cls`).

```python
class Hra:
    počet_hráčů = 0

    def __init__(self, jméno):
        self.jméno = jméno
        Hra.počet_hráčů += 1

    @classmethod
    def ukaz_pocet_hracu(cls):
        return f"Počet hráčů: {cls.počet_hráčů}"

    @classmethod
    def ukaz_pocet_hracu2(cls):
        return f"Počet hráčů: {Hra.počet_hráčů}"

    @classmethod
    def ukaz_pocet_hracu3(Hra):
        return f"Počet hráčů: {Hra.počet_hráčů}"

    @staticmethod
    def pravidla_hry():
        return "Pravidla hry: Nikdy neútoč na spojence."

h1 = Hra("Bojovník")
h2 = Hra("Kouzelník")

print(Hra.ukaz_pocet_hracu())   # Výstup: Počet hráčů: 2
print(Hra.ukaz_pocet_hracu2())  # Výstup: Počet hráčů: 2
print(Hra.ukaz_pocet_hracu3())  # Výstup: Počet hráčů: 2
print(Hra.pravidla_hry())  # Výstup: Pravidla hry: Nikdy neútoč na spojence.
```

### **Rozdíl mezi statickými metodami a metodami třídy**
V Pythonu existují dva typy metod, které nepracují s instancí objektu (`self`), ale fungují na úrovni třídy:

-   **Statické metody** (`@staticmethod`) - Nemají přístup k instanci (`self`) ani ke třídě (`cls`). Jsou jako běžné funkce, které logicky souvisejí se třídou.
-   **Metody třídy** (`@classmethod`) - Přijímají jako první argument `cls`, což umožňuje pracovat přímo se třídou a jejími atributy.


### 1. **Statické metody (`@staticmethod`)**
Statická metoda nevyužívá žádný atribut ani metodu instance nebo třídy. Používá se, když chceme vytvořit pomocnou funkci v rámci třídy, ale nemáme potřebu přistupovat k jejím datům.

**Příklad 1 -- Statická metoda jako užitečná funkce**

```python
class Matematika:
    @staticmethod
    def scitej(a, b):
        return a + b

    @staticmethod
    def celsius_2_fahrenheit(celsius):
        return (celsius * 9/5) + 32

# Použití statické metody bez vytváření instance
print(Matematika.scitej(10, 5))  # Výstup: 15
fahrenheit = Matematika.celsius_2_fahrenheit(0)   # 32
```

✅ **Kdy použít statickou metodu?**

-   Když funkce logicky patří do třídy, ale nepotřebuje instanční ani třídní proměnné.
-   Například matematické operace (`scitej()`, `odecti()`), validace vstupů nebo pomocné metody.

### 2. **Metody třídy (`@classmethod`)**
Metody třídy přijímají jako první argument `cls`, což umožňuje přístup ke **sdíleným atributům třídy**, ale ne k atributům konkrétní instance.

**Příklad 2 -- Počítání instancí třídy pomocí metody třídy**

```python
class Hra:
    pocet_hracu = 0  # Sdílená proměnná pro všechny instance

    def __init__(self, jmeno):
        self.jmeno = jmeno
        Hra.pocet_hracu += 1

    @classmethod
    def ukaz_pocet_hracu(cls):
        return f"Aktuální počet hráčů: {cls.pocet_hracu}"

    @classmethod
    def vytvor_hrace_z_fullname(cls, full_name):
        name = full_name.split()[0]
        return cls(name)

# Vytvoření několika hráčů
hrac1 = Hra("Bojovník")
hrac2 = Hra("Kouzelník")
hrac3 = Hra.vytvor_hrace_z_fullname("Ježibaba ze Vsetína")

# Metodu voláme přímo na třídě, nemusíme vytvářet instanci
print(Hra.ukaz_pocet_hracu())  # Výstup: Aktuální počet hráčů: 3
```

✅ **Kdy použít metodu třídy?**

-   Když potřebujeme pracovat s atributy třídy (`cls`), například počítat instance.
-   Když chceme implementovat **alternativní konstruktory** -- metody, které vytvoří instanci jiným způsobem než `__init__()`.

### **Shrnutí rozdílů**
| Typ metody | Přístup k `self` | Přístup k `cls` | Použití |
| --- | --- | --- | --- |
| **Statická metoda (`@staticmethod`)** | ❌ Ne | ❌ Ne | Pomocné metody bez interakce s třídou nebo instancí |
| **Metoda třídy (`@classmethod`)** | ❌ Ne | ✅ Ano | Práce s atributy třídy, alternativní konstruktory |

Pokud potřebujete upravit globální stav třídy, použijte **metodu třídy**. Pokud jen chcete mít užitečnou funkci uvnitř třídy, která nepotřebuje pracovat s daty třídy, použijte **statickou metodu**.

---

## 5. Alternativní konstruktory

Jedním z častých použití metod třídy je definování **alternativních konstruktorů**, které umožní vytvořit objekt jiným způsobem než přes `__init__()`.

```python
class Postava:
    def __init__(self, jmeno, level):
        self.jmeno = jmeno
        self.level = level

    @classmethod
    def z_textu(cls, text):
        """Alternativní konstruktor, který vytvoří instanci z řetězce."""
        jmeno, level = text.split("-")
        return cls(jmeno, int(level))

# Vytvoření instance pomocí běžného konstruktoru
hrdina1 = Postava("Aragorn", 10)

# Vytvoření instance pomocí alternativního konstruktoru
hrdina2 = Postava.z_textu("Legolas-12")

print(hrdina1.jmeno, hrdina1.level)  # Výstup: Aragorn 10
print(hrdina2.jmeno, hrdina2.level)  # Výstup: Legolas 12
```

✅ **Kdy použít alternativní konstruktory?**

-   Když chceme vytvářet objekty z jiných datových formátů (např. text, JSON, CSV).
-   Když potřebujeme různé způsoby inicializace objektů.

---

## 6. Kompozice vs. Dědičnost

V objektově orientovaném programování (OOP) existují dva hlavní způsoby, jak vytvořit vztah mezi třídami:

-   **Dědičnost** (`is-a` vztah, „je to"): Třída dědí vlastnosti a metody od nadřazené třídy. (`Mág je Character`)
-   **Kompozice** (`has-a` vztah, „má to"): Objekt jedné třídy obsahuje instanci jiné třídy jako svůj atribut. (`Mág má Inventář`)

Dědičnost je silné spojení, ale kompozice dává více flexibility.
Obě techniky mají své výhody a nevýhody a měly by být používány podle kontextu a potřeb návrhu.



### 1\. Dědičnost („je to" vztah)

Dědičnost umožňuje vytvořit novou třídu (`potomek`), která přebírá atributy a metody z jiné třídy (`rodič`).\
To umožňuje opětovné využití kódu a rozšíření funkcionality bez nutnosti psát stejný kód znovu.

**Příklad - Dědičnost mezi třídami**

```python
class Postava:
    def __init__(self, jmeno, level):
        self.jmeno = jmeno
        self.level = level

    def info(self):
        return f"{self.jmeno}, Level: {self.level}"

class Bojovník(Postava):
    def __init__(self, jmeno, level, síla):
        super().__init__(jmeno, level)  # Volání konstruktoru rodičovské třídy
        self.síla = síla

    def utok(self):
        return f"{self.jmeno} útočí se silou {self.síla}!"

# Vytvoření instancí
hrdina = Bojovník("Aragorn", 10, 50)
print(hrdina.info())   # Výstup: Aragorn, Level: 10
print(hrdina.utok())   # Výstup: Aragorn útočí se silou 50!
```

✅ **Kdy použít dědičnost?**

-   Když **potomek** je specializovaná verze **rodiče** („Bojovník je Postava").
-   Když chceme **přidat nové vlastnosti nebo chování**, aniž bychom měnili původní třídu.
-   Když chceme využít **polymorfismus** (schopnost volat stejnou metodu různými třídami).

❌ **Nevýhody dědičnosti**

-   Pevná struktura -- podtřídy jsou silně závislé na rodičovské třídě.
-   Jakákoli změna v rodičovské třídě může způsobit problémy v podřízených třídách.


### 2\. Kompozice („má to" vztah)

Kompozice znamená, že objekt obsahuje jiný objekt jako **atribut** místo toho, aby po něm dědil.\
Tato technika podporuje větší flexibilitu a lepší oddělení odpovědností.

**Příklad - Postava má inventář (kompozice)**

```python

class Inventář:
    def __init__(self):
        self.předměty = []

    def přidej_předmět(self, předmět):
        self.předměty.append(předmět)

    def zobraz(self):
        return f"Inventář: {', '.join(self.předměty)}" if self.předměty else "Inventář je prázdný."

class Postava:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.inventář = Inventář()  # Kompozice - postava má inventář

    def info(self):
        return f"{self.jmeno} - {self.inventář.zobraz()}"

# Vytvoření instance
hrdina = Postava("Aragorn")
hrdina.inventář.přidej_předmět("Meč")
hrdina.inventář.přidej_předmět("Brnění")

print(hrdina.info())  # Výstup: Aragorn - Inventář: Meč, Brnění
```

✅ **Kdy použít kompozici?**

-   Když chceme **znovu použít funkcionalitu**, ale nechceme pevné vazby mezi třídami.
-   Když objekt **„má něco"** (např. „Postava má inventář" místo „Postava je inventář").
-   Když chceme **zlepšit flexibilitu kódu** -- můžeme snadno měnit nebo nahrazovat části systému.

❌ **Nevýhody kompozice**

-   Může vést k větší složitosti při implementaci.
-   Může vyžadovat více metod pro propojení objektů.


### 3\. Porovnání Dědičnosti a Kompozice

| Kritérium | Dědičnost (`is-a`) | Kompozice (`has-a`) |
| --- | --- | --- |
| **Vztah** | Potomek je specializovaná verze rodiče („Bojovník je Postava"). | Objekt obsahuje jiný objekt jako atribut („Postava má inventář"). |
| **Použití** | Když chceme rozšířit existující třídu. | Když chceme kombinovat různé třídy flexibilněji. |
| **Závislost** | Podtřída závisí na rodičovské třídě. | Objekty jsou volně propojené a nezávislé. |
| **Flexibilita** | Méně flexibilní -- pevně daná struktura. | Vyšší flexibilita -- moduly lze snadno nahradit. |
| **Opětovné použití** | Sdílené vlastnosti a metody rodičovské třídy. | Lze kombinovat různé objekty podle potřeby. |



### 4\. Kombinace dědičnosti a kompozice

V praxi se často kombinuje **dědičnost** a **kompozice**, aby se využily výhody obou přístupů.

**Příklad -- Postava dědí z Bojovníka a používá kompozici pro inventář**

```python
class Inventář:
    def __init__(self):
        self.předměty = []

    def přidej_předmět(self, předmět):
        self.předměty.append(předmět)

    def zobraz(self):
        return f"Inventář: {', '.join(self.předměty)}" if self.předměty else "Inventář je prázdný."

class Postava:
    def __init__(self, jmeno, level):
        self.jmeno = jmeno
        self.level = level
        self.inventář = Inventář()  # Kompozice – Postava má Inventář

    def info(self):
        return f"{self.jmeno}, Level {self.level} - {self.inventář.zobraz()}"

class Bojovník(Postava):
    def __init__(self, jmeno, level, síla):
        super().__init__(jmeno, level)  # Dědičnost – Bojovník je Postava
        self.síla = síla

    def utok(self):
        return f"{self.jmeno} útočí se silou {self.síla}!"

# Vytvoření instance bojovníka
hrdina = Bojovník("Aragorn", 10, 50)
hrdina.inventář.přidej_předmět("Meč")

print(hrdina.info())   # Výstup: Aragorn, Level 10 - Inventář: Meč
print(hrdina.utok())   # Výstup: Aragorn útočí se silou 50!
```

**Shrnutí**

✅ **Použijte dědičnost, pokud:**

-   Váš objekt je speciální verzí jiného objektu (`Bojovník je Postava`).
-   Chcete sdílet a rozšířit metody rodičovské třídy.

✅ **Použijte kompozici, pokud:**

-   Váš objekt obsahuje jiný objekt (`Postava má Inventář`).
-   Chcete vytvořit **volnější propojení mezi třídami** a zvýšit flexibilitu systému.

💡 Nejlepší přístup je **kombinovat oba principy podle potřeby**! 😊

---

## 7. Mixiny

Mixiny jsou lehké třídy, které přidávají funkcionalitu jiným třídám, ale samy o sobě nejsou určeny k instanciaci. Umožňují sdílení kódu mezi různými třídami bez použití dědičnosti. Používají se v případech, kdy chceme přidat specifickou funkcionalitu více různým třídám, aniž bychom je museli všechny dědit od společné základní třídy.

### Použití mixinů:

Logování – Přidání logování do různých tříd bez duplikace kódu.
Autorizace – Kontrola oprávnění v různých třídách aplikace.
Sledování změn – Automatická registrace změn atributů objektů.

```python
class LogMixin:
    def log(self, zpráva):
        print(f"[LOG] {zpráva}")

class Bojovník(LogMixin):
    def __init__(self, jméno):
        self.jméno = jméno

    def útok(self):
        self.log(f"{self.jméno} útočí!")
        return "Způsobeno poškození!"

class Kouzelník(LogMixin):
    def __init__(self, jméno):
        self.jméno = jméno

    def kouzlo(self):
        self.log(f"{self.jméno} sesílá kouzlo!")
        return "Sesláno kouzlo!"

bojovník = Bojovník("Ragnar")
kouzelník = Kouzelník("Merlin")
print(bojovník.útok())  
print(kouzelník.kouzlo())

# Výstup:
# [LOG] Ragnar útočí!
# Způsobeno poškození!
# [LOG] Merlin sesílá kouzlo!
# Sesláno kouzlo!
```

---
---

## Reálné použití dekorátorů v praxi – Logování API požadavků

Dekorátory se často využívají v reálných aplikacích například pro:
✅ **Logování funkcí** (zaznamenání volání a návratových hodnot).  
✅ **Autorizaci uživatelů** (kontrola přístupu před spuštěním funkce).  
✅ **Měření výkonu** (zaznamenání doby běhu funkce).  
✅ **Úpravu návratových hodnot** (např. automatická serializace výstupu do JSON).  

Vytvoříme dekorátor `log_request`, který automaticky zaznamená volání API funkce 
do logovacího souboru a vypíše informace do konzole.

**Jak dekorátor funguje?**
1️⃣ Když zavoláme funkci get_user_info(101), dekorátor log_request:
* Zaznamená aktuální čas.
* Zaloguje informace o volání funkce (název funkce, argumenty, čas).
* Vypíše informace do konzole.
* Zavolá původní funkci a vrátí její výstup.

2️⃣ Totéž se děje pro process_payment(101, 250).

```python
import logging
from datetime import datetime

# Nastavení logování
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Dekorátor pro logování API požadavků
def log_request(func):
    def wrapper(*args, **kwargs):
        # Získání aktuálního času
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Zaznamenání volání funkce do logu
        logging.info(f"API REQUEST - Funkce: {func.__name__}, Argumenty: {args}, {kwargs}, Čas: {timestamp}")

        # Výpis do konzole pro rychlou kontrolu
        print(f"[{timestamp}] Volání API: {func.__name__} s argumenty {args} {kwargs}")
        
        # Spuštění původní funkce a návrat výsledku
        return func(*args, **kwargs)
    return wrapper

# Simulace API funkcí s dekorátorem
@log_request
def get_user_info(user_id):
    """Simuluje získání informací o uživateli podle ID."""
    return {"id": user_id, "name": "John Doe", "email": "john.doe@example.com"}

@log_request
def process_payment(user_id, amount):
    """Simuluje zpracování platby uživatele."""
    return {"user_id": user_id, "amount": amount, "status": "Processed"}

# Test API funkcí s logováním
user_data = get_user_info(101)
print("Výstup API:", user_data)

payment_result = process_payment(101, 250)
print("Výstup API:", payment_result)
```

### Konzolový výstup
```python
[2024-02-05 16:30:10] Volání API: get_user_info s argumenty (101,) {}
Výstup API: {'id': 101, 'name': 'John Doe', 'email': 'john.doe@example.com'}

[2024-02-05 16:30:15] Volání API: process_payment s argumenty (101, 250) {}
Výstup API: {'user_id': 101, 'amount': 250, 'status': 'Processed'}
```

### Obsah logovacího souboru api_requests.log
```python
2024-02-05 16:30:10 - INFO - API REQUEST - Funkce: get_user_info, Argumenty: (101,), {}, Čas: 2024-02-05 16:30:10
2024-02-05 16:30:15 - INFO - API REQUEST - Funkce: process_payment, Argumenty: (101, 250), {}, Čas: 2024-02
```

---

## Reálné použití dekorátorů v praxi – Autentizace API požadavků

Dekorátory se často používají ke **kontrole oprávnění uživatele** před vykonáním funkce.  
V tomto příkladu vytvoříme dekorátor `authenticate`, který ověří, zda má uživatel platný token a může danou funkcí provádět.

**Reálné využití**:  
- Ověření přístupu k **chráněným API endpointům**.  
- **Role-based access control (RBAC)** – omezení akcí podle role uživatele.  
- **Prevence neoprávněného přístupu** k citlivým datům.  

### Implementace autentizačního dekorátoru

Vytvoříme seznam **povolených tokenů** a dekorátor, který zkontroluje, zda volající uživatel má platný token a dostatečnou roli.

* 1️⃣ Ověříme token uživatele podle databáze USERS.
* 2️⃣ Pokud je vyžadována role, ověříme, zda uživatel odpovídá požadované roli.
* 3️⃣ Pokud uživatel nemá dostatečná oprávnění, dekorátor přístup odmítne.

```python
import functools

# Simulovaná databáze uživatelů s rolemi a tokeny
USERS = {
    "user123": {"token": "token_abc", "role": "user"},
    "admin456": {"token": "token_xyz", "role": "admin"}
}

def authenticate(role_required=None):
    """Dekorátor pro ověření uživatele a jeho role.
    
    Args:
        role_required (str): Očekávaná role uživatele ('user' nebo 'admin')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_id, token, *args, **kwargs):
            # Ověření, zda uživatel existuje a token odpovídá
            user = USERS.get(user_id)
            if not user or user["token"] != token:
                print(f"❌ Přístup odepřen! Neplatný token pro uživatele '{user_id}'.")
                return {"error": "Unauthorized access"}

            # Ověření role, pokud je vyžadována
            if role_required and user["role"] != role_required:
                print(f"❌ Přístup odepřen! Uživatel '{user_id}' nemá oprávnění '{role_required}'.")
                return {"error": "Insufficient privileges"}

            print(f"✅ Uživatel '{user_id}' (Role: {user['role']}) byl úspěšně autentizován.")
            return func(user_id, *args, **kwargs)  # Zavolání původní funkce
        return wrapper
    return decorator

# API funkce s rozlišením rolí
@authenticate(role_required="user")
def get_user_info(user_id):
    """Simuluje získání informací o uživateli podle ID."""
    return {"id": user_id, "name": "John Doe", "email": "john.doe@example.com"}

@authenticate(role_required="admin")
def process_payment(user_id, amount):
    """Simuluje zpracování platby uživatele (pouze admin)."""
    return {"user_id": user_id, "amount": amount, "status": "Processed"}

# Test autentizace s rozlišením rolí
print(get_user_info("user123", "token_abc"))            # ✅ Uživatelský přístup OK
print(process_payment("user123", "token_abc", 500))     # ❌ Uživateli chybí oprávnění
print(get_user_info("admin456", "token_xyz"))           # ✅ Admin si může zobrazit info
print(process_payment("admin456", "token_xyz", 1000))   # ✅ Admin může provádět platby
print(get_user_info("hacker999", "token_hack"))         # ❌ Neautorizovaný přístup
```

### Výstupy programu
```python
✅ Uživatel 'user123' (Role: user) byl úspěšně autentizován.
{'id': 'user123', 'name': 'John Doe', 'email': 'john.doe@example.com'}

❌ Přístup odepřen! Uživatel 'user123' nemá oprávnění 'admin'.
{'error': 'Insufficient privileges'}

✅ Uživatel 'admin456' (Role: admin) byl úspěšně autentizován.
{'id': 'admin456', 'name': 'John Doe', 'email': 'john.doe@example.com'}

✅ Uživatel 'admin456' (Role: admin) byl úspěšně autentizován.
{'user_id': 'admin456', 'amount': 1000, 'status': 'Processed'}

❌ Přístup odepřen! Neplatný token pro uživatele 'hacker999'.
{'error': 'Unauthorized access'}
```
### Shrnutí

✅ Autentizační dekorátor přidává vrstvu bezpečnosti k API funkcím.
✅ Snadné rozšíření – stačí dekorátor přidat nad další funkce.
✅ Ochrana citlivých operací jako získání uživatelských dat nebo platby.
✅ Jednoduchá správa oprávnění – stačí aktualizovat VALID_TOKENS.
✅ Dekorátor authenticate(role_required="admin") omezuje přístup k funkcím podle role.
✅ Uživatelé s rolí "user" mohou zobrazit své údaje.
✅ Uživatelé s rolí "admin" mohou zpracovávat platby.
✅ Neoprávněným uživatelům je přístup odepřen.

---

## Vícenásobná dědičnost + diamantový problém

**Lze v Pythonu dědit od dvou rodičovských tříd?**

Ano! Python podporuje **vícenásobnou dědičnost**, což znamená, že třída může dědit od **více rodičů**.  

To se často používá v kombinaci s **mixiny**, které přidávají dodatečné funkcionality bez složité dědičnosti.

**Příklad**  
- Postava může být **Bojovník** (silné útoky) a zároveň **Kouzelník** (magické schopnosti).  
- Chceme kombinovat vlastnosti obou tříd a zároveň **použít mixin** pro logování (viz předchozí kapitoly)  

```python
# Vícenásobná dědičnost v OOP – Bojovník + Kouzelník

class LogMixin:
    """Mixin třída pro logování akcí."""
    def log(self, zpráva):
        print(f"[LOG] {zpráva}")

class Bojovník:
    """Třída reprezentující bojovníka."""
    def __init__(self, jméno):
        self.jméno = jméno

    def útok(self):
        return f"{self.jméno} provádí silný úder mečem!"


class Kouzelník:
    """Třída reprezentující kouzelníka."""
    def __init__(self, jméno):
        self.jméno = jméno

    def kouzlo(self):
        return f"{self.jméno} sesílá mocné kouzlo!"


class BojovýMág(Bojovník, Kouzelník, LogMixin):
    """Třída kombinující vlastnosti Bojovníka a Kouzelníka."""
    def __init__(self, jméno):
        # MRO (Method Resolution Order) – řád prioritního volání metod
        # zajistí správné volání rodičů, vyhneme se problému "diamant" - viz níže
        super().__init__(jméno)

    def kombinovaný_útok(self):
        """Provádí kombinaci fyzického útoku a magického kouzla."""
        self.log(f"{self.jméno} provádí kombinovaný útok!")
        return f"{self.útok()} A zároveň {self.kouzlo()}"


# Vytvoření instancí
bojovník = Bojovník("Válek")
kouzelník = Kouzelník("Hrčiřík")
bojový_mág = BojovýMág("Metelka")

# Test jednotlivých postav
print(bojovník.útok())           # Válek provádí silný úder mečem!
print(kouzelník.kouzlo())        # Hrčiřík sesílá mocné kouzlo!

# Test kombinovaného útoku BojovéhoMága
print(bojový_mág.kombinovaný_útok())  
    # [LOG] Metelka provádí kombinovaný útok!
    # Metelka provádí silný úder mečem! A zároveň Metelka sesílá mocné kouzlo!
```
✅ Vícenásobná dědičnost funguje správně díky super().
✅ Python automaticky určuje správné pořadí volání metod pomocí MRO.

**Další příklad včetně diamant řešení pomocí MRO**

```python
class Employee:
    """Základní třída pro zaměstnance."""
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        print(f"Zaměstnanec {self.name} vytvořen s platem {self.salary} Kč.")

class Manager(Employee):
    """Třída pro manažera – přidává řízení týmu."""
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)  # Zavolá Employee.__init__()
        self.team_size = team_size
        print(f"{self.name} je manažer s týmem o velikosti {self.team_size}.")

class Technician(Employee):
    """Třída pro technika – přidává schopnost opravovat stroje."""
    def __init__(self, name, salary, skill_level):
        super().__init__(name, salary)  # Zavolá Employee.__init__()
        self.skill_level = skill_level
        print(f"{self.name} je technik s úrovní dovedností {self.skill_level}.")

class LeadTechnician(Manager, Technician):
    """Vedoucí technik kombinuje manažerské a technické schopnosti."""
    def __init__(self, name, salary, team_size, skill_level):
        super().__init__(name, salary, team_size)  # MRO zajistí správné volání rodičů
        self.skill_level = skill_level
        print(f"{self.name} je vedoucí technik s týmem {self.team_size} a dovedností {self.skill_level}.")

# Vytvoření instance vedoucího technika
leader = LeadTechnician("Válek", 60000, 5, "expert")

# Výpis pořadí dědičnosti
print("\nPořadí dědičnosti:", LeadTechnician.mro())

# Zaměstnanec Válek vytvořen s platem 60000 Kč.
# Válek je manažer s týmem o velikosti 5.
# Válek je vedoucí technik s týmem 5 a dovedností expert.

# Pořadí dědičnosti: 
# [<class '__main__.LeadTechnician'>, 
# <class '__main__.Manager'>, 
# <class '__main__.Technician'>, 
# <class '__main__.Employee'>, 
# <class 'object'>]
```
✅ Použili jsme super() místo přímého volání rodičovských tříd.
✅ MRO (Method Resolution Order) zajistilo, že Employee se inicializuje jen jednou.
✅ Třída LeadTechnician správně kombinuje manažerské i technické schopnosti.
✅ Základní třída Employee se zavolá pouze jednou.
✅ Můžeme snadno kombinovat role ve firmě – přidání dalších tříd bude jednoduché.

---

## Metatřídy a dynamická tvorba tříd + logování

### 1️⃣ Co je metatřída?

V Pythonu jsou **všechny třídy objekty** a třídy samotné jsou instancemi jiné třídy.  
Tato speciální třída se nazývá **metatřída**.  

```python
# Všechny třídy jsou ve skutečnosti instancemi třídy "type"
print(type(int))      # <class 'type'>
print(type(str))      # <class 'type'>
print(type(object))   # <class 'type'>
```

✅ Metatřída type říká, jak se mají třídy vytvářet a chovat.

### 2️⃣ Jak vytvořit vlastní metatřídu?
Metatřídy se definují jako podtřídy type, ve kterých můžeme přizpůsobit, jak se třídy vytvářejí.

```python
class MetaLogger(type):
    """Metatřída, která při každém vytvoření třídy vypíše zprávu."""
    def __new__(cls, name, bases, dct):
        print(f"🔧 Vytváří se třída: {name}")
        return super().__new__(cls, name, bases, dct)

# Použití metatřídy
class Auto(metaclass=MetaLogger):
    def __init__(self, model):
        self.model = model

# Vytvoření instance
a = Auto("Tesla")
```

📌 Výstup programu:

    🔧 Vytváří se třída: Auto

✅ __new__() umožňuje ovlivnit proces tvorby třídy ještě před jejím vytvořením.

### 3️⃣ Praktický příklad: Automatické logování metod
Metatřída může přidat logovací funkci ke každé metodě nové třídy.

```python
class MetaLogger(type):
    """Metatřída, která automaticky přidá logování volání metod."""
    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if callable(value):  # Pokud je atribut metoda, obalíme ji logováním
                def logged_method(method):
                    def wrapper(*args, **kwargs):
                        print(f"📢 Volání metody: {method.__name__}")
                        return method(*args, **kwargs)
                    return wrapper
                dct[attr] = logged_method(value)
        return super().__new__(cls, name, bases, dct)

# Třída používající metatřídu
class Auto(metaclass=MetaLogger):
    def start(self):
        print("🚗 Auto nastartovalo!")

    def stop(self):
        print("🚗 Auto zastavilo!")

# Test metatřídy
a = Auto()
a.start()
a.stop()
```

📌 Výstup programu:

    📢 Volání metody: start
    🚗 Auto nastartovalo!
    📢 Volání metody: stop
    🚗 Auto zastavilo!

- ✅ Každá metoda je automaticky obalena logováním, aniž bychom museli měnit kód třídy.
- ✅ To umožňuje snadno přidávat funkcionality do všech tříd, které metatřídu používají.

### 4️⃣ Shrnutí

- ✔ Metatřídy ovládají proces tvorby tříd a mohou automaticky upravovat jejich chování.
- ✔ __new__() v metatřídách umožňuje upravit definici třídy před jejím vytvořením.
- ✔ Použití metatříd je užitečné pro automatizaci, logování a vylepšení OOP v Pythonu.
- více viz lekce - **OOP_metaClass**

---
## Protected property - další možnost ošetření
Další zajímavá možnost, jak zapouzdřit proměnné uvnitř instance před dunder __getattr__ a __setattr__.

```python
class ProtectedAttributes:
    def __init__(self):
        self._protected = "Pomyslně chráněno."

    def __getattr__(self, name):
        if name == "secret":   # lze vymyslet podmínku, kdy se může zobrazit
            raise AttributeError("K tomuto atributu nemáte přístup.")
        return self.__dict__.get(name, f"{name} není nadefinováno.")

    def __setattr__(self, name, value):
        if name == "secret":   # lze vymyslet podmínku, kdy lze modifikovat
            raise AttributeError("Tento atribut nemůžete měnit.")
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name == "secret":
            raise AttributeError("Cannot delete secret")
        del self.__dict__[name]

obj = ProtectedAttributes()
print(obj._protected)  # Lze přistupovat, nemělo by se.
print(obj.missing)     # Nic takového není definováno, ošetřeno: "missing není nadefinováno."
# obj.secret            # AttributeError: K tomuto atributu nemáte přístup.
# obj.secret = "New"    # AttributeError: Tento atribut nemůžete měnit.


```

