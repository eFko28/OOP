# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram

# Logování běhu programu do souboru pomocí metatřídy - základní varianta
"""_summary_
# Logování běhu programu pomocí metatřídy v Pythonu

Tento skript demonstruje použití metatřídy v Pythonu pro logování běhu programu. 
Metatřídy jsou pokročilým konceptem v Pythonu, který umožňuje modifikovat chování 
tříd při jejich vytváření. V tomto příkladu využíváme metatřídu k automatickému 
logování volání metod tříd `Auto` a `Letadlo`.

## Struktura skriptu

1. **Importy a nastavení cesty k logovacímu souboru**:
    - Importujeme potřebné moduly `os` a `datetime`.
    - Nastavíme relativní cestu k logovacímu souboru a zajistíme, že adresář pro logy existuje.

2. **Globální přepínač logování**:
    - Definujeme globální proměnnou `LOG_ENABLED`, která umožňuje zapnout nebo vypnout logování.

3. **Funkce pro logování**:
    - `log_message(message)`: Zapíše zprávu do logovacího souboru, pokud je logování povoleno.
    - `enable_logging()`: Zapne logování a zapíše tuto akci do logu.
    - `disable_logging()`: Vypne logování a zapíše tuto akci do logu.

4. **Zaznamenání startu skriptu**:
    - Při spuštění skriptu zaznamenáme tuto událost do logu.

5. **Definice tříd `Auto` a `Letadlo`**:
    - Každá třída má metody pro základní operace (např. `start` a `stop` pro `Auto`, `vzlet` a `pristani` pro `Letadlo`).
    - V konstruktoru a metodách těchto tříd voláme funkci `log_message`, která zaznamenává vytvoření instance a volání metod.

6. **Test logování**:
    - Zapneme logování.
    - Vytvoříme instance tříd `Auto` a `Letadlo` a voláme jejich metody, což se zaznamená do logu.
    - Vypneme logování a ověříme, že další volání metod již nejsou logována.

7. **Zaznamenání ukončení skriptu**:
    - Při ukončení skriptu zaznamenáme tuto událost do logu.

## Použití metatřídy
V tomto příkladu není metatřída explicitně definována, ale koncept metatřídy by mohl 
být použit k automatizaci logování metod tříd. Metatřída by mohla přepsat metody tříd 
tak, aby automaticky volaly `log_message` při každém volání metody. Tento skript slouží 
jako základní příklad, který lze dále rozšířit o metatřídu pro plně automatizované logování.

Tento skript je vhodný pro studenty, kteří se chtějí naučit základy logování v Pythonu 
a pochopit, jak by mohly být metatřídy využity k automatizaci opakujících se úkolů, 
jako je logování.
"""

import os
from datetime import datetime

# Nastavení relativní cesty k logu
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")  # Relativní cesta k adresáři /log
LOG_FILE = os.path.join(LOG_DIR, "method_calls_1.log")  # Plná cesta k logovacímu souboru

# Pokud složka log neexistuje, vytvoříme ji
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Globální přepínač logování
LOG_ENABLED = True  # Lze zapnout/vypnout voláním enable_logging() / disable_logging()

def log_message(message):
    """Zapíše zprávu do logovacího souboru, pokud je logování povoleno."""
    if LOG_ENABLED:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def enable_logging():
    """Zapne logování."""
    global LOG_ENABLED
    LOG_ENABLED = True
    print("✅ Logování povoleno.")
    log_message("✅ Logování povoleno.")

def disable_logging():
    """Vypne logování."""
    global LOG_ENABLED
    LOG_ENABLED = False
    print("❌ Logování zakázáno.")
    log_message("❌ Logování zakázáno.")


class MetaLogger(type):
    """Metatřída, která automaticky přidává logování ke všem metodám třídy."""

    def __new__(cls, name, bases, dct):
        """Obalí všechny metody logovací funkcí."""
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith("__"):  # Pouze metody, ne dunder
                dct[attr_name] = cls._log_method(attr_name, attr_value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def _log_method(method_name, method):
        """Obalí metodu tak, aby se logovala při každém volání."""
        def wrapper(*args, **kwargs):
            if LOG_ENABLED:
                log_message(f"METACLASS: {method_name}, Argumenty: {args}, {kwargs}")
            return method(*args, **kwargs)
        return wrapper


class Auto(metaclass=MetaLogger):
    """Třída reprezentující auto."""
    def __init__(self, model):
        self.model = model
        log_message(f"📢 Vytvořena instance Auto: {self.model}")

    def start(self):
        print(f"🚗 {self.model} nastartovalo!")
        log_message(f"📢 {self.model} nastartovalo!")

    def stop(self):
        print(f"🚗 {self.model} zastavilo!")
        log_message(f"📢 {self.model} zastavilo!")


class Letadlo(metaclass=MetaLogger):
    """Třída reprezentující letadlo."""
    def __init__(self, name):
        self.name = name
        log_message(f"📢 Vytvořena instance Letadlo: {self.name}")

    def vzlet(self):
        print(f"✈️ {self.name} vzlétlo!")
        log_message(f"📢 {self.name} vzlétlo!")

    def pristani(self):
        print(f"✈️ {self.name} přistálo!")
        log_message(f"📢 {self.name} přistálo!")


# =============================================================================
# =============================================================================

if __name__ == "__main__":

    # Zaznamenání startu skriptu
    log_message(f"🚀 === START {os.path.basename(__file__)} - {LOG_FILE} ===")
    print(f"🚀 Skript spuštěn.")
    # print(f"Logovací soubor: {LOG_FILE}")

    auto = Auto("Tesla")
    auto.start()
    auto.stop()

    letadlo = Letadlo("Boeing 747")
    letadlo.vzlet()
    letadlo.pristani()

    disable_logging()

    auto.start()  # Toto volání už se nezaloguje

    # Zaznamenání ukončení skriptu
    print("🏁 Skript ukončen.")
    LOG_ENABLED = True  # Při ukončení skriptu se logování automaticky vypne
    log_message(f"🏁 === END Skript {os.path.basename(__file__)} ukončen. ===\n\n")
