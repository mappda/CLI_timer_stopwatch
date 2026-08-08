import time
import sys
import os
import subprocess
import termios
import tty
import signal


# ─── Raw Terminal Manager ──────────────────────────────────────────────────────

class RawTerminal:
    """Context manager for non-blocking key input on Linux."""
    
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
        self.active = False

    def __enter__(self):
        if os.isatty(self.fd):
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)  # cbreak > raw: keeps Ctrl+C working
            self.active = True
        return self

    def __exit__(self, *args):
        if self.active and self.old_settings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self.active = False

    def get_key(self):
        """Non-blocking single key read. Returns lowercase char or None."""
        if not self.active:
            return None
        try:
            import select
            if select.select([sys.stdin], [], [], 0)[0]:
                ch = sys.stdin.read(1)
                # Handle escape sequences (arrow keys etc.) by consuming them
                if ch == '\x1b':
                    select.select([sys.stdin], [], [], 0.01)
                    while select.select([sys.stdin], [], [], 0)[0]:
                        sys.stdin.read(1)
                    return None
                return ch.lower()
        except Exception:
            pass
        return None


# ─── Utilities ─────────────────────────────────────────────────────────────────

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def notify(message="Timer Finished!"):
    try:
        subprocess.run(["notify-send", "CLI Clock", message],
                       check=False, capture_output=True)
    except FileNotFoundError:
        pass


def parse_time_args(args):
    valid_units = {'h': 3600, 'm': 60, 's': 1}
    total = 0.0
    for arg in args:
        arg = arg.strip().lower()
        idx = 0
        while idx < len(arg) and (arg[idx].isdigit() or arg[idx] == '.'):
            idx += 1
        amount_str, unit_str = arg[:idx], arg[idx:]
        if not amount_str or unit_str not in valid_units:
            return None
        try:
            total += float(amount_str) * valid_units[unit_str]
        except ValueError:
            return None
    return int(total) if total > 0 else None


# ─── Timer ─────────────────────────────────────────────────────────────────────

def timer(args, term):
    total_sec = parse_time_args(args)
    if total_sec is None:
        print_help()
        sys.exit(1)

    emojis = ['🕛', '🕘', '🕕', '🕒']
    end_time = time.time() + total_sec
    paused_remaining = None

    print(f"\n⏰ Timer: {format_time(total_sec)}")
    print("   [P] Pause/Resume  [Ctrl+C] Cancel\n")

    try:
        while True:
            key = term.get_key()

            if key == 'p':
                if paused_remaining is None:
                    # PAUSE
                    paused_remaining = max(0, int(end_time - time.time()))
                    print(f"\r⏸  PAUSED {format_time(paused_remaining)} \033[K", end="", flush=True)
                    # Wait for resume
                    while True:
                        k = term.get_key()
                        if k == 'p':
                            break
                        if k == '\x03':  # Ctrl+C
                            raise KeyboardInterrupt
                        time.sleep(0.05)
                    # RESUME
                    end_time = time.time() + paused_remaining
                    paused_remaining = None
                    continue

            if paused_remaining is not None:
                remaining = paused_remaining
            else:
                remaining = max(0, int(end_time - time.time()))

            h, m, s = remaining // 3600, (remaining % 3600) // 60, remaining % 60
            print(f"\r{emojis[remaining % 4]} {h:02d}:{m:02d}:{s:02d} \033[K", end="", flush=True)

            if remaining <= 0 and paused_remaining is None:
                break

            time.sleep(0.25)

        print(f"\r✅ 00:00:00 Done! \033[K")
        print("\a", end="", flush=True)
        notify()

    except KeyboardInterrupt:
        print("\n\n⏹ Timer cancelled.")


# ─── Stopwatch ─────────────────────────────────────────────────────────────────

def stopwatch(term):
    print("\n⏱ Stopwatch")
    print("   [L] Lap  [P] Pause/Resume  [X] Stop  [Ctrl+C] Quit\n")

    start_time = time.time()
    elapsed_before_pause = 0.0
    paused = False
    laps = []
    lap_start = 0.0

    try:
        while True:
            key = term.get_key()

            if key == 'x':
                final = elapsed_before_pause + (0 if paused else time.time() - start_time)
                print(f"\r⏱ Stopped: {format_time(int(final))} \033[K")
                if laps:
                    print("\n  Laps:")
                    for i, lt in enumerate(laps, 1):
                        print(f"    {i:3d}. {format_time(lt)}")
                break

            if key == 'p':
                if not paused:
                    elapsed_before_pause += time.time() - start_time
                    paused = True
                    print(f"\r⏸  PAUSED {format_time(int(elapsed_before_pause))} \033[K", end="", flush=True)
                else:
                    start_time = time.time()
                    paused = False

            if key == 'l' and not paused:
                current = elapsed_before_pause + (time.time() - start_time)
                lap_time = current - lap_start
                laps.append(lap_time)
                lap_start = current
                print(f"\r  🏁 Lap {len(laps)}: {format_time(int(lap_time))} \033[K")

            if not paused:
                elapsed = elapsed_before_pause + (time.time() - start_time)
                print(f"\r  ⏱ {format_time(int(elapsed))} \033[K", end="", flush=True)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n\n⏹ Stopwatch quit.")


# ─── Display & Help ────────────────────────────────────────────────────────────

def display():
    print(f"\n🕰 {time.strftime('%Y-%m-%d %H:%M:%S')}\n")


def print_help():
    print("""
CLI Clock — Minimal & Functional

USAGE:
  cli_clock timer <value><unit> [...]   Countdown timer
  cli_clock stopwatch                   Stopwatch with laps
  cli_clock display                     Show current time
  cli_clock help                        Show this message

TIMER CONTROLS:     [P] Pause/Resume   [Ctrl+C] Cancel
STOPWATCH CONTROLS: [L] Lap  [P] Pause/Resume  [X] Stop  [Ctrl+C] Quit

EXAMPLES:
  cli_clock timer 1h 30m
  cli_clock timer 90s
  cli_clock timer 1h 5m 30s

UNITS: h (hours), m (minutes), s (seconds)
""".strip())


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    # Commands that don't need raw terminal
    simple_cmds = {'display', 'help', '-h', '--help'}
    if cmd in simple_cmds:
        {'display': display, 'help': print_help,
         '-h': print_help, '--help': print_help}[cmd]()
        return

    if cmd not in ('timer', 'stopwatch'):
        print(f"Unknown command: '{cmd}'\n")
        print_help()
        sys.exit(1)

    # Interactive commands: enter raw mode ONCE for entire session
    with RawTerminal() as term:
        if cmd == 'timer':
            timer(args, term)
        elif cmd == 'stopwatch':
            stopwatch(term)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("")
