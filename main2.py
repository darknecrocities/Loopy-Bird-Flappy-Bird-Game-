import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime

# Define tasks, dependencies, and durations
tasks = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
durations = [4, 5, 6, 7, 6, 5, 4, 3, 4, 5]
dependencies = {
    "B": "A", "C": "A", "D": "A", "E": ["A", "D"], "F": ["C", "E"],
    "G": ["D", "E"], "H": "E", "I": ["F", "G"], "J": ["H", "I"]
}

# Calculate start times
start_times = {}
end_times = {}
current_time = datetime.datetime.today()

for task in tasks:
    if task not in dependencies:
        start_times[task] = current_time
    else:
        if isinstance(dependencies[task], list):
            start_times[task] = max(end_times[dep] for dep in dependencies[task])
        else:
            start_times[task] = end_times[dependencies[task]]
    end_times[task] = start_times[task] + datetime.timedelta(days=durations[tasks.index(task)])

# Plot Gantt Chart
fig, ax = plt.subplots(figsize=(10, 6))
for i, task in enumerate(reversed(tasks)):
    ax.barh(task, (end_times[task] - start_times[task]).days, left=start_times[task], color='skyblue')

date_format = DateFormatter("%b %d")
ax.xaxis.set_major_formatter(date_format)
plt.xlabel("Date")
plt.ylabel("Tasks")
plt.title("Project Schedule Gantt Chart")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()
