# **_Performance data collector_**

## What the project does
Performance data collector launches a specified _process_ and collects the following data about it:
* CPU usage (percent);
* Memory consumption: Working Set and Private Bytes (for Windows systems) or Resident Set Size and Virtual Memory Size (for Linux systems);
* Number of open handles (for Windows systems) or file descriptors (for Linux systems).

Data collection performs all the time _the process_ is running. 
Path to the executable file for _the process_ and time interval between data collection iterations should be provided. 
Collected data stores on the disk with provided or default file name. The latest consists of _the process_ ID.
The format of the stored data by default is CSV.

## How users can get started with the project
### Call example (for Windows):
```kotlin
python performance_data_collector.py [--p <path_to_executable_file>] [--i <positive_whole_number>]
```

\* for Linux use "python3" instead of "python"

If no arguments are provided, they will be requested.

Optional arguments:
* [--s <store_file_name>] - store data file name. By default it's 'perf_data_collection_pid_{process_id}.csv'
* [--fch <True || False>] - if True the program collects data for child processes that were launched by the main process.

The project was implemented and may be run with Python 3.9.0. Compatibility with previous Python versions has not been verified.
Other requirements are in [requirements.txt](https://github.com/Ms-Anna/Performance_data_collector/blob/master/requirements.txt)
