# -- Strings --
ALL_FILTER = 'all'
START_TIME = 'Start Time'
END_TIME = 'End Time'
START_STATION = 'Start Station'
END_STATION = 'End Station'
USER_TYPE = 'User Type'
GENDER = 'Gender'
BIRTH_YEAR = 'Birth Year'
# Prompt Messages
filter_prompt_msg = \
    'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. '
city_prompt_msg = 'Would you like to see data for Chicago, New York, or Washington? '
month_prompt_msg = \
    'Which month? January, February, March, April, May, or June? '
day_prompt_msg = 'Which day? Please type your response as an integer (e.g. 1=Sunday). '

# -- Arrays --
ALLOWED_FILTER_CHOICES = [
    'day',
    'month',
    'both',
    'none',
]

# -- Dicts --
# list of files for each city
CITY_DATA = {
    'New York': './formatted_data/new_york_city.csv',
    'Chicago': './formatted_data/chicago.csv',
    'Washington': './formatted_data/washington.csv',
}
MONTHS_MAP = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}
DAYS_MAP = {
    'Sunday': 1,
    'Monday': 2,
    'Tuesday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Friday': 6,
    'Saturday': 7,
}
