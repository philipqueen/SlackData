from enum import Enum

class Currency(str, Enum):
    """
    Enum for ISO 4217 currency codes.
    """
    ARS = "ARS"  # Argentine Peso
    AUD = "AUD"  # Australian Dollar
    BOB = "BOB"  # Boliviano
    BRL = "BRL"  # Brazilian Real
    BYN = "BYN"  # Belarusian Ruble
    CAD = "CAD"  # Canadian Dollar
    CHF = "CHF"  # Swiss Franc
    CLP = "CLP"  # Chilean Peso
    CNY = "CNY"  # Chinese Yuan
    COP = "COP"  # Colombian Peso
    CZK = "CZK"  # Czech Koruna
    DKK = "DKK"  # Danish Krone
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound
    HKD = "HKD"  # Hong Kong Dollar
    ILS = "ILS"  # Israeli New Shekel
    INR = "INR"  # Indian Rupee
    IRR = "IRR"  # Iranian Rial
    JPY = "JPY"  # Japanese Yen
    KRW = "KRW"  # South Korean Won
    MXN = "MXN"  # Mexican Peso
    PEN = "PEN"  # Peruvian Sol
    PLN = "PLN"  # Polish Zloty
    RUB = "RUB"  # Russian Ruble
    SEK = "SEK"  # Swedish Krona
    SGD = "SGD"  # Singapore Dollar
    TRY = "TRY"  # Turkish Lira
    UAH = "UAH"  # Ukrainian Hryvnia
    USD = "USD"  # United States Dollar
    ZAR = "ZAR"  # South African Rand