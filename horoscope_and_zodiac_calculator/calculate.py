from datetime import datetime
from lunardate import LunarDate

# Western zodiac date ranges
western_zodiac = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
    ("Capricorn", (12, 22), (12, 31)),  # Handles Dec 22–31 edge case
]

# Chinese zodiac cycle
chinese_zodiac = [
    "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat",
    "Monkey", "Rooster", "Dog", "Pig"
]


def get_western_horoscope(month: int, day: int) -> str:
    for sign, start, end in western_zodiac:
        start_month, start_day = start
        end_month, end_day = end
        if (month == start_month and day >= start_day) or \
           (month == end_month and day <= end_day) or \
           (start_month < end_month and start_month < month < end_month) or \
           (start_month > end_month and (month > start_month or month < end_month)):
            return sign
    return "Unknown"


def get_chinese_zodiac(year: int, month: int, day: int) -> str:
    birth_date = datetime(year, month, day).date()  # Convert to date object

    # Find Chinese New Year for that Gregorian year
    cny = LunarDate(year, 1, 1).toSolarDate()

    # If birthday is before Chinese New Year, use previous year's zodiac
    zodiac_year = year if birth_date >= cny else year - 1
    index = (zodiac_year - 1900) % 12
    return chinese_zodiac[index]


def get_astrology_info(birthdate_str: str) -> dict:
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    horoscope = get_western_horoscope(birthdate.month, birthdate.day)
    zodiac = get_chinese_zodiac(birthdate.year, birthdate.month, birthdate.day)

    return {"Western Horoscope": horoscope, "Chinese Zodiac": zodiac}


# --- Test ---
if __name__ == "__main__":
    # Sample input
    date_str = input("Enter your birthdate (YYYY-MM-DD): ")
    result = get_astrology_info(date_str)

    if "error" in result:
        print(result["error"])
    else:
        print("Western Horoscope:", result["Western Horoscope"])
        print("Chinese Zodiac:", result["Chinese Zodiac"])
