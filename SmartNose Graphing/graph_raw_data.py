import sqlite3
import matplotlib.pyplot as plt

variables = ['humidity', 'raw_humidity']
databases = ['local_database_sam.db', 'local_database_sukuna.db']


datasets = []
for db in databases:
    print(databases.index(db))



for db in databases:
    conn = sqlite3.connect('local_database.db')
    cursor = conn.cursor()

    # Execute a query to retrieve data from the table
    cursor.execute('SELECT raw_humidity, humidity FROM StudyAreaBME12NormalAirToLysol')
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    rate = 5    #every x samples gets stored

    # Unpack the data into separate lists
    column1_data, column2_data = zip(*data)

    sampled_column1_data = column1_data[::rate]
    sampled_column2_data = column2_data[::rate]

    print(len(sampled_column1_data))
    print(len(sampled_column2_data))


    # Create a line plot
    plt.plot( sampled_column1_data, label='Raw')
    plt.plot( sampled_column2_data, label='BSEC Adjusted')

    # Add labels and a legend
    plt.xlabel('Sample', fontsize=14)
    plt.ylabel('Raw Humidity', fontsize=14)
    plt.title('Humidity', fontsize=18)
    plt.legend()

    # Show the plot
    plt.show()

print(datasets)