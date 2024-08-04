import http.server
import socketserver
import os
import sys
import threading
import signal

# Colour Codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
# Styles
UNDERLINE = '\033[4m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Script Variables
NEWLN = "\n"
AUTHOR = "Diagnostics"
SCRIPT_NAME = os.path.basename(__file__)
EX_USAGE = f"Usage: Run this script to serve Oathsworn story mode.{NEWLN}   Example: python {SCRIPT_NAME}"

# Global Variables
server = None

# Functions for Error and Warning Handling
def print_header(message):
    print(f"{PURPLE}{BOLD}{message}{RESET}", flush=True)

def print_fatal_error(message):
    print(f"{RED}{BOLD}Fatal Error: {message}{RESET}", flush=True)
    sys.exit(1)

def print_error(message):
    print(f"{RED}{BOLD}Error: {message}{RESET}", flush=True)

def print_warning(message):
    print(f"{YELLOW}{BOLD}Warning: {message}{RESET}", flush=True)

def print_success(message):
    print(f"{GREEN}{BOLD}{message}{RESET}", flush=True)

def print_info(message):
    print(f"{BLUE}{message}{RESET}", flush=True)

def print_separator():
    print(f"{CYAN}------------------------------------{RESET}", flush=True)

# Check if the script is run with sudo (if required)
def check_sudo():
    if os.geteuid() != 0:
        print_fatal_error("Permissions you don't have; sudo you must.")

def start_server(port, directory):
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    global server
    server = socketserver.TCPServer(("", port), CustomHandler)
    print_info(f"Serving at port {port}")
    server.serve_forever()

def stop_server(signum, frame):
    global server
    if server:
        print_info("Shutting down the server...")
        server.shutdown()
        server.server_close()
    sys.exit(0)

def main():
    # Author and Usage
    print_header(f"Script by: {AUTHOR}{NEWLN}   {EX_USAGE}")

    # Check if the output directory exists
    output_dir = "output"
    if not os.path.isdir(output_dir):
        print_fatal_error(f"Directory '{output_dir}' does not exist. Run 'python web.py' first.")

    # Check if index.html exists in the current directory
    index_file = "index.html"
    if not os.path.isfile(index_file):
        print_fatal_error(f"'{index_file}' does not exist in the current directory.")
    
    # Start the web server in a separate thread
    port = 3000
    print_info("Starting the web server...")
    server_thread = threading.Thread(target=start_server, args=(port, '.'), daemon=True)
    server_thread.start()

    print_warning("Press 'ctrl+c' to exit...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print_info("Shutting down the server...")

    print_success("Script reached the end.")

if __name__ == "__main__":
    main()
