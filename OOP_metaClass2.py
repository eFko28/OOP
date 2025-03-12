# -*- coding: utf-8 -*-
# Příliš žluťoučký kůň úpěl ďábelské ódy - testovací pangram

# Logování běhu programu do souboru pomocí metatřídy
"""_summary_
Tento Python skript demonstruje použití metatřídy pro automatické logování volání metod tříd. 
Program je navržen tak, aby zaznamenával všechny volání metod do logovacího souboru 
a zároveň vypisoval zprávy do terminálu. 

## Hlavní části programu
1. **Importy a nastavení logování**:
    - Importuje potřebné moduly jako `functools`, `logging`, `sys`, `os` a `datetime`.
    - Nastavuje základní konfiguraci logování, včetně názvu logovacího souboru, úrovně logování, formátu zpráv a kódování.

2. **Třída `DualLogger`**:
    - Tato třída přesměrovává výstup jak do terminálu, tak do logovacího souboru.
    - Metoda `write` zajišťuje, že všechny zprávy jsou zapsány do obou výstupů.
    - Metoda `flush` zajišťuje, že všechny výstupy jsou správně vyprázdněny.

3. **Metatřída `MetaLogger`**:
    - Tato metatřída automaticky obaluje všechny metody tříd, které ji používají, logovací funkcionalitou.
    - Metoda `__new__` přidává logování ke všem metodám nové třídy.
    - Metoda `_log_method` obaluje jednotlivé metody logováním.
    - Metody `enable_logging` a `disable_logging` umožňují zapnutí a vypnutí logování.

4. **Třídy `Auto` a `Letadlo`**:
    - Tyto třídy využívají metatřídu `MetaLogger` pro automatické logování volání jejich metod.
    - Třída `Auto` reprezentuje auto a obsahuje metody `start` a `stop`.
    - Třída `Letadlo` reprezentuje letadlo a obsahuje metody `vzlet` a `pristani`.

5. **Testování metatřídy s logováním**:
    - Vytváří instance tříd `Auto` a `Letadlo` a volá jejich metody, aby demonstroval logování.
    - Logování je následně vypnuto a je ukázáno, že volání metod již nejsou logována.

## Použití programu
1. **Spuštění skriptu**:
    - Skript zaznamená svůj start do logovacího souboru.
    - Vytvoří instance tříd `Auto` a `Letadlo` a volá jejich metody, což je zaznamenáno do logu.
    - Vypne logování a znovu volá metody, které již nejsou zaznamenány.
    - Skript zaznamená svůj konec do logovacího souboru.

Tento skript je užitečný pro studenty, kteří se chtějí naučit, jak používat metatřídy v Pythonu 
a jak implementovat logování volání metod automaticky.
"""

import functools
import logging
import sys
import os
from datetime import datetime

# Logování - povolení/vypnutí logování
LOG_ENABLED = True  # Přepínač pro zapnutí/vypnutí logování před startem skriptu

# Nastavení relativní cesty k logu
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")  # Relativní cesta k adresáři /log
LOG_FILE = os.path.join(LOG_DIR, "method_calls_2.log")  # Plná cesta k logovacímu souboru

# Pokud složka log neexistuje, vytvoříme ji
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Správné nastavení logování (vždy UTF-8, timestamp, formát zpráv)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)



# Třída pro správné přesměrování výstupu do logu i terminálu, pomocná třída
# Může být vynechána, pokud chcete pouze logovat do souboru bez terminálových stringů
class DualLogger:
    """Třída DualLogger zachytává výstup a posílá ho do logu i do terminálu.
    Bez této třídy by se výstup z terminálu nezobrazil v logu.
    Atributy:
        terminal (TextIO): Původní terminálový výstupní proud.
        log (TextIO): Výstupní proud logovacího souboru.
    Metody:
        Zapíše zprávu jak do terminálu, tak do logovacího souboru.
        Přeskakuje prázdné řádky, pokud je logování povoleno.
        Vyprázdní oba výstupní proudy, terminál i logovací soubor.
    """
    
    def __init__(self, original_stdout): 
        self.terminal = original_stdout                   # Původní terminálový výstup
        self.log = open(LOG_FILE, "a", encoding="utf-8")  # Správné kódování

    def write(self, message): 
        self.terminal.write(message)  # Výpis do terminálu
        self.terminal.flush()
        if LOG_ENABLED and message.strip():  # Přeskakujeme prázdné řádky, pokud je logování povoleno
            self.log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - TERMINÁL - {message}\n")
            self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()


# Metatřída, která automaticky loguje volání metod potomka do souboru.
# TOTO JE METATŘÍDA, KTERÁ SE POUŽÍVÁ JAKO METACLASS PŘI VYTVOŘENÍ NOVÝCH TŘÍD
class MetaLogger(type):
    """
    Metatřída MetaLogger automaticky loguje volání metod do souboru.
    Metody:
        __new__(cls, name, bases, dct):
            Přidá logování ke všem metodám nové třídy.
        _log_method(cls, method_name, method):
            Obalí metodu logováním, pokud je logování povoleno.
        enable_logging(cls):
            Zapne logování.
        disable_logging(cls):
            Vypne logování.
    """
 
    def __new__(cls, name, bases, dct):
        """Přidá logování ke všem metodám nové třídy."""
        for attr_name, attr_value in dct.items():
            if callable(attr_value):  # Pokud je atribut metoda, obalíme ji logováním
                dct[attr_name] = cls._log_method(attr_name, attr_value)
        return super().__new__(cls, name, bases, dct)

    @classmethod
    def _log_method(cls, method_name, method):
        """Obalí metodu logováním, pokud je logování povoleno."""
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            global LOG_ENABLED
            if LOG_ENABLED:
                log_msg = f"📢 Volání metody: {method_name}, Argumenty: {args}, {kwargs}"
                logging.info(log_msg)
            return method(*args, **kwargs)
        return wrapper

    @classmethod
    def enable_logging(cls):
        """Zapne logování."""
        global LOG_ENABLED
        LOG_ENABLED = True
        logging.info(f"📢 ZAPNUTO LOGOVÁNÍ")

    @classmethod
    def disable_logging(cls):
        """Vypne logování."""
        global LOG_ENABLED
        logging.info(f"📢 VYPNUTO LOGOVÁNÍ")
        LOG_ENABLED = False


# =============================================================================
# Dále už jen běžný program, jak jej známe z dřívějška
# =============================================================================

class Auto(metaclass=MetaLogger):
    """Třída reprezentující auto."""
    def __init__(self, model):
        self.model = model

    def start(self):
        print(f"🚗 {self.model} nastartovalo!")

    def stop(self):
        print(f"🚗 {self.model} zastavilo!")


class Letadlo(metaclass=MetaLogger):
    """Třída reprezentující letadlo."""
    def __init__(self, name):
        self.name = name
        print(f"✈️ Letadlo {self.name} bylo vytvořeno.")

    def vzlet(self):
        print(f"✈️ {self.name} vzlétlo!")

    def pristani(self):
        print(f"✈️ {self.name} přistálo!")


# =============================================================================
# =============================================================================

if __name__ == "__main__":
    # Přesměrování výstupu do terminálu i logu (nutné pro výpis terminálových zpráv do logu)
    sys.stdout = DualLogger(sys.stdout)

    # Zaznamenání startu skriptu - vždy
    logging.info(f"=============== 🚀 Skript {os.path.basename(__file__)} spuštěn. ===============")

    # Test metatříd s logováním
    auto = Auto("Tesla")
    auto.start()
    auto.stop()

    letadlo = Letadlo("Boeing 747")
    letadlo.vzlet()
    letadlo.pristani()

    MetaLogger.disable_logging()  # Vypneme logování

    auto.start()  # Toto volání už se nezaloguje

    # Zaznamenání ukončení skriptu - vždy
    logging.info(f"=============== 🏁 Skript {os.path.basename(__file__)} ukončen. ===============\n\n")
