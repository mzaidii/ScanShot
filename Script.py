import os
import nmap
import requests
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # For displaying progress

# Function to take screenshot of the HTTP/HTTPS page
def take_screenshot(url, output_path):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"Taking screenshot of {url}...")
        driver.get(url)
        time.sleep(1)  # wait for the page to load
        driver.save_screenshot(output_path)
        print(f'Screenshot saved for {url} at {output_path}')
    except Exception as e:
        print(f'Error taking screenshot for {url}: {e}')
    finally:
        driver.quit()

# Async function to determine if a port is serving HTTP or HTTPS
async def check_http_service_async(host, port):
    print(f"Checking HTTP/HTTPS service on {host}:{port}...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'http://{host}:{port}', timeout=3) as response:
                if response.status == 200 or 'text/html' in response.headers.get('Content-Type', ''):
                    print(f"HTTP service found on {host}:{port}")
                    return 'http'
        except Exception:
            pass

        try:
            async with session.get(f'https://{host}:{port}', timeout=3, ssl=False) as response:
                if response.status == 200 or 'text/html' in response.headers.get('Content-Type', ''):
                    print(f"HTTPS service found on {host}:{port}")
                    return 'https'
        except Exception:
            pass

    print(f"No HTTP/HTTPS service found on {host}:{port}")
    return None

# Async function to handle scanning and taking screenshots
async def scan_and_capture_async(host, port):
    print(f"Starting scan for {host} on port {port}...")
    service_type = await check_http_service_async(host, port)
    if service_type:
        url = f'{service_type}://{host}:{port}'
        output_path = os.path.join('screenshots', f'{host}_{port}.png')
        take_screenshot(url, output_path)
    print(f"Completed scan for {host} on port {port}.")

# Function to scan a single host using Nmap
def scan_host_with_nmap(host):
    scanner = nmap.PortScanner()
    print(f'Starting Nmap scan for IP: {host}...')
    scanner.scan(hosts=host, arguments='-p 1-65535 -sS -T4 --open')

    tasks = []
    for port in scanner[host].all_tcp():
        if scanner[host]['tcp'][port]['state'] == 'open':
            print(f"Open port found on {host}:{port}")
            tasks.append((host, port))
    
    print(f"Completed Nmap scan for IP: {host}.")
    return tasks

# Function to scan subnet using Nmap with threading for each host
def scan_subnet_with_nmap(subnet, max_workers=10):
    scanner = nmap.PortScanner()
    print(f'Starting Nmap host discovery for subnet: {subnet}...')

    # Perform host discovery only
    scanner.scan(hosts=subnet, arguments='-sn')  # Ping scan for host discovery
    
    # List of hosts to scan
    hosts_to_scan = [host for host in scanner.all_hosts() if scanner[host].state() == 'up']
    
    print(f"Found {len(hosts_to_scan)} live hosts to scan.")

    # Use ThreadPoolExecutor for parallel scanning
    tasks = []
    
    # Adding progress bar to track the number of completed Nmap scans
    with tqdm(total=len(hosts_to_scan), desc="Nmap Scanning Progress", unit="host") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_host = {executor.submit(scan_host_with_nmap, host): host for host in hosts_to_scan}
            
            for future in as_completed(future_to_host):
                host = future_to_host[future]
                try:
                    host_tasks = future.result()
                    tasks.extend(host_tasks)
                except Exception as exc:
                    print(f'{host} generated an exception: {exc}')
                # Update progress bar after each host is scanned
                pbar.update(1)
    
    print(f"Total open ports found: {len(tasks)}")
    return tasks

# Main function
def main():
    subnet = input('Enter the subnet (e.g., 192.168.1.0/24): ').strip()
    output_dir = 'screenshots'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Starting the scanning process...")
    tasks = scan_subnet_with_nmap(subnet)

    # Run the asynchronous event loop for taking screenshots
    loop = asyncio.get_event_loop()

    asyncio_tasks = [scan_and_capture_async(host, port) for host, port in tasks]
    loop.run_until_complete(asyncio.gather(*asyncio_tasks))

    print("All tasks are completed.")

if __name__ == "__main__":
    main()
