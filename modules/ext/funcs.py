from decimal import Decimal

def isdigit(item:str) -> bool:
    "Tries to convert the given `item` into an integer using try/except"
    try: int(Decimal(item)); return True
    except: return False

def format_seconds(delta:int) -> str:
    "Formats an integer representing seconds, breaking it into days, hours, minutes, and seconds"
    days = int(delta/3600/24); hours = int(delta/3600)%24; minutes = int((delta%3600)/60); seconds = int(delta%3600%60)
    return "{}{}{}{}".format("{} day{}, ".format(days, 's' if days!=1 else '') if days else '', "{} hour{}, ".format(hours, 's' if hours!=1 else '') if hours else '', "{} minute{}".format(minutes, 's' if minutes!=1 else '') if minutes or hours else '', "{} second{}".format(seconds, 's' if seconds!=1 else '') if not (minutes or hours) else '')

def value_in(list_):
    list_ = list(map(str.casefold, list_))

    def inner(text):
        text = str(text).casefold()
        if text in list_: return text
        else: raise ValueError(f"`{text}` is not an acceptable value.")

    return inner