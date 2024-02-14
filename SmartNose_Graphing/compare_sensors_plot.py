import sqlite3
import matplotlib.pyplot as plt
import numpy as np


def normalize(data):
    data = np.array(data)
    min_val = np.min(data)
    max_val = np.max(data)
    data = (data - min_val) / (max_val - min_val)
    return data


# SPECIFY variable that you want to plot and the name of the trial
var = 'gas_estimate_1'
trial_name = 'StudyAreaBME12NormalAirToLysol'

# SPECIFY paths to each of the databases where the data is stored
database1_path = 'local_database_sam.db'
database2_path = 'local_database_sukuna.db'
databases = [database1_path, database2_path]

all_raw_data = []
all_norm_data = []

for db in databases:
        print(f"Database: {db}")
        print(f"Variable: {var}")

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(f'SELECT {var} FROM {trial_name}')
        data = cursor.fetchall()
        data = np.array(data).flatten()
        # Normalize Data
        norm_data = normalize(data)

        all_raw_data.append(data)
        all_norm_data.append(norm_data)

        conn.close()

        print('data successfully gathered from SQLite\n')


# Set figure size
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot raw data
for i, dataset in enumerate(all_raw_data, start=1):
    time = [x * 2 * 10.78 / 60 for x in range(1, len(dataset) + 1)]
    axs[0].plot(time, dataset, label=f'Smart Nose {i}', linewidth=2)

# Plot normalized data
for i, dataset in enumerate(all_norm_data, start=1):
    time = [x * 2 * 10.78 / 60 for x in range(1, len(dataset) + 1)]
    axs[1].plot(time, dataset, label=f'Smart Nose {i}', linewidth=2)

# Set titles and labels
axs[0].set_title(f'RAW Readings of {var} Over Time', fontsize=14)
axs[1].set_title(f'NORMALIZED Readings of {var} Over Time', fontsize=14)
for ax in axs:
    ax.set_xlabel('Time (mins)', fontsize=12)
    ax.set_ylabel('Prediciton', fontsize=12)
    ax.grid(True)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=10)
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=2)
    ax.fill_between(time, 0, 0.5, color='#89CFF0', alpha=0.3)
    ax.fill_between(time, 0.5, np.max(ax.get_ylim()), color='green', alpha=0.3)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()
