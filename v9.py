#!/usr/bin/env python3
"""
launcher_decor.py — Neon-themed decorated launcher for Mafia Bot with
compulsory owner id, dependency checks, premium token UX, boot animation,
and updated Surprise flow that asks whether the user joined and re-opens
the link if not.
"""

import os
import re
import subprocess
import sys
import time
import webbrowser
import getpass
from glob import glob
from shutil import get_terminal_size

BOT_FILENAME = "mafia_bot.py"
TEMP_FILENAME = "mafia_bot_temp.py"
_SURPRISE_URL = "https://t.me/techyspyther"

# ----- Neon ANSI palette -----
C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "blink": "\033[5m",
    "neon_pink": "\033[95m",
    "neon_cyan": "\033[96m",
    "neon_green": "\033[92m",
    "neon_yellow": "\033[93m",
    "neon_blue": "\033[94m",
    "neon_white": "\033[97m",
    "neon_red": "\033[91m",
}

CSNV_ART = CSNV_ART = r"""
  ____  ____  __   __  _____ _   _ 
 / ___||  _ \ \ \ / / |_   _| | | |
 \___ \| |_) | \ V /    | | | |_| |
  ___) |  __/   | |     | | |  _  |
 |____/|_|      |_|     |_| |_| |_|

      S P Y T H E R
"""

def neon_print(text, color="neon_white", delay=0.0, end="\n"):
    seq = C.get(color, C["neon_white"]) + text + C["reset"]
    print(seq, end=end)
    if delay and delay > 0:
        time.sleep(delay)

def get_cols():
    try:
        return get_terminal_size().columns
    except Exception:
        return 80

# ----------------------------
# Dependency check / helper
# ----------------------------
def which(cmd):
    try:
        path = subprocess.check_output(["which", cmd], stderr=subprocess.DEVNULL).decode().strip()
        return path if path else None
    except Exception:
        return None

def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        return 0, out
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode() if e.output else ""

def detect_pkg_manager():
    if which("pkg"):
        return "pkg"
    if which("apt"):
        return "apt"
    return None

def check_and_install_dependencies():
    neon_print("Checking system dependencies...", "neon_cyan")
    deps = {
        "termux-open-url": {"found": False, "pkg": "termux-api"},
        "xdg-open": {"found": False, "pkg": "xdg-utils"},
        "am": {"found": False, "pkg": None},
    }
    pkgmgr = detect_pkg_manager()
    if pkgmgr:
        neon_print(f"Package manager found: {pkgmgr}", "neon_green")
    else:
        neon_print("No package manager detected (pkg/apt). Auto-install will be skipped.", "neon_yellow")

    for cmd in deps.keys():
        p = which(cmd)
        if p:
            deps[cmd]["found"] = True
            neon_print(f"{cmd}: found ({p})", "neon_green")
        else:
            deps[cmd]["found"] = False
            neon_print(f"{cmd}: not found", "neon_yellow")

    for cmd, info in deps.items():
        if info["found"]:
            continue
        pkg = info.get("pkg")
        if not pkg:
            neon_print(f"No installer defined for {cmd}. Install manually.", "neon_yellow")
            continue
        if not pkgmgr:
            neon_print(f"Cannot auto-install {pkg}. No package manager.", "neon_red")
            continue
        install_cmd = f"pkg install {pkg} -y" if pkgmgr == "pkg" else f"apt update -y && apt install {pkg} -y"
        neon_print(f"Installing {pkg} ...", "neon_cyan")
        run_cmd(install_cmd)

    neon_print("Dependency check complete.", "neon_cyan")
    time.sleep(0.4)

# ----- Boot animation -----
def boot_animation():
    check_and_install_dependencies()
    cols = get_cols()
    os.system("clear")
    frames = [
        C["neon_cyan"] + "▂▅▇█▓▒░   BOOT SEQUENCE INIT" + C["reset"],
        C["neon_pink"] + "▂▅▇█▓▒░   LOADING NEON MODULES" + C["reset"],
        C["neon_green"] + "▂▅▇█▓▒░   STARTING SERVICES" + C["reset"],
    ]
    for i in range(2):
        for f in frames:
            print(f.center(cols))
            time.sleep(0.12)
            os.system("clear")

    os.system("clear")
    print(C["neon_cyan"] + CSNV_ART + C["reset"])
    neon_print("        " + C["neon_pink"] + C["bold"] + " TELEGRAM AUTOMATION NC " + C["reset"])
    neon_print("        " + C["neon_green"] + "Created by SPYTHER. Version: v9")
    print()
    neon_print(" Tele - https://t.me/techyspyther", "neon_yellow")
    print()

# ----- Menu -----
def neon_header_pulse():
    print(C["neon_cyan"] + CSNV_ART + C["reset"])
    neon_print("        " + C["neon_pink"] + C["bold"] + " TELEGRAM AUTOMATION NC " + C["reset"])
    neon_print("        " + C["neon_green"] + "Created by SPYTHER. Version: v9")
    print()
    neon_print("  Tele - https://t.me/techyspyther", "neon_yellow")
    print()
    neon_print(C["neon_cyan"] + "=" * 52)

def print_menu():
    neon_print("\n" + C["neon_pink"] + C["bold"] + " TELEGRAM NC MENU" + C["reset"])
    neon_print(C["neon_cyan"] + "=" * 52)
    print()
    print("1. " + C["neon_yellow"] + "Command Mode")
    print("2. " + C["neon_blue"] + "Show Bot Status")
    print("3. " + C["neon_red"] + "Stop All Threads")
    print("4. " + C["neon_pink"] + "Exit")
    print("5. " + C["neon_green"] + "Surprise ✨")
    print()

# ----- Owner ID (compulsory) -----
def prompt_owner_id():
    while True:
        owner_id = input(C["neon_pink"] + C["bold"] +
                         "Enter OWNER ID (numeric, required): " +
                         C["reset"]).strip()
        if owner_id.isdigit():
            neon_print(f"Owner ID set to {owner_id}", "neon_green")
            return owner_id
        neon_print("Invalid Owner ID — digits only. Try again.", "neon_red")
        # ----- Token helpers -----
TOKEN_REGEX = re.compile(r"^\d{5,}:[A-Za-z0-9_\-]+$")
def validate_token(tok):
    return bool(TOKEN_REGEX.match(tok.strip()))

def mask_token(tok, show_start=4, show_end=4):
    if len(tok) <= show_start + show_end + 2:
        return tok[:show_start] + "****" + tok[-show_end:]
    return tok[:show_start] + "****" + tok[-show_end:]

SPINNER_CHARS = ["|", "/", "-", "\\"]

def spinner(d=0.6, i=0.07):
    end = time.time() + d
    n = 0
    while time.time() < end:
        print(SPINNER_CHARS[n % 4], end="\b", flush=True)
        time.sleep(i)
        n += 1
    print(" ", end="\b")

# ----- Token input box -----
def draw_input_box(width=60):
    cols = get_cols()
    w = min(width, max(40, cols - 4))
    left = (cols - w) // 2
    print(" " * left + C["neon_blue"] + "┌" + "─" * (w - 2) + "┐" + C["reset"])
    print(" " * left + C["neon_cyan"] + "│" + " TOKEN ENTRY ".center(w - 2) + "│" + C["reset"])
    print(" " * left + "│" + " " * (w - 2) + "│")
    return left, w

def read_tokens_interactively():
    neon_print("", "neon_white")
    left, w = draw_input_box()
    neon_print(" " * left + "✦ Enter tokens; 'q' to finish", "neon_yellow")
    masked = input(C["neon_pink"] + "Mask tokens? (y/N): " + C["reset"]).strip().lower() == "y"

    tokens = []
    idx = 1
    while True:
        prompt = f"✦ Token {idx} → "
        if masked:
            try:
                entry = getpass.getpass(C["neon_pink"] + prompt + C["reset"])
            except Exception:
                entry = input(C["neon_pink"] + prompt + C["reset"])
        else:
            entry = input(C["neon_pink"] + prompt + C["reset"])

        entry = entry.strip()

        if not entry or entry.lower() == "q":
            neon_print("Done entering tokens.", "neon_green")
            break

        print(C["neon_white"] + "  validating " + C["reset"], end="")
        spinner()

        if validate_token(entry):
            neon_print("✔ Accepted — " + mask_token(entry), "neon_green")
            tokens.append(entry)
            idx += 1
        else:
            neon_print("✖ Invalid token format", "neon_red")

    return tokens

# ----- Patch bot for each token -----
def patch_bot_file_single_token(original_path, dest_path, token, owner_id):
    with open(original_path, "r", encoding="utf-8") as f:
        src = f.read()

    token_repr = f'[\n    "{token}"\n]'
    src = re.sub(r"TOKENS\s*=\s*\[[^\]]*\]", f"TOKENS = {token_repr}", src)
    src = re.sub(r"OWNER_ID\s*=\s*\d+", f"OWNER_ID = {owner_id}", src)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(src)

# ----- Process management -----
launched_procs = []

def is_launched(path):
    for proc, file, _ in launched_procs:
        if os.path.abspath(file) == os.path.abspath(path):
            return True
    return False

def start_tempfile(path, masked=None):
    if is_launched(path):
        return
    python = sys.executable or "python3"
    try:
        proc = subprocess.Popen(
            [python, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        launched_procs.append((proc, path, masked))
        neon_print(f"  ▶ Started {path} (pid {proc.pid})", "neon_green")
    except Exception as e:
        neon_print(f"Failed to start {path}: {e}", "neon_red")

def launch_bot_for_each_token(bot_filename, tokens, owner_id):
    base, ext = os.path.splitext(TEMP_FILENAME)
    for i, tok in enumerate(tokens, 1):
        dest = f"{base}_{i}{ext}"
        patch_bot_file_single_token(bot_filename, dest, tok, owner_id)
        start_tempfile(dest, mask_token(tok))

def stop_all_procs():
    neon_print("Stopping all bots...", "neon_yellow")
    for proc, _, _ in launched_procs:
        try:
            proc.terminate()
        except:
            pass
    time.sleep(0.4)
    for proc, f, _ in launched_procs:
        try:
            if proc.poll() is None:
                proc.kill()
        except:
            pass
        try:
            os.remove(f)
        except:
            pass
    launched_procs.clear()
    neon_print("All threads stopped.", "neon_pink")

def show_status():
    if not launched_procs:
        neon_print("No bots running.", "neon_yellow")
        return
    neon_print("Bot Status:", "neon_cyan")
    for proc, f, m in launched_procs:
        st = "running" if proc.poll() is None else f"exited({proc.returncode})"
        neon_print(f"PID {proc.pid} | {st} | {f} | {m}", "neon_white")

# ----- Surprise logic -----
def sparkle(d=0.6, r=6):
    chars = ["✦", "✧", "✵", "✶"]
    for i in range(r):
        print(C["neon_green"] + chars[i % 4] + C["reset"], end="", flush=True)
        time.sleep(d/(r*1.4))
        print("\b \b", end="", flush=True)

def open_surprise():
    if os.system(f'termux-open-url "{_SURPRISE_URL}"') == 0:
        return
    if os.system(f'xdg-open "{_SURPRISE_URL}"') == 0:
        return
    if os.system(f'am start -a android.intent.action.VIEW -d "{_SURPRISE_URL}"') == 0:
        return
    try:
        webbrowser.open(_SURPRISE_URL)
    except:
        pass

def option_surprise():
    neon_print("Launching Surprise...", "neon_green")
    sparkle()
    open_surprise()

    neon_print("Please wait", "neon_yellow", end="")
    for s in range(10, 0, -1):
        print(f" {C['neon_pink']}{s}{C['reset']}", end="", flush=True)
        time.sleep(1)
        print("\b" * (len(str(s)) + 1), end="")

    print()
    while True:
        ans = input(C["neon_cyan"] + "Did you join? (y/n): " + C["reset"]).strip().lower()
        if ans in ("y", "yes"):
            neon_print("Great! Returning to menu.", "neon_green")
            break
        neon_print("Are you serious — join plzz!", "neon_red")
        sparkle()
        open_surprise()
        time.sleep(2)

# ----- Command mode -----
def option_command_mode(bot_filename):
    tokens = read_tokens_interactively()
    if not tokens:
        neon_print("No tokens entered.", "neon_red")
        return

    owner_id = prompt_owner_id()
    launch_bot_for_each_token(bot_filename, tokens, owner_id)

    neon_print("Bots running. Go to Telegram. Press Enter to stop...", "neon_yellow")
    input()
    stop_all_procs()

# ----- Main Loop -----
def ensure_bot_file_exists():
    if not os.path.exists(BOT_FILENAME):
        neon_print(f"Missing bot file: {BOT_FILENAME}", "neon_red")
        sys.exit(1)

def menu_input():
    return input(C["neon_cyan"] + C["bold"] + "Select option (1-5): " + C["reset"])

def main():
    ensure_bot_file_exists()
    boot_animation()

    while True:
        os.system("clear")
        neon_header_pulse()
        print_menu()

        try:
            choice = menu_input().strip()
        except:
            choice = "4"

        if choice == "1":
            option_command_mode(BOT_FILENAME)
            input("Press Enter to return...")

        elif choice == "2":
            show_status()
            input("Press Enter to return...")

        elif choice == "3":
            stop_all_procs()
            input("Press Enter to continue...")

        elif choice == "4":
            neon_print("Goodbye ✨!! I hope u enjoyed and make sure to join channel.for updates", "neon_pink")
            break

        elif choice == "5":
            option_surprise()
            input()

        else:
            neon_print("Invalid choice!", "neon_red")
            time.sleep(1)

if __name__ == "__main__":
    main()
