import numpy as np

import constants
import errors


def nan_coalesce(val, fallback_val, _type=int):
    return fallback_val if np.isnan(val) else _type(val)


def parse_filter_choice(filter_choice):
    filter_choice = filter_choice.strip().lower()
    if filter_choice not in constants.ALLOWED_FILTER_CHOICES:
        raise errors.ValidationError('Invalid "Filter Choice" input.')

    return filter_choice


def parse_city(city):
    city = city.strip().replace('_', ' ').title()
    if city not in constants.CITY_DATA:
        raise errors.ValidationError('Invalid "City" input.')

    return city


def parse_day(day):
    if day == 'all':
        return 0

    try:
        return int(day)
    except ValueError:
        try:
            return constants.DAYS_MAP[day.title()]
        except KeyError:
            raise errors.ValidationError('Invalid "Day" input.')


def parse_month(month):
    if month == 'all':
        return 0

    try:
        return int(month)
    except ValueError:
        try:
            return constants.MONTHS_MAP[month.title()]
        except KeyError:
            raise errors.ValidationError('Invalid "Month" input.')


def extract_timedelta(timedelta):
    """
    Extracts np.Timedelta properties

    :arg
        (np.Timedelta) timedelta

    :returns tuple of days, hours, minutes, seconds
    """
    return (timedelta.days, np.round(timedelta.seconds / 3600, 2),
            np.round(timedelta.seconds / 360, 2), np.round(timedelta.seconds % 60, 2))
