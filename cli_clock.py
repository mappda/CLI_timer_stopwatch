import time
import sys

#value=['1h','30m','90s']

value=sys.argv[2:]

def timer(value):
    hrs=mins=secs=0
    amount=[i[:len(i)-1] for i in value]
    unit=[i[len(i)-1:] for i in value]
    try:
        amount=[int(i) for i in amount]
    except Exception as error:
        print("Usage: timer <value><unit>.\nExample: 10m -> 10 minutes\n         1h 10m 30s -> 1 hour, 10 minutes and 30 seconds.\nsee cli_clock -help.")
        sys.exit(1)
    if False in [False for i in unit if not(i in ['h','m','s'])]:
        print("Usage: timer <value><unit>.\nExample: 10m -> 10 minutes\n         1h 10m 30s -> 1 hour, 10 minutes and 30 seconds.\nsee cli_clock -help.")
        sys.exit(1)
    
    if 'h' in unit: hrs=amount[unit.index('h')]
    if 'm' in unit: mins=amount[unit.index('m')]
    if 's' in unit: secs=amount[unit.index('s')]

    total_sec=(hrs*3600)+(mins*60)+secs
    seconds=total_sec%60
    minutes=int((total_sec/60))%60
    hours=int((total_sec/3600))
    print(f"⏰ Starting timer for {hours:02}:{minutes:02}:{seconds:02}\n")    
    emojis=['🕛', '🕘', '🕕', '🕒']
    for sec in range(total_sec,0,-1):
        seconds=sec%60
        minutes=int((sec/60))%60
        hours=int((sec/3600))
        print(f"\r{emojis[sec%4]} {hours:02}:{minutes:02}:{seconds:02}", flush=True, end="")
        time.sleep(1)
    print()
timer(value)

def stopwatch():
    pass

def display():
    pass

def notify():
    pass

def print_help():
    pass
    
def main():
    pass


if __name__=="__main__":
    try:
        main()
    except BaseException as error:
        print('An error occurred: {}'.format(error))
