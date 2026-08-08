# ⏰ CLI Clock

A minimal, dependency-free command-line timer and stopwatch for Linux.

## Features

- **Timer** with pause/resume (`P`) and system notifications
- **Stopwatch** with lap (`L`), pause/resume (`P`), and stop (`X`)
- Current time display
- Zero dependencies (stdlib only)
- Non-blocking key input via `termios`

## Installation

```bash
git clone https://github.com/<your-username>/cli-clock.git
cd cli-clock
chmod +x cli_clock.py

# Optional: add to PATH
sudo ln -s "$(pwd)/cli_clock.py" /usr/local/bin/cli_clock
