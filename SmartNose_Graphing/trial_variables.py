import itertools

#variables
distances = ["0 ft", "1.5 ft", "3 ft"]
heater_prof = ["heater config 1"]
humidity = ["low humidity", "high humidity"]
technique = ["wipe", "spray"]
solutions = ["bleach", "multipurpose cleaner", "stale air"]
room_type = ["closed room", "open room"]

a = [distances, heater_prof, humidity, technique, solutions, room_type]

trial_list = list(itertools.product(*a))
time_to_complete = len(trial_list) / 6

print("Total Number of Trials: ", len(trial_list))
print(time_to_complete)

for trial in trial_list:
    print(trial)