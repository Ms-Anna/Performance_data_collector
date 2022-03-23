import datetime
import platform
import subprocess
import csv
import os
import argparse
from time import sleep, time
import psutil


def write_data(data, file):
    file_exists = os.path.isfile(file)
    with open(file, 'a', newline='') as file_to_write:
        writer = csv.DictWriter(file_to_write, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def log_data(ps_process, file, is_child, add_children):
    data = {'Date and time': datetime.datetime.now().strftime("%Y-%m-%d %X"),
            'PID': ps_process.pid,
            'CPU usage (percent)': ps_process.cpu_percent(interval=0.5) / psutil.cpu_count()}

    if platform.system() == 'Linux':
        data.update({'Resident Set Size': ps_process.memory_info().rss,
                     'Virtual Memory Size': ps_process.memory_info().vms,
                     'Number of open file descriptors': ps_process.num_fds()})
    elif platform.system() == 'Windows':
        data.update({'Working Set': ps_process.memory_info().rss,
                     'Private Bytes': ps_process.memory_info().private,
                     'Number of open handles': ps_process.num_handles()})

    if add_children:
        data['Process is child'] = is_child
        data['Parent process'] = ps_process.ppid() if is_child else '-'

    write_data(data, file)


if __name__ == '__main__':

    if platform.system() not in ['Linux', 'Windows']:
        print('The program doesn\'t work for the current OS.')
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('-program_path', '--p', help='the path to executable file')
    parser.add_argument('-time_interval', '--i', help='time interval (seconds)')
    parser.add_argument('-store_file', '--s', help='the name of store file')
    parser.add_argument('-follow_children', '--fch', action='store_true', help='get child processes data')
    args = parser.parse_args()

    program_path = args.p
    time_interval = args.i
    get_children_data = args.fch

    while not time_interval or (type(time_interval) == str and not time_interval.isdigit()) or int(time_interval) <= 0:
        try:
            time_interval = int(input('Time interval in seconds (positive whole-number):\n'))
        except ValueError as valerr:
            print('ATTENTION: Time interval must be a positive number.')

    while not program_path or os.path.isdir(program_path):
        program_path = input('The path to the executable file:\n')

    try:
        process = subprocess.Popen(os.path.abspath(program_path), stdout=subprocess.DEVNULL)
        process_id = process.pid
        p_process = psutil.Process(process_id)

        # allow to specify the file path/name as additional argument if needed
        store_file = f'{args.s}' if args.s is not None else f'perf_data_collection_pid_{process_id}.csv'

        nexttime = time()
        while process.poll() is None:
            try:
                nexttime += int(time_interval)
                log_data(p_process, store_file, False, get_children_data)
                if get_children_data:
                    for child in p_process.children(recursive=False):
                        log_data(child, store_file, True, get_children_data)
                sleep_time = nexttime - time()
                sleep(sleep_time)
            except KeyboardInterrupt as err:
                print('The program was interrupted.')
                exit(0)
            except ValueError as valerr:
                pass
    except OSError as oserr:
        if oserr.errno == 8:
            print('The file isn\'t executable')
        else:
            print(f'Error occurred:\n{oserr.__repr__()}')
    except Exception as err:
        print(f'Error occurred:\n{err.__repr__()}')
