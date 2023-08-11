from datetime import datetime
from colorama import Fore
from colorama import Style

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

date_format = "%a, %d %b %Y"

def log(type, message):

    switcher={
        'info': f'{Fore.YELLOW}[INFO] {time_log} {message} {Style.RESET_ALL}',
        'info_m': f'{Fore.MAGENTA}[INFO] {time_log} {message} {Style.RESET_ALL}',
        'error': f'{Fore.RED}[ERROR] {time_log} {message} {Style.RESET_ALL}',
        'warning': f'{Fore.YELLOW}[WARNING] {time_log} {message} {Style.RESET_ALL}',
        'client': f'{Fore.GREEN}[INFO] {time_log} {message} {Style.RESET_ALL}',
    }

    print(switcher.get(type,"Invalid type"))


def savelog(type, message):
    now = datetime.now()
    time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

    switcher={
        'info': f'[INFO] {time_log} {message}',
        'error': f'[ERROR] {time_log} {message}',
        'warning': f'[WARNING] {time_log} {message}',
    }

    with open('logs.txt', 'a') as f:
        f.write(switcher.get(type, "Invalid type") + '\n')