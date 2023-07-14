import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'bean town': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'new york': 'new_york_city.csv',
              'big apple': 'new_york_city.csv',
              'the big apple': 'new_york_city.csv',
              'dc': 'washington.csv',
              'd.c.': 'washington.csv',
              'washington dc': 'washington.csv',
              'washington d.c.': 'washington.csv'}
              #Town aliases and nicknames added for the creative user input

def say_hello():
    """This functions says hello to the user and ask if they would like to run the program!

    Arguments:
    User Input - The user is asked to answer yes or no
    No response but yes or no (.lower used to avoid case sensitivity) is accepted.
    The input request is reapeated until acceptable input is provided or keyboard interrupt is utilized

    Returns:
    (str) start - a lowercase string of 'yes' or 'no'
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('\nWould you like to explore some bikeshare data?')

    yes_or_no = ('yes', 'no')
    start = input('\nPlease enter "yes" or "no": \n').lower()
    while start not in yes_or_no:
        print('\nSorry, that is not an acceptable response. Please try again')
        start = input('\nPlease enter "yes" or "no": \n').lower()
    return start

def get_filters(start):
    """
    Asks user to specify a city, month, and day to analyze.

    Arguments:
        (str) start - tells the program to continue running (if 'yes') or stop (if 'no')

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month_input = ['january', 'february', 'march', 'april', 'may', 'june', 'all'] # acceptable input for the month variable

    day_input = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'] #acceptable input for the day variable

    while True:
        if start == 'yes':
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            print('\nFirst, We need to select a city to view data from. \n')
            print('Would you like to view data from Chicago, New York City, or Washington?\n')

            while True:
                city = input('Please enter your city selection (Chicago, New York City, or Washington): \n').lower()
                if city not in CITY_DATA:
                    print('\nSorry, that is not an acceptable response. Please try again\n')
                else:
                    break
            print('\nExcellent! You selected {}! \n'.format(city.title()))
            # TO DO: get user input for month (all, january, february, ... , june)

            print('Now, if you would like to, you can view data for only a specific month.\n')
            while True:
                month = input('Please select a month from January to June or enter "all" to view data from entire range of months: \n').lower()
                if month not in month_input:
                    print('\nSorry, that is not an acceptable response. Please try again\n')
                else:
                    break
            print('\nAwesome! You selected to view data from {} (months). \n'.format(month.title()))

            # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

            print('Now, would you like to filter by a specific day of the week?\n')
            while True:
                day = input('Please select the day you would like to view data from or enter "all": \n').lower()
                if day not in day_input:
                    print('\nSorry, that is not an acceptable response. Please try again\n')
                else:
                    break

            print('\nNow, this is exciting!\n')
            print('We are about to look at data from {} for {} (months) for {} (days)!'.format(city.title(), month.title(), day.title()))

            print('-'*40)
            return city, month, day
        else:

            break



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
            for month, january = 1
            for day, monday = 0
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)

        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Finds the mode of the month and/or day input, calculates data related to the ride starting hour, converts the start time data to a more easily read datatype, and prints the appropriate string based on user input.

    Arguments:
        df - data filtered by user selection of which city and what month(s)/day(s) to examine
        (int) month - integer which represents the month selected if input was not 'all' months
        (int) day - integer which represents the day selected if input was not 'all' days

    Returns:
        prints a string formatted to display the most popular month and most popular day (if a specific month/day was not selected) and provides the most common ride starting hour
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode().item()
    popular_month = calendar.month_name[popular_month]

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode().item()
    popular_day = calendar.day_name[popular_day]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_starting_hour = df['hour']

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode().item()
    popular_hour = datetime.time(popular_hour).strftime('%I:00 %p')

    if day == 'all' and month == 'all':
        print('{} is the most common month, {} is the most common day of the week, and {} is the most common time people are traveling!'.format(popular_month, popular_day, popular_hour))
    elif day != 'all' and month == 'all':
        print('{} is the most common month, {} is day of the week selected for the filter, and {} is the most common time people are traveling!'.format(popular_month, popular_day, popular_hour))
    elif month != 'all' and day == 'all':
        print('{} is the month selected for the filter, {} is the most common day of the week, and {} is the most common time people are traveling!'.format(popular_month, popular_day, popular_hour))
    else:
        print('{} is the month selected for the filter, {} is the day of the week selected for the filter, and {} is the most common time people are traveling!'.format(popular_month, popular_day, popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Arguments:
        (df) - data filtered by user selection of which city and what month(s)/day(s) to examine

    Returns:
        prints a string formatted to display the most popular starting station, the most popular ending station, and the most popular start/end combination based on the user input

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip_tuple = df.groupby(['Start Station', 'End Station']).size().idxmax()
    popular_trip = popular_trip_tuple[0] + ' to ' + popular_trip_tuple[1]


    print('{} is the most popular starting station, {} is the most popular ending station, and {} is the most popular trip.'.format(popular_start, popular_end, popular_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Arguments:
        (df) - data filtered by user selection of which city and what month(s)/day(s) to examine

    Returns:
        prints a string formatted to display the total time traveled and the average trip duration during the user selected month/day.

        The total travel time and average travel time were converted into more accessible data.

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (df['Trip Duration'].sum() / 60 / 60 /24).round(decimals=2)

    # TO DO: display mean travel time
    avg_travel_time = (df['Trip Duration'].mean() / 60).round(decimals=2)

    print('The total travel time for this month and day combination was {} days and the average trip took {} minutes'.format(total_travel_time, avg_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users.

    Arguments:
        (df) - data filtered by user selection of which city and what month(s)/day(s) to examine
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        prints a statement provided the count of user types for all cities, gender statistic (if the city selected was not 'washington'), and some dob statistics (again, if the city selected was not 'washington')
        - if user input was 'washington' the second part of the printed statement apologizes that 'washington' does not have gender nor dob data

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()

    if city != 'washington' and city != 'washington dc' and city != 'washington d.c.' and city != 'dc' and city != 'd.c.':
        # TO DO: Display counts of gender
        user_gender_count = df['Gender'].value_counts()

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_dob_year = int(df['Birth Year'].min())
        most_recent_dob_year = int(df['Birth Year'].max())
        most_frequent_dob_year = int(df['Birth Year'].mode()[0])

        print('For trips taken in {} during the timeframe selected ({} for the month filter and {} for the day filter) there were many different types of riders!\n'.format(city.title(), month.title(), day.title()))

        print('First, the types of users:\n{}\n'.format(user_type_count))

        print('Now, the genders of all the users:\n{}\n'.format(user_gender_count))

        print('Lastly, the earliest birth year was {}, the most recent birth year was {}, and the most frequent birth year was {}'.format(earliest_dob_year, most_recent_dob_year, most_frequent_dob_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('For trips taken in {} during the timeframe selected ({} for the month filter and {} for the day filter) there were many different types of riders!\n'.format(city.title(), month.title(), day.title()))

        print('In {}, these were the user types:\n{}\n'.format(city.title(), user_type_count))

        print("Sorry, there are no gender or DOB statistics for {}'s bikeshare program!".format(city.title()))

def display_results_5(df):
    """Provides user data 5 users at a time until no more data is requested

    Arguments:
        (df) - data filtered by user selection of which city and what month(s)/day(s) to examine

    Returns:
        prints 5 lines of a the df at a time based on user input

    """

    print('\nPrinting User Info...\n')
    start_time = time.time()

    print('\nNow, would you like to see the individual user statistics for the filters you selected?')

    yes_or_no = ('yes', 'no')

    print('\nI can print the user data 5 lines at a time!')
    print('\nTwo notes about the results: \n- 0 will mean Monday and 6 will mean Sunday for the "day" column\n- hour is from 0(midnight) to 23(11pm) for the "hour" column)')
    while True:
        print_data = input('\nPlease enter yes to view the data or no to stop viewing the results: \n').lower()

        if print_data not in yes_or_no:
            print('\nSorry, that is not an acceptable response. Please try again')
        else:
            break

    if print_data in ('yes'):
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            while True:
                more_data = input('\nWould you like to see more data? Please enter yes or no: \n').lower()

                if more_data not in yes_or_no:
                    print('\nSorry, that is not an acceptable response. Please try again')
                else:
                    break
            if more_data not in ('yes'):
                print('\nOkay, we are done with this data selection!')
                break

    else:
        print('Okay, we are done with this data selection!')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        start = say_hello()
        if start != 'yes':
            print('\nSorry you do not want to explore any data! Have a nice day!')
            break
            #Ends program incase the user changed their mind!
        city, month, day = get_filters(start)
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city, month, day)

        display_results_5(df)

        yes_or_no = ('yes', 'no')
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()

            if restart not in yes_or_no:
                print('\nSorry, that is not an acceptable response. Please try again')
            else:
                break
        if restart != 'yes':
            print('\nThanks for looking at bikeshare data with me today!')
            break
            #Ends the program without an error and says thanks the user!

"""Websites such as Stackoverflow, Udacity Forums, Python Libraries, and other reference/discussion forums were used to trouble shoot problems, but no solutions were copied verbatim. All of this code was provided by Udacity at the start of the project or written by me with a lot of trial and error (generally after hours of reading about similar solutions or new techniques and adapting them to my line of thinking). Nothing was intentionally copied."""

if __name__ == "__main__":
	main()
