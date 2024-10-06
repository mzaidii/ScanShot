# ScanShot
ScanShot is a multi-threaded network scanning and web service discovery tool that identifies open ports, detects HTTP/HTTPS services, and captures screenshots of accessible web pages. Built with Python, it uses Nmap for network scanning, Selenium for browser automation, and aiohttp for asynchronous HTTP requests. With real-time progress tracking, ScanShot helps security professionals quickly analyze subnets and document exposed services visually.

Before installing and running ScanShot, ensure you have the following installed:
Python 3.7 or higher
pip (Python package manager)

**Clone the Repository**
  First, clone the GitHub repository to your local machine:
  git clone https://github.com/yourusername/scanshot.git
  cd scanshot

**Install Dependencies:**
  Install all required Python packages by using the requirements.txt file:
  pip install -r requirements.txt

**Usage**
Once the dependencies are installed, you can run ScanShot as follows:
  
  Run the Tool
  Execute the Python script to start scanning:
    python scanshot.py
    Input Subnet
    When prompted, enter the subnet you want to scan (e.g., 192.168.1.0/24).
  
  View Results
  The tool will:
  Perform an Nmap scan of the subnet to discover live hosts and open ports.
  Detect HTTP/HTTPS services on open ports.
  Capture screenshots of accessible web services and save them in the screenshots folder.
  Example
  Enter the subnet (e.g., 192.168.1.0/24): 192.168.1.0/24
  The tool will display the progress of scanning and notify you when each scan is completed. Screenshots of detected web services will be saved to the screenshots directory.

**Features**
Multi-threaded Scanning: Faster scanning across multiple hosts using concurrent threads.
HTTP/HTTPS Detection: Identifies web services running on open ports.
Screenshot Capture: Automatically takes screenshots of accessible web pages.
Real-time Progress: Displays real-time progress of network scanning and screenshot captures.
