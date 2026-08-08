import time
import sys

#value=['1h','30m','90s']

value=sys.argv[2:]

def timer(value):
    # 1. Clean the input (remove spaces)
    value_str="".join(value)
    print(value_str)
    parts = value_str.split()
    total_sec = 0
    
    # 2. Parse the components
    for part in parts:
        # Extract number and unit using a more robust method
        # This handles "10m", "10 m", "10min" (if you want)
        amount_str = ""
        unit_char = ""
        for i, char in enumerate(part):
            if char.isdigit() or char == '.':
                amount_str += char
            else:
                unit_char = char
                break
        
        try:
            val = int(amount_str)
            if unit_char == 'h': total_sec += val * 3600
            elif unit_char == 'm': total_sec += val * 60
            elif unit_char == 's': total_sec += val
            else: raise ValueError("Invalid Unit")
        except:
            print(f"Error: Invalid input '{part}'. Use h, m, or s.")
            sys.exit(1)

    if total_sec <= 0:
        print("Please enter a valid duration (e.g., 10m).")
        return

    # 3. Countdown Logic
    emojis = ['🕛', '🕘', '🕕', '🕒']
    print(f"⏰ Starting timer for {total_sec} seconds.")
    
    # Use a while loop with time.time() to prevent "drift"
    start_time = time.time()
    end_time = start_time + total_sec

    while time.time() < end_time:
        remaining = int(end_time - time.time())
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        
        # \r moves the cursor to the start of the line
        print(f"\r{emojis[remaining % 4]} {h:02}:{m:02}:{s:02}", end="", flush=True)
        time.sleep(1)

    print("\n🔔 Time's up!")

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
