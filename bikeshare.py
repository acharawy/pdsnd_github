import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\nPlease choose a city (Chicago, new york city or washington): \n')).lower()
            if city not in CITY_DATA.keys():
                print('Invalid input\n')
                continue
            else:
                break
        except ValueError:
            print('Invalid input')
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month? '
                              '\nPlease choose from (january, february, march, april, may, june or all): \n')).lower()
            if month not in months and month != 'all':
                print('Data only available for (january, february, march, april, may, june or all\n')
                continue
            else:
                break
        except ValueError:
            print('Invalid input')
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Enter a day of the week): \n')).lower()
            if day not in days and day != 'all':
                print('Invalid input!\n')
                continue
            else:
                break
        except ValueError:
            print('Invalid input')
            break

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
    # load data file into a dataframe
    df = pd.DataFrame(pd.read_csv(CITY_DATA[str(city)]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        number = int(months.index(month)) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == number]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = months[((df['month'].mode()[0]) - 1)]
    print('{} is the most common month for bike sharing.'.format(month_mode).title())

    # display the most common day of week

    dow_mode = df['day_of_week'].mode()[0]
    print('{} is the most common day of the week for bike-sharing.'.format(dow_mode))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour of the day for bike sharing is {}:00.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    SStation_mode = df['Start Station'].mode()[0]
    print('Most people start from "{}" station.'.format(SStation_mode))

    # display most commonly used end station
    EStation_mode = df['End Station'].mode()[0]
    print('Most people start from "{}" station.'.format(EStation_mode))

    # display most frequent combination of start station and end station trip
    CombStation_mode = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('Most people start and end their trips at "{}" stations, consequently.'.format(CombStation_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Time_sum = df['Trip Duration'].sum() / 3600
    print('The sum of durations of all trips is {} hours.'.format(Time_sum))

    # display mean travel time
    Time_mean = df['Trip Duration'].mean() / 60
    print('The sum of durations of all trips is {} minutes.'.format(Time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        User_type_count = df.groupby(['User Type'])['User Type'].count()
        print('User types and their counts \n {}\n'.format(User_type_count))

        # Display counts of gender
        Gender_count = df.groupby(['Gender'])['Gender'].count()
        print('The gender distribution is as following: \n {}\n'.format(Gender_count))

        # Display earliest, most recent, and most common year of birth
        Oldest = int(df['Birth Year'].min())
        small = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode())
        print('The earliest year of birth is: {}'.format(Oldest))
        print('The most recent year of birth is: {}'.format(small))
        print('The most common year of birth is: {}'.format(common))
    except:
        print('sorry, some data are missing.')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

def data_display(df):
    """
    Asks user if he want to visualize the data.

    Returns:
         5 rows of data each time.
    """
    # Display 5 rows of data from n to m
    n = 0
    m = 5
    ddf = df.iloc[n:m]
    while True:
        try:
            # Display the first question.
            display = input('\nWould you like to see the first 5 rows of the data? Enter yes or no.\n')

            if display.lower() == 'no':
                print('Great!')

            elif display.lower() == 'yes':
                print(ddf)

                while True:
                    # Display the subsequent question.
                    display2 = input('\nWould you like to see the next 5 rows of the data? Enter yes or no.\n')

                    # specify the new values of n and m.
                    if display2.lower() == 'yes':
                        n += 5
                        m += 5
                        ddf = df.iloc[n:m]
                        print(ddf)
                        continue

                    elif display2.lower() == 'no':
                        print('Great!')
                        break

                    else:
                        print('Invalid input')
                        continue

            else:
                print('Invalid input')
                continue
            break

        except ValueError:
            print('Invalid input')
            continue




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
