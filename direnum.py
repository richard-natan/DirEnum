import requests
import argparse
import threading
import numpy
import signal
import sys

stop_event = threading.Event()

def printBanner():
    print('\n\n')
    print('▓█████▄  ██▓ ██▀███  ▓█████  ███▄    █  █    ██  ███▄ ▄███▓')
    print('▒██▀ ██▌▓██▒▓██ ▒ ██▒▓█   ▀  ██ ▀█   █  ██  ▓██▒▓██▒▀█▀ ██▒')
    print('░██   █▌▒██▒▓██ ░▄█ ▒▒███   ▓██  ▀█ ██▒▓██  ▒██░▓██    ▓██░')
    print('░▓█▄   ▌░██░▒██▀▀█▄  ▒▓█  ▄ ▓██▒  ▐▌██▒▓▓█  ░██░▒██    ▒██ ')
    print('░▒████▓ ░██░░██▓ ▒██▒░▒████▒▒██░   ▓██░▒▒█████▓ ▒██▒   ░██▒')
    print(' ▒▒▓  ▒ ░▓  ░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░')
    print(' ░ ▒  ▒  ▒ ░  ░▒ ░ ▒░ ░ ░  ░░ ░░   ░ ▒░░░▒░ ░ ░ ░  ░      ░')
    print(' ░ ░  ░  ▒ ░  ░░   ░    ░      ░   ░ ░  ░░░ ░ ░ ░      ░   ')
    print('   ░     ░     ░        ░  ░         ░    ░            ░   ')
    print(' ░                                                          ')
    print('\n\nmade by: RiccK')
    print('\n\n')

# Send the request
def sendRequest(url):
    try:
        request = requests.get(url)
        if request.status_code != 404:
            print(f"{url.strip()} ------- Status: {request.status_code}")
    except:
        print(f"Cannot connect to the {url}")

# Each thread prepare request function
def threadFunction(wordlist):
    for line in wordlist:
        if stop_event.is_set(): # Verify if stop flag is set
            break

        sendRequest(url + line.strip())

parser = argparse.ArgumentParser(
    prog="DirEnum",
    usage="Python3 direnum.py -w <wordlist> -u <url>"
)
parser.add_argument("-w", "--wordlist", help="Wordlist file/path", required=True)
parser.add_argument("-u", "--url", help="Target URL (http://target.com/)", required=True)
parser.add_argument("-t", "--threads", type=int, help="Number of threads (default is 5)", default=5)

# Get arguments ready
args = parser.parse_args()
wordlist = args.wordlist
threads = args.threads
url = args.url
if not url.endswith("/"):
    url += "/"


threads_pool = []

# Read file
with open(wordlist, 'r') as file:
   # Create a temp wordlist for split later
    temp_wordlist = []
    for line in file:
        temp_wordlist.append(line.strip())

    # Split wordlist by number of threads 
    splited_array = numpy.array_split(temp_wordlist, threads)

    try:
        printBanner()
        print("="*100)
        print(f"\n\nTARGET: {url}\nWORDLIST: {wordlist}\nTHREADS: {threads}\n\n")
        print("="*100+"\n\n")

        # Create thread, add it to pool threads and start
        for split_array in splited_array:
            new_thread = threading.Thread(target=threadFunction, args=(split_array,))
            threads_pool.append(new_thread)
            new_thread.start()
    
        for thread in threads_pool:
            thread.join()
    except KeyboardInterrupt:
        print("\nExiting...")
        stop_event.set()
        quit()
        sys.exit()
        
