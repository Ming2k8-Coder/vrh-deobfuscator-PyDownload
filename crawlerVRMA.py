import requests
import json

# Define the target URL
url = "https://hub.vroid.com/api/character_models/"

# Define the custom headers (excluding ones like 'method', 'path', 'scheme' which are handled by the library)
headers = {
    "authority": "hub.vroid.com",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,nl;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://hub.vroid.com/en",
    "sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-api-version": "11"
}

# The PowerShell command uses a WebSession, which typically handles cookies and session state.
# For a single GET request without explicit cookie management, you can usually omit session handling.
# If session management (like maintaining cookies) is needed across multiple requests, 
# you'd use a `requests.Session()` object, but for this simple GET, a direct call is enough.
charid = input("INPUT CHARACTER ID:")
urlf = url + charid
try:
    # Make the GET request
    response = requests.get(urlf, headers=headers)

    # Raise an exception for bad status codes (4xx or 5xx)
    response.raise_for_status()

    print(f"✅ Request successful. Status Code: {response.status_code}\n")
    print("--- Response Content (JSON Formatted) ---")
    
    # Check if the response is JSON and pretty-print it
    try:
        data = response.json()
        print(json.dumps(data, indent=4))
    except json.JSONDecodeError:
        # If it's not JSON, print the raw text content
        print(response.text)

except requests.exceptions.RequestException as e:
    # Handle any request errors (connection, timeout, DNS, bad status)
    print(f"❌ An error occurred: {e}")
