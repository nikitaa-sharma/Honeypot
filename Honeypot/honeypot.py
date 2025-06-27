import datetime
import getpass
import os
import sys
import time

LOG_FILE = "honeypot_logs.txt"
AUTHORIZED_USER = "admin"
AUTHORIZED_PASS = "SecurePass123!"  # Change this to your secure password

def log_attempt(username, password, success=False):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILURE"
    log_entry = f"[{timestamp}] - {status} - Username: '{username}' Password: '{password}'\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return log_entry.strip()

def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print("\033[1;32m")  # Green color
    print("=" * 60)
    print(" SECURE SERVER ACCESS ".center(60, '*'))
    print("=" * 60)
    print("\033[0m")  # Reset color

def honeypot():
    """Main honeypot function"""
    attempts = 0
    auth_attempts = 0
    max_auth_attempts = 3
    
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    
    print(f"Honeypot active. Logging to: {os.path.abspath(LOG_FILE)}")
    print(f"Authorized user: {AUTHORIZED_USER}")
    print("Press Ctrl+C to exit\n")
    time.sleep(2)
    
    try:
        while True:
            attempts += 1
            clear_screen()
            show_banner()
            
            print(f"\nLogin Attempt #{attempts}")
            print("---------------------")
            
            try:
                username = input("Username: ").strip()
                
                # Allow exit command
                if username.lower() in ['exit', 'quit']:
                    break
                
                password = getpass.getpass("Password: ").strip()
                
                # Check credentials
                if username == AUTHORIZED_USER and password == AUTHORIZED_PASS:
                    # Log successful authentication
                    log_entry = log_attempt(username, password, success=True)
                    print("\n\033[1;32mAuthentication successful! Access granted.\033[0m")
                    print(f"Logged: {log_entry}")
                    
                    # Simulate authorized session
                    print("\nWelcome to the secure system!")
                    print("Type 'logout' to end session or continue working...")
                    
                    # Simple session simulation
                    while True:
                        command = input(f"{AUTHORIZED_USER}@secure-server$ ").strip()
                        if command.lower() == 'logout':
                            print("Logging out...")
                            time.sleep(1)
                            break
                        elif command:
                            print(f"Executing: {command}")
                            # Log command execution
                            with open(LOG_FILE, "a") as f:
                                f.write(f"   |_ Command executed: '{command}'\n")
                else:
                    # Log failed attempt
                    log_entry = log_attempt(username, password)
                    auth_attempts += 1
                    remaining = max(0, max_auth_attempts - auth_attempts)
                    
                    print(f"\n\033[1;31mAuthentication failed. {remaining} attempts remaining.\033[0m")
                    print(f"Logged: {log_entry}")
                    
                    if auth_attempts >= max_auth_attempts:
                        print("\n\033[1;31mMaximum attempts reached. System locked.\033[0m")
                        print("Please contact administrator to unlock.")
                        time.sleep(3)
                        auth_attempts = 0  # Reset for next session
                
                # Delay next prompt
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                break
                
    except KeyboardInterrupt:
        print("\nHoneypot terminated")

if __name__ == '__main__':
    honeypot()
    print("\nHoneypot session ended. All captured credentials saved.")