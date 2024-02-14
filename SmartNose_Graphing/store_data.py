from bme68x import BME68X
import bme68xConstants as cnst
import bsecConstants as bsec
from datetime import datetime as dt
import json
import sqlite3

def read_conf(path: str):
    with open(path, 'rb') as conf_file:
        conf = [int.from_bytes(bytes([b]), 'little') for b in conf_file.read()]
        conf = conf[4:]
    return conf
    
def create_table(cursor, table_name):
    # Define your table schema (adjust column names and data types as needed)
    table_creation_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            sample_nr INTEGER,
            timestamp TEXT,
            raw_temperature REAL,
            raw_pressure REAL,
            raw_humidity REAL,
            raw_gas REAL,
            iaq REAL,
            iaq_accuracy INTEGER,
            static_iaq REAL,
            static_iaq_accuracy INTEGER,
            co2_equivalent REAL,
            co2_accuracy INTEGER,
            breath_voc_equivalent REAL,
            breath_voc_accuracy INTEGER,
            stabilization_status INTEGER,
            run_in_status INTEGER,
            temperature REAL,
            humidity REAL,
            comp_gas_value REAL,
            comp_gas_accuracy INTEGER,
            gas_percentage REAL,
            gas_percentage_accuracy INTEGER,
            gas_estimate_1 REAL,
            gas_estimate_1_accuracy INTEGER,
            gas_estimate_2 REAL,
            gas_estimate_2_accuracy INTEGER,
            gas_estimate_3 REAL,
            gas_estimate_3_accuracy INTEGER
        )
    '''
    cursor.execute(table_creation_query)

def insert_data(cursor, data):
    # Insert data into the table
    insert_query = f'''
        INSERT INTO distance_test ({', '.join(data.keys())})
        VALUES ({', '.join(['?' for _ in data.values()])})
    '''
    cursor.execute(insert_query, tuple(data.values()))

def send_to_sqlite(entry, table_name):
    # Connect to the SQLite database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('/home/capstone2023/BME688CheeseMeatDetector/local_database.db')
    cursor = conn.cursor()

    # Step 2: Create a table (if it doesn't exist)
    create_table(cursor, table_name)

    # Step 3: Insert data from the JSON into the table
    data_to_insert = entry
    insert_data(cursor, data_to_insert)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
	

def main():
    s = BME68X(cnst.BME68X_I2C_ADDR_HIGH, 0)

    table_name = 'test'

    meat_n_cheese = read_conf('/home/capstone2023/BME688CheeseMeatDetector/bme68x-extension/Algorithms/CheeseVsMeat/2021_08_09_17_10_bsec_NormalAi_Meat_Cheese_2_0_6_1.config')
    
    meat_n_cheese_ramblers = read_conf('/home/capstone2023/BME688CheeseMeatDetector/bme68x-extension/Algorithms/MeatOrCheeseOrAirRamblersV2/2023_11_08_22_11_MeatorCheeseorAirv2_HP-354_RDC-5-10.config')
    
    default_conf = read_conf('/home/capstone2023/BME688CheeseMeatDetector/bme68x-extension/BSEC_2.0.6.1_Generic_Release_04302021/config/bsec_sel_iaq_33v_4d/2021_04_29_02_51_bsec_h2s_nonh2s_2_0_6_1 .config')

    air_meat_cheese = read_conf('/home/capstone2023/BME688CheeseMeatDetector/bme68x-extension/Algorithms/AirMeatCheese/2021_09_27_19_24_bsec_NormalAi_Meat_Cheese_2_0_6_1.config')

    # print(f'SET BSEC CONF {s.set_bsec_conf(meat_n_cheese)}')
    print(f'SET BSEC CONF {s.set_bsec_conf(meat_n_cheese_ramblers)}')
    # print(f'SET BSEC CONF {s.set_bsec_conf(air_meat_cheese)}')
    # print(f'SET BSEC CONF DEFAULT SELECTIVITY {s.set_bsec_conf(default_conf)}')

    BSEC_SAMPLE_RATE_HIGH_PERFORMANCE = 0.055556
    BSEC_SAMPLE_RATE_LP = 0.33333

    print(f'SUBSCRIBE STANDARD OUTPUTS {s.set_sample_rate(BSEC_SAMPLE_RATE_HIGH_PERFORMANCE)}')
    print(f'SUBSCRIBE GAS ESTIMATES {s.subscribe_gas_estimates(3)}')

                                            # enable(int), temp_profile, duration_profile(in milli), operation_mode 
    print(f'SET HEATER PROFILE {s.set_heatr_conf(1, [320, 100, 100, 100, 200, 200, 200, 320, 320, 320], [700, 280, 1400, 4200, 700, 700, 700, 700, 700, 700], 2)}')
    # print(f'INIT BME68X {s.init_bme68x()}')
   # [150, 150, 150, 150, 150, 150, 150, 150, 150, 150] Original

    print('\n\nSTARTING MEASUREMENT\n')

    while(True):
        #print(s.get_data())
        try:
            data = s.get_digital_nose_data()
        except Exception as e:
            print(e)
            main()
        if data:
            # for entry in s.get_digital_nose_data():
            entry = data[-1]
            print(dt.now())
            print(f'CHEESE {entry["gas_estimate_1"]}\nMEAT {entry["gas_estimate_2"]}\nNORMAL AIR {entry["gas_estimate_3"]}\n')
            entry["timestamp"] = str(dt.now())
            send_to_sqlite(entry, table_name)
            
            with open('/home/capstone2023/BME688CheeseMeatDetector/data.json', 'w') as file:
                json.dump(entry, file)
			

if __name__ == '__main__':
    main()
