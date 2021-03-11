import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        city -  name of the city to analyze
        month - name of the month to filter by,
                or "all" to apply no month filter
        day -   name of the day of week to filter by,
                or "all" to apply no day filter
    """

    city, month, day = '', '', ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city_valid = False
    while city_valid is False:
        city = input('Of which city do you want to explore bikeshare data: \n'
                     '"Chicago", "New York City" or Washington"?\n')
        valid_cities = {'chicago': ['chicago',
                                    'c',
                                    '1'],
                        'new york city': ['new york city',
                                          'new york',
                                          'n',
                                          'nyc',
                                          '2'],
                        'washington': ['washington',
                                       'w',
                                       '3']}
        for key, value in valid_cities.items():
            if str(city).lower().strip() in value:
                city = key
                city_valid = True
                break
        else:
            print('\n-----Please enter a valid city!-----\n\n')

    # get user input for month
    month_valid = False
    while month_valid is False:
        month = input('Of which month would you like do see data?\n'
                      'Data from January to June is available\n'
                      'If you don\'t want to filter by month, '
                      'type "all" or "0"!\n')
        valid_months = {'all': ['all',
                                '0'],
                        'january': ['january',
                                    'jan',
                                    '1'],
                        'february': ['february',
                                     'feb',
                                     '2'],
                        'march': ['march',
                                  'mar',
                                  '3'],
                        'april': ['april',
                                  'apr',
                                  '4'],
                        'may': ['may',
                                '5'],
                        'june': ['june',
                                 'jun',
                                 '6']}
        for key, value in valid_months.items():
            if str(month).lower().strip() in value:
                month = key
                month_valid = True
                break
        else:
            print('\n-----Please enter a valid month!-----\n\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_valid = False
    while day_valid is False:
        day = input('Of which day of the week would you like do see data?\n'
                    '"Monday" (1) to "Sunday" (7)\n'
                    'If you don\'t want to filter by day, '
                    'type "all" or "0"!\n')
        valid_days = {'all': ['all',
                              '0'],
                      'monday': ['monday',
                                 'mon',
                                 '1'],
                      'tuesday': ['tuesday',
                                  'tue',
                                  '2'],
                      'wednesday': ['wednesday',
                                    'wed',
                                    '3'],
                      'thursday': ['thursday',
                                   'thu',
                                   '4'],
                      'friday': ['friday',
                                 'fri',
                                 '5'],
                      'saturday': ['saturday',
                                   'sat',
                                   '6'],
                      'sunday': ['sunday',
                                 'sun',
                                 '7']}
        for key, value in valid_days.items():
            if str(day).lower().strip() in value:
                day = key
                day_valid = True
                break
        else:
            print('\n-----Please enter a valid day of the week!-----\n\n')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters
    by month and day if applicable.

    Args:
        city -  name of the city to analyze
        month - name of the month to filter by,
                or "all" to apply no month filter
        day -   name of the day of week to filter by,
                or "all" to apply no day filter
    Returns:
        df -    Pandas DataFrame containing city data
                filtered by month and day
    """

    # load data file into a dataframe
    df_raw = pd.read_csv(CITY_DATA[city])
    df = df_raw.copy(deep=True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january',
                  'february',
                  'march',
                  'april',
                  'may',
                  'june']
        month = months.index(month.lower())+1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.capitalize()]
    return df_raw, df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    input('Press "ENTER" to continue:')
    print('-' * 40)
    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['month'].mode()[0]
    print('The month with the most times of travel: ', mode_month)

    # display the most common day of week
    mode_day = df['day_of_week'].mode()[0]
    print('The day of week with the most times of travel: ', mode_day)

    # display the most common start hour
    mode_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common start hour: ', mode_hour)

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    input('Press "ENTER" to continue:')
    print('-' * 40)
    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_startstation = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', mode_startstation)

    # display most commonly used end station
    mode_endstation = df['End Station'].mode()[0]
    print('The most commonly used end station: ', mode_endstation)

    # display most frequent combination of start station and end station trip
    mode_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most common trip is from "{mode_trip[0]}" to "{mode_trip[1]}"')

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    input('Press "ENTER" to continue:')
    print('-' * 40)
    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total_days = divmod(df['Trip Duration'].sum(), 3600*24)
    total_hours = divmod(total_days[1], 3600)
    total_minutes = divmod(total_hours[1], 60)
    print('The total trip duration: '
          '{} days {} hours and {} minutes'.format(int(total_days[0]),
                                                   int(total_hours[0]),
                                                   int(total_minutes[0])))

    # display mean travel time in minutes
    mean_minutes = divmod(df['Trip Duration'].mean(), 60)
    print('The mean trip duration: '
          '{} minutes and {} seconds'.format(int(mean_minutes[0]),
                                             int(mean_minutes[1].round())))
    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    input('Press "ENTER" to continue:')
    print('-' * 40)
    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertype_count = df['User Type'].value_counts()
    usertypes = usertype_count.count()
    print(f'There are {usertypes} different user types!')
    for index, value in usertype_count.items():
        print(' ', value, index)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        genders = gender_count.count()
        print(f'There are {genders} different genders registered!')
        for index, value in gender_count.items():
            print(f'  {value} Subscribers are {index}')
    else:
        print('There are no data on Genders in this city!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        youngest = df['Birth Year'].max()
        oldest = df['Birth Year'].min()
        mode_yob = df['Birth Year'].mode()
        print('The youngest Subscriber was born in: ', int(youngest))
        print('  The oldest Subscriber was born in: ', int(oldest))
        print('   The most common Year of Birth is: ', int(mode_yob[0]))
    else:
        print('There are no data on Years of Birth in this city!')

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def display_raw(df_raw):
    """
    Asks user to whether raw data should be displayed or not.

    If yes:
    Displays the first 5 lines of raw data.
    """
    # get user input whether raw data should be displayed or not
    see_raw = input('Do you want to see the first few lines of raw data?\n'
                    'Type "yes"/"y" or any other to continue without:\n')
    if str(see_raw).lower().strip() in ('yes', 'y'):
        print(df_raw.head())
        print('-' * 40)
    else:
        print('No raw data requested..\n'
              '..continuing with statistics!')
        print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df_raw, df = load_data(city, month, day)
        display_raw(df_raw)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
