import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}

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
    city = ''
    month = ''
    day = ''
    cities = ['chicago', 'new york', 'washington']
    while city not in cities:
        city = input('Please enter a city from the following: Chicago, New York or Washington?: ').lower()
    # get user input for month (all, january, february, ... , june)
    timeFilters = ['month', 'day', 'both', 'none']
    timeFilter = ''
    numDay = 0
    day = ''
    while timeFilter not in timeFilters:
        timeFilter = input('Would you like to filter the data by month, day, both or not at all? Type none for no time filter: ').lower()
    if timeFilter != 'none':
        if timeFilter in ('month', 'both'):
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            while month not in months:
                month = input('Which month? January - June: ').lower()
        # get user input for day of week (all, monday, tuesday, ... sunday)
        if timeFilter in ('both', 'day'):
            while (numDay < 1) or (numDay > 7):
                numDay = int(input('Which day? Please type your response as an integer (eg., 1= Sunday): '))
            daysOfWeek = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
            if numDay in daysOfWeek:
                day = daysOfWeek[numDay]
    print('-'*40)
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
    print("City, month, day : ", city, month, day)
    fileName = ''
    fileName = CITY_DATA[city]
    df = pd.read_csv(fileName)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df['Start_Time'] = pd.to_datetime(df.Start_Time)
    if month != '':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        monthNum = months.index(month) + 1
        df = df.loc[df.Start_Time.dt.month == monthNum]
    if day != '':
        df = df.loc[df.Start_Time.dt.weekday_name == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_monthNum = df.Start_Time.dt.month.mode().iloc[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[popular_monthNum - 1]

    df_month = df.loc[df.Start_Time.dt.month == popular_monthNum]
    month_count = df_month['Start_Time'].count()
    print("Most popular month: ", popular_month, "   Total Count: ", month_count)

    # display the most common day of week
    popular_weekday = df.Start_Time.dt.weekday_name.mode().iloc[0]
    weekday_count = df.loc[df.Start_Time.dt.weekday_name == popular_weekday]['Start_Time'].count()
    print("Most popular weekday: ", popular_weekday, "   Total Count: ", weekday_count)

    # display the most common start hour
    popular_hour = df.Start_Time.dt.hour.mode().iloc[0]
    hour_count = df.loc[df.Start_Time.dt.hour == popular_hour]['Start_Time'].count()
    print("Most popular start hour: ", popular_hour, "   Total Count: ", hour_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startStation = df.Start_Station.mode().iloc[0]
    startStation_count = df.loc[df.Start_Station == popular_startStation]['Start_Station'].count()
    print("Most popular start station: ", popular_startStation, "   Total Count: ", startStation_count)

    # display most commonly used end station
    popular_endStation = df.End_Station.mode().iloc[0]
    endStation_count = df.loc[df.End_Station == popular_endStation]['End_Station'].count()
    print("Most popular end station : ", popular_endStation, "   Total Count: ", endStation_count)

    # display most frequent combination of start station and end station trip
    print("\n ------Most popular combination of start station and end station -------")
    df_grouped = df.groupby(["Start_Station", "End_Station"]).size().reset_index(name='count')
    df_grouped = df_grouped.sort_values(by='count', ascending=False)
    print("Start Station: ", df_grouped['Start_Station'].iloc[0], "->   End Station: ", df_grouped['End_Station'].iloc[0],
                                "   Count : ", df_grouped['count'].iloc[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # find total travel time
    total_time = df['Trip_Duration'].sum()

    # find mean travel time
    mean_time = df['Trip_Duration'].mean()

    # find average travel time
    total_count = df['Trip_Duration'].count()
    avg_time = total_time/total_count

    # Display total, average and mean trip duration time
    print("Total Duration: ", total_time, " Average Duration: ", avg_time, "   Mean Duration : ", mean_time, "  Total number of trips: ", df['Trip_Duration'].count())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_userType = df.groupby(["User_Type"]).size().reset_index(name='count')
    df_userType = df_userType.sort_values(by='count', ascending=False)
    for index, row in df_userType.iterrows():
        print("User Type:", df_userType['User_Type'].iloc[index], " Count: ", df_userType['count'].iloc[index])

    # Display counts of gender
    if 'Gender' in df.columns:
        df_genderType = df.groupby(["Gender"]).size().reset_index(name='count')
        df_genderType = df_genderType.sort_values(by='count', ascending=False)
        for index, row in df_genderType.iterrows():
            print("Gender Type:", df_genderType['Gender'].iloc[index], " Count: ", df_genderType['count'].iloc[index])
    else:
        print("No gender data to share")

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df.columns:
        earliest_year = df['Birth_Year'].min().astype(int)
        print("Earliest Year: ", str(earliest_year))

        recent_year = df['Birth_Year'].max().astype(int)
        print("Recent Year: ", str(recent_year))

        df_birthYear = df.groupby(["Birth_Year"]).size().reset_index(name='count')
        df_birthYear = df_birthYear.sort_values(by='count', ascending=False)
        print("Most common birth year:", df_birthYear['Birth_Year'].iloc[0].astype(int), " Count: ", df_birthYear['count'].iloc[0])
    else:
        print("No Birth Year data to share")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if (len(df) == 0):
            print("No data available for your data filter")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
