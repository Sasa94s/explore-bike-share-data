import time
import pandas as pd

import constants
import errors
import utils

FILTER_CHOICE = None
CITY_CHOICE = None


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    city = utils.parse_city(input(constants.city_prompt_msg))

    # filter choice: [day, month, both, none]
    global FILTER_CHOICE
    FILTER_CHOICE = utils.parse_filter_choice(input(constants.filter_prompt_msg))

    if FILTER_CHOICE == 'both':
        # get user input for month (all, january, february, ... , june)
        month = utils.parse_month(input(constants.month_prompt_msg))

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = utils.parse_day(input(constants.day_prompt_msg))
    elif FILTER_CHOICE == 'month':
        month = utils.parse_month(input(constants.month_prompt_msg))
        day = utils.parse_day(constants.ALL_FILTER)
    elif FILTER_CHOICE == 'day':
        month = utils.parse_month(constants.ALL_FILTER)
        day = utils.parse_day(input(constants.day_prompt_msg))
    else:
        month = utils.parse_month(constants.ALL_FILTER)
        day = utils.parse_day(constants.ALL_FILTER)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(constants.CITY_DATA[city])

    # For debugging
    # print('Pre-Filtered Loaded Data Size:- Rows: {}, Columns: {}'.format(len(df), len(df.columns)))

    # convert Start Time and End Time columns to DateTime data type
    df[constants.START_TIME] = pd.to_datetime(df[constants.START_TIME])
    df[constants.END_TIME] = pd.to_datetime(df[constants.END_TIME])

    if month != 0:
        df = df[df[constants.START_TIME].dt.month == month]

    if day != 0:
        df = df[(df[constants.START_TIME].dt.dayofweek + 1) % 7 + 1 == day]  # Sunday = 1

    # For debugging
    # print('Filtered Loaded Data Size:- Rows: {}, Columns: {}'.format(len(df), len(df.columns)))
    # print(df.info())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    global FILTER_CHOICE
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_freq = df[constants.START_TIME].groupby([df[constants.START_TIME].dt.month]).count()
    max_month_freq = month_freq[month_freq == month_freq.max()]
    if len(max_month_freq) > 0:
        print('Most popular Month: {}, Count: {}, Filter: {}'
              .format(max_month_freq.keys()[0], max_month_freq.values[0], FILTER_CHOICE))
    else:
        print('Most popular Month: "No data to be displayed".')
    print('-' * 10)

    # display the most common day of week
    dow_freq = df[constants.START_TIME].groupby([df[constants.START_TIME].dt.dayofweek]).count()
    max_dow_freq = dow_freq[dow_freq == dow_freq.max()]
    if len(max_dow_freq) > 0:
        print('Most popular Day of Week: {}, Count: {}, Filter: {}'
              .format(max_dow_freq.keys()[0], max_dow_freq.values[0], FILTER_CHOICE))
    else:
        print('Most popular Day of Week: "No data to be displayed".')
    print('-' * 10)

    # display the most common start hour
    hour_freq = df[constants.START_TIME].groupby([df[constants.START_TIME].dt.hour]).count()
    max_hour_freq = hour_freq[hour_freq == hour_freq.max()]
    if len(max_hour_freq) > 0:
        print('Most popular Hour: {}, Count: {}, Filter: {}'
              .format(max_hour_freq.keys()[0], max_hour_freq.values[0], FILTER_CHOICE))
    else:
        print('Most popular Hour: "No data to be displayed".')
    print('-' * 10)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_st_freq = df[constants.START_STATION].groupby([df[constants.START_STATION]]).count()
    max_start_st_freq = start_st_freq[start_st_freq == start_st_freq.max()]
    if len(max_start_st_freq) > 0:
        print('Most popular Start Station: {}, Count: {}, Filter: {}'
              .format(max_start_st_freq.keys()[0], max_start_st_freq.values[0], FILTER_CHOICE))
    else:
        print('Most popular Start Station: "No data to be displayed".')
    print('-' * 10)

    # display most commonly used end station
    end_st_freq = df[constants.END_STATION].groupby([df[constants.END_STATION]]).count()
    max_end_st_freq = end_st_freq[end_st_freq == end_st_freq.max()]
    if len(max_end_st_freq) > 0:
        print('Most popular End Station: {}, Count: {}, Filter: {}'
              .format(max_end_st_freq.keys()[0], max_end_st_freq.values[0], FILTER_CHOICE))
    else:
        print('Most popular End Station: "No data to be displayed".')
    print('-' * 10)

    # display most frequent combination of start station and end station trip
    start_end_st_freq = df.groupby([constants.START_STATION, constants.END_STATION]).size().reset_index()
    max_start_end_st_freq = start_end_st_freq[start_end_st_freq[0] == start_end_st_freq[0].max()]
    print('Most popular both Start and End Station:-')
    for idx, row_idx in enumerate(max_start_end_st_freq.index):
        max_start_end_st_freq_row = max_start_end_st_freq.loc[row_idx]
        print('[#{}] - Start Station Name: {}, End Station Name: {}, Count: {}, Filter: {} '
              .format(idx + 1, max_start_end_st_freq_row[constants.START_STATION],
                      max_start_end_st_freq_row[constants.END_STATION][0],
                      max_start_end_st_freq_row[0], FILTER_CHOICE))
    else:
        print('Most popular both Start and End Station: "No data to be displayed".')
    print('-' * 10)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df[constants.END_TIME] - df[constants.START_TIME]).sum()
    print('Total Time Travel:- Days: {}, Hours: {}, Minutes: {}, Seconds: {}'
          .format(*utils.extract_timedelta(total_travel_time)))
    print('-' * 10)

    # display mean travel time
    mean_travel_time = (df[constants.END_TIME] - df[constants.START_TIME]).mean()
    print('Mean Time Travel:- Days: {}, Hours: {}, Minutes: {}, Seconds: {}'
          .format(*utils.extract_timedelta(mean_travel_time)))
    print('-' * 10)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertype_freq = df[constants.USER_TYPE].groupby([df[constants.USER_TYPE]]).count()
    print('User Types Count:-')
    for idx, user_type in enumerate(usertype_freq.index):
        print('[#{}] - User Type: {}, Count: {}'
              .format(idx + 1, user_type, usertype_freq[user_type]))
    print('-' * 10)

    if CITY_CHOICE != 'Washington':
        # Display counts of gender
        gender_freq = df[constants.GENDER].groupby([df[constants.GENDER]]).count()
        print('Gender Count:-')
        for idx, gender in enumerate(gender_freq.index):
            print('[#{}] - Gender: {}, Count: {}'
                  .format(idx + 1, gender, gender_freq[gender]))
        print('-' * 10)

        # Display earliest, most recent, and most common year of birth
        earliest_dob = df[constants.BIRTH_YEAR].min()
        print('Earliest Year of Birth: {}'.format(utils.nan_coalesce(earliest_dob, 0)))
        most_recent_dob = df[constants.BIRTH_YEAR].max()
        print('Most Recent Year of Birth: {}'.format(utils.nan_coalesce(most_recent_dob, 0)))
        most_common_dob = df[constants.BIRTH_YEAR].mode()
        print('Most Common Year of Birth: {}'.format(
            utils.nan_coalesce(most_common_dob[0], 0) if len(most_common_dob) > 0 else 0))
        print('-' * 10)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    global CITY_CHOICE

    while True:
        try:
            CITY_CHOICE, month, day = get_filters()
            df = load_data(CITY_CHOICE, month, day)

            if len(df) == 0:
                raise errors.ValidationError('No data to be displayed. Please change your filter options.')

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except errors.ValidationError as e:
            print('=' * 40)
            print('Error: {}'.format(e.message))
            print('=' * 40)
        finally:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
    main()
