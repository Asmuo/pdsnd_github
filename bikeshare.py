import time
import pandas as pd
import numpy as np
import colorama as clr
clr.init()

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_DATA = { 'all': 0,
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june':6 }

MONTH_LIST = list(MONTHS_DATA.keys())

DAY_DATA = ['all',
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday']

YES_NO_DATA = {'yes': True,
               'no': False}

STATISTIC_DATA = {'time': 1,
                  'station': 2,
                  'trip duration': 3,
                  'user information': 4,
                  'raw data': 5 }

CITY_TEXT = ( clr.Fore.YELLOW + 'chicago' + clr.Fore.RESET,
              clr.Fore.YELLOW + 'new york city' + clr.Fore.RESET,
              clr.Fore.YELLOW + 'washington' + clr.Fore.RESET )

MONTH_TEXT = ( clr.Fore.YELLOW + 'all' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'january' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'february' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'march' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'april' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'may' + clr.Fore.RESET,
               clr.Fore.YELLOW + 'june' + clr.Fore.RESET )

DAY_TEXT = ( clr.Fore.YELLOW + 'all' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'monday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'tuesday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'wednesday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'thursday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'friday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'saturday' + clr.Fore.RESET,
             clr.Fore.YELLOW + 'sunday' + clr.Fore.RESET )

YES_NO_TEXT = ( clr.Fore.YELLOW + 'yes' + clr.Fore.RESET,
                clr.Fore.YELLOW + 'no' + clr.Fore.RESET )

STATISTIC_TEXT = ( clr.Fore.YELLOW + 'time' + clr.Fore.RESET,
                   clr.Fore.YELLOW + 'station' + clr.Fore.RESET,
                   clr.Fore.YELLOW + 'trip duration' + clr.Fore.RESET,
                   clr.Fore.YELLOW + 'user information' + clr.Fore.RESET,
                   clr.Fore.YELLOW + 'raw data' + clr.Fore.RESET )


def error_message(word):
    """
    Displays error message with the specified word in red color.
    
    Args:
        (str) word - the word that will be formated in red and printed.
    Returns:
        (str) 3 line of error text with a specified word in red."""

    formatted_word = clr.Fore.RED + '"{}"'.format(word) + clr.Fore.RESET
    print('\nINCORRECT VALUE! {} is not a valid value!'.format(formatted_word))
    print('Please check for spelling mistakes and try again.\n')
    print('-' * 40)    


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-' * 40)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-' * 40, '')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input('\nPlease type a city name ({}, {} or {}):\n'.format(*CITY_TEXT))
        try:
            city = CITY_DATA[city_input.lower()]
            break
        except:
            error_message(city_input)

    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input('\nWhich month are you interested in? ({}, {}, {}, {}, {}, {} or {}):\n'.format(*MONTH_TEXT))
        try:
            month = MONTHS_DATA[month_input.lower()]
            month = MONTH_LIST[month]
            break
        except:
            error_message(month_input)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input('\nWhich day of week you are interested in? ({}, {}, {}, {}, {}, {}, {} or {}):\n'.format(*DAY_TEXT))
        if day_input.lower() in DAY_DATA:
            day = day_input.lower()
            break
        else:
            error_message(day_input)

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
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour
    if 'Birth Year' in df.columns:
        df['Birth Year'].fillna(df['Birth Year'].mean(), inplace=True)
        df['Birth Year'] = df['Birth Year'].astype(int)
    if month != 'all':
        df = df[df['month'] == MONTHS_DATA[month]]
    if day != 'all':
        df = df[df['weekday'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_msg = clr.Fore.GREEN + MONTH_LIST[popular_month].title() + clr.Fore.RESET
    print('{} is the peak month in the chosen period.'.format(month_msg))

    # display the most common day of week
    popular_DOW = df['weekday'].mode()[0]
    DOW_mgs = clr.Fore.GREEN + popular_DOW + clr.Fore.RESET
    print('{} is the peak day in the chosen period.'.format(DOW_mgs))

    # display the most common start hour
    popular_start_h = df['start_hour'].mode()[0]
    start_h_msg = clr.Fore.GREEN + str(popular_start_h) + 'h' + clr.Fore.RESET
    print('{} is the peak starting hour in the chosen period.'.format(start_h_msg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station_msg = clr.Fore.GREEN + popular_start_station + clr.Fore.RESET
    print('{} is the most frequently used route starting station.'.format(start_station_msg))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station_msg = clr.Fore.GREEN + popular_end_station + clr.Fore.RESET
    print('{} is the most frequently used route ending station.'.format(end_station_msg))

    # display most frequent combination of start station and end station trip
    popular_stations_combination = df[['Start Station', 'End Station']].value_counts().index[0]
    pop_comb_start_station = popular_stations_combination[0]
    pop_comb_end_station = popular_stations_combination[1]
    start_station_msg = clr.Fore.GREEN + pop_comb_start_station + clr.Fore.RESET
    end_station_msg = clr.Fore.GREEN + pop_comb_end_station + clr.Fore.RESET
    print('{} & {} are the most frequently used combination of starting & ending route stations.'.format(start_station_msg, end_station_msg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600 
    total_travel_msg = clr.Fore.GREEN + str(total_travel_time.round()) + 'h' + clr.Fore.RESET
    print('Total travel time in the selected period is: {}'.format(total_travel_msg))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600
    mean_travel_msg = clr.Fore.GREEN + str(mean_travel_time.round(2)) + 'h' + clr.Fore.RESET
    print('Average time per travel in the selected period is: {}'.format(mean_travel_msg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_users = df['User Type'].value_counts()
    print('In total there are:')
    for user in count_of_users.index:
        user_msg = clr.Fore.GREEN + user + "'s" + clr.Fore.RESET
        user_qty_msg = clr.Fore.GREEN + str(count_of_users[user]) + clr.Fore.RESET
        print('{} amount of {} in the selected period'.format(user_qty_msg, user_msg))

    # Display counts of gender
    try:
        count_of_genders = df['Gender'].value_counts()
        print('\nIn total there are:')
        for gender in count_of_genders.index:
            gender_msg = clr.Fore.GREEN + gender + "'s" + clr.Fore.RESET
            gender_qty_msg = clr.Fore.GREEN + str(count_of_genders[gender]) + clr.Fore.RESET
            print('{} amount of {} in the selected period.'.format(gender_qty_msg, gender_msg))
    except:
        print(clr.Fore.RED + 'There is no data about Users gender in this city!' + clr.Fore.RESET)

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_client_msg = clr.Fore.GREEN + str(df['Birth Year'].min()) + clr.Fore.RESET
        youngest_client_msg = clr.Fore.GREEN + str(df['Birth Year'].max()) + clr.Fore.RESET
        most_clients_msg = clr.Fore.GREEN + str(df['Birth Year'].mode()[0]) + clr.Fore.RESET
        print('\nOldest client in the selected period is born on:', oldest_client_msg)
        print('Youngest client in the selected period is born on:', youngest_client_msg)
        print('The most common year of birth in the selected period is:', most_clients_msg)
    except:
        print(clr.Fore.RED + 'There is data about Users year of birth in this city!' + clr.Fore.RESET)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def chunker(df, chunk_size):
    """
        Generator that returns data by the specified chunk size.
    Args:
        (DataFrame) - df
        (int) - chunk_size
    """
    for row in range(0, df.size, chunk_size):
        yield df.iloc[row: row + chunk_size]


def raw_data(df):
    """
        Displays chuck of data per iteration. Every iteration ask if user wants to see more data.
    Args:
        (DataFrame) - df
    """
    pd.set_option('display.max_columns', 200)
    for chunk in chunker(df, 5):
        print(chunk)

        more_data = True
        while more_data:
            more_data = input('\nDo you want to see more data? Enter {} or {}.\n'.format(*YES_NO_TEXT))
            try:
                more_data = not YES_NO_DATA[more_data]
                if more_data:
                    break
            except:
                error_message(more_data)
        if more_data:
            break


def execute_statistics(statistic_name, df):
    """
    Executes the choosen statistics.
    
    Args:
        (str)  - statistic name - statistics that user is interested in.
        (df)   - pandas data frame.
    """

    return {
        'time': lambda: time_stats(df),
        'station': lambda: station_stats(df),
        'trip duration': lambda: trip_duration_stats(df),
        'user information': lambda: user_stats(df),
        'raw data': lambda: raw_data(df)
    }[statistic_name]()


def choose_statistic(df):

    """Asks user what statistics to displays and checks if user would like to see more statistics."""

    run = True
    while run:
        statistic_input = input('\nPlease type statistics you are interested in ({}, {}, {}, {} or {}):\n'.format(*STATISTIC_TEXT))
        try:
            STATISTIC_DATA[statistic_input.lower()]
            execute_statistics(statistic_input.lower(), df)

            more_statistics = True
            while more_statistics:
                more_statistics = input('\nDo you want to see more statistics? Enter {} or {}.\n'.format(*YES_NO_TEXT))
                try:
                    more_statistics = not YES_NO_DATA[more_statistics.lower()]
                    if more_statistics:
                        more_statistics = False
                        run = False
                except:
                    error_message(more_statistics)
        except:
            error_message(statistic_input)


def restart():
    """Asks user if user wants to restart the program.
    
    Returns:
        (bool) - True - if user whant to restart the program else - False.
    """
    while True:
        restart = input('\nWould you like to restart the program? Enter {} or {}.\n'.format(*YES_NO_TEXT))
        try:
            restart = YES_NO_DATA[restart.lower()]
            return restart
        except:
            error_message(restart)


def main():
    run = True
    while run:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        choose_statistic(df)
        run = restart()

    print('')
    print('-' * 40)
    print('Thank you for using this program.')
    print('Have a great day!\n')

if __name__ == "__main__":
	main()
