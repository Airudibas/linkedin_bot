# LinkedIn Connection Bot

A Python script to automate connecting with people on LinkedIn who have mutual connections with you.

## Features

- Search for people by job title or keywords
- Filter for profiles with mutual connections
- Automatic or manual login
- Dry-run mode to preview candidates without sending requests
- Headless mode for background operation
- Configurable maximum number of requests

## Requirements

- Python 3.6+
- Chrome browser installed
- Required Python packages (install via pip):
  ```
  pip install -r requirements.txt
  ```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/linkedin_bot.git
   cd linkedin_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up environment variables for automatic login:
   - Create a `.env` file in the project directory
   - Add your LinkedIn credentials:
     ```
     LINKEDIN_USER=your.email@example.com
     LINKEDIN_PASS=your_password
     ```

## Usage

Basic usage:
```bash
python networking.py --title "Software Engineer"
```

### Command Line Options

- `--title`: Job title or keyword to search for (default: "CTO")
  ```bash
  python networking.py --title "Data Scientist"
  ```

- `--max-requests`: Maximum number of connection requests to send (default: 3)
  ```bash
  python networking.py --title "Developer" --max-requests 5
  ```

- `--dry-run`: List candidates without sending requests
  ```bash
  python networking.py --title "CTO" --dry-run
  ```

- `--headless`: Run in headless mode (no browser GUI)
  ```bash
  python networking.py --title "Developer" --headless
  ```

### Examples

1. Preview potential connections (no requests sent):
   ```bash
   python networking.py --title "Python Developer" --dry-run
   ```

2. Connect with up to 10 CTOs:
   ```bash
   python networking.py --title "CTO" --max-requests 10
   ```

3. Run in background mode:
   ```bash
   python networking.py --title "Tech Lead" --max-requests 5 --headless
   ```

## Important Notes

- If no environment variables are set, the script will prompt for manual login
- The script only sends requests to profiles with mutual connections
- LinkedIn has rate limits and may temporarily restrict accounts that send too many requests
- Use responsibly and in accordance with LinkedIn's terms of service

## Legal Disclaimer

This tool is for educational purposes only. Use of automated tools may violate LinkedIn's terms of service. Use at your own risk.