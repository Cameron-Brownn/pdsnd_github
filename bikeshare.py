import time
import numpy as np
import pandas as pd
from scipy.stats import mode

# Dictionary containing file paths for different cities datasets
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Function to get user inputs for city, month, and day filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city and validate
    while True:
        city = input("Please select a city, Chicago, New York City or Washington.")
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print("Please select a valid city.")

    # Get user input for month and validate
    while True:
        month = input(f"Please select a month to analyze {city.title()} bikeshare data for.\nChoose between January to June, or type 'all':")
        month = month.lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Please enter a month between January and June. Or select all.")
        else:
            break

    # Get user input for day and validate
    while True:
        day = input("Please select a day of week to analyze, or type all.")
        day = day.lower()
        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"):
            print("Please select a valid day.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day

# Function to load data based on city, month, and day filters
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

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from 'Start Time'
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    print("Columns in the dataset:", df.columns)

    # Filter data based on user inputs for month and day
    if month != 'all':
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day = days.index(day)
        df = df[df['Day of Week'] == day]

    return df

# Function to display statistics on the most frequent times of travel
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month, day of the week, and start hour
    if not df['Month'].empty:
        common_month = df['Month'].mode()[0]
        print(f"The most common month is: {common_month}")
    else:
        print("No data available for the most common month.")

    if not df['Day of Week'].empty:
        common_day = df['Day of Week'].mode()
        if not common_day.empty:
            print(f"The most common day of the week is: {common_day[0]}")
        else:
            print("No data available for the most common day of the week.")
    else:
        print("The 'Day of Week' column is empty.")

    if not df['Hour'].empty:
        common_hour = df['Hour'].mode()[0]
        print(f"The most common start hour is: {common_hour}")
    else:
        print("No data available for the most common start hour.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display statistics on the most popular stations and trips
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate the most common start station
    if not df['Start Station'].empty:
        most_common_start_station = df['Start Station'].value_counts().idxmax()
        print(f"The most common start station is: {most_common_start_station}")
    else:
        print("No data available for the most common start station.")

    # Calculate the most common end station
    if not df['End Station'].empty:
        most_common_end_station = df['End Station'].value_counts().idxmax()
        print(f"The most common end station is: {most_common_end_station}")
    else:
        print("No data available for the most common end station.")

    # Calculate the most frequent combination of start and end stations for a trip
    if not df['Start Station'].empty and not df['End Station'].empty:
        df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']
        station_combination = df['Station Combination'].value_counts().idxmax()
        print(f"The most frequent combination of start station and end station trip is: {station_combination}")
    else:
        print("No data available for the most frequent combination of start station and end station trip.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display statistics on trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the total travel time and mean travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is:", round(total_travel_time / 60), "hours.")

    mean_travel_time = df['Trip Duration'].dropna().mean()
    if not np.isnan(mean_travel_time):
        print("The mean travel time is:", round(mean_travel_time / 60), "hours.")
    else:
        print("No data available to calculate mean travel time.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display statistics on bikeshare users
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_type_counts = df['User Type'].value_counts().to_frame().reset_index()
        print("User Type Counts:")
        print(user_type_counts, '\n')
    else:
        print("User Type information not available for this city.")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().to_frame().reset_index()
        print("Gender Counts:")
        print(gender_counts, '\n')
    else:
        print("Gender information not available for this city.")

    # Calculate and display statistics for birth year
    try:
        birthyear = df['Birth Year'].values
        birthyear_unique = np.unique(birthyear[~np.isnan(birthyear)])
        recent_birthyear = birthyear_unique.max()
        earliest_birthyear = birthyear_unique.min()
        common_birthyear = mode(birthyear_unique)[0]
        print(f"The most recent birth year is: {recent_birthyear}, the earliest birth year is: {earliest_birthyear}, and the most common birth year is {common_birthyear}.")

    except KeyError:
        print("Birth Year information not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display raw data 5 rows at a time
def display_data(df):
    """Displays raw data 5 rows at a time."""
    print('\nDisplaying Data...\n')

    start_index = 0
    chunk_size = 5
    while True:
        display = input("Would you like to see the first 5 rows of data? Enter yes or no: ").lower()
        if display != 'yes':
            break

        print(df.iloc[start_index:start_index+chunk_size])
        start_index += chunk_size

        display_more = input("Would you like to see the next 5 rows? Enter yes or no: ").lower()
        if display_more != 'yes':
            break

# Function to control program execution
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()