import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = ['january', 'february', 'mars', 'april', 'may', 'june', 'all']
    days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']

    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('please select a city, type:\n chicago\n or new york city\n or washington\n').lower()
    while city not in CITY_DATA:
        print('invalid city name')
        city = input('please select a city, type:\n chicago\n or new york city\n or washington\n').lower()
    month = input("select a month or select all if you don't want to select a specific one").lower()

    while month not in months:
        print('invalid month choice')
        month = input("select a month or select all if you don't want to select a specific one").lower()

    day = input('select a day or select all').lower()
    while day not in days:
        print('invalid day name')
        day = input('select a day or select all').lower()

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

    df = pd.read_csv(CITY_DATA[city])
    print(df.head())

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    print(df['Start Time'])

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'mars', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

        # Filter by day
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month - 1]
    print('Most Popular Start Month:', popular_month)

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print('Most Popular Start day:', popular_day)

    # display the most common start hour
    most_common_hr = df['hour'].mode()[0]
    print('most common hour is: ', most_common_hr)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_st = df['Start Station'].mode()[0]
    print('most common start station is: {}'.format(most_common_start_st))

    # display most commonly used end station
    most_common_end_st = df['End Station'].mode()[0]
    print('most common end station is: {}'.format(most_common_end_st))

    # display most frequent combination of start station and end station trip
    df["route"] = df["Start Station"] + "-" + df["End Station"]
    most_freq_comb = df.route.mode()[0]
    print('most most frequent combination of start station and end station trip is: {}'.format(most_freq_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    # """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total trip duration is:{} ".format(total_travel_time))

    # display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print("mean travel time is:{} ".format(travel_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('count of user type:{}'.format(counts_of_user_types))

    # Display counts of gender
    if 'Gender' in df:
        counts_gender = df['Gender'].value_counts()
        print('count of genders:{}'.format(counts_gender))
    # Only access Gender column in this case
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(city):
    df = pd.read_csv(CITY_DATA[city])

    print('\nRaw data is available to check... \n')
    start_loc = 0
    while True:
        display_option = input('To View the available raw data in  5 rows type: Yes if not type: No \n').lower()
        if display_option not in ['yes', 'no']:
            print('That\'s invalid choice, pleas type yes or no')

        elif display_option == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5

        elif display_option == 'no':
            print('\nExiting...')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

# references
# udacity problem solutions in classroom
# fwd community walk through presentation
# https://github.com/Aritra96/bikeshare-project/blob/master/bikeshare.py
