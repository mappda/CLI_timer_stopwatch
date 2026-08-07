import time
import sys

def timer(amount, unit):
    pass
    

def stopwatch():
    pass

def display():
    pass

def notify():
    pass

def print_help():
    print("""Usage: cli_clock <command> [options]

Commands:
  timer <value> <unit>   Countdown timer
                         Units: -s (seconds), -m (minutes), -h (hours)
  stopwatch              Start stopwatch (Ctrl+C to stop)
  --help                 Show this help message

Examples:
  cli_clock timer 90 -s      # 90 seconds
  cli_clock timer 5 -m       # 5 minutes
  cli_clock timer 2 -h       # 2 hours
  cli_clock stopwatch""")
    sys.exit(0)    

def main():
    pass
if __name__=="__main__"
    try:
        main()
    except BaseException as error:
        print('An error occurred: {}'.format(error))
