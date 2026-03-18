import requests
import time
import sys

# Spoofed Windows 11 Edge User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
CLIENT_ID = "1950a258-227b-4e31-a9cf-717495945fc2" # Azure PowerShell

headers = {
    "User-Agent": USER_AGENT
}

# Step 1: Request Device Code
print("[*] Requesting Device Code...")
device_code_data = {
    "client_id": CLIENT_ID,
    "resource": "https://graph.microsoft.com"
}
resp = requests.post("https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0", headers=headers, data=device_code_data)
auth_data = resp.json()

if "device_code" not in auth_data:
    print("[-] Failed to get device code. Response:")
    print(auth_data)
    sys.exit(1)

device_code = auth_data["device_code"]
interval = int(auth_data.get("interval", 5))

print(f"\n[+] Action Required:")
print(f"    Go to: {auth_data['verification_url']}")
print(f"    Enter code: {auth_data['user_code']}\n")
print(f"[*] Waiting for you to complete authentication in the browser... (Polling every {interval} seconds)")

# Step 2: Poll for the Token
token_data = {
    "client_id": CLIENT_ID,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "code": device_code
}

while True:
    time.sleep(interval)
    token_resp = requests.post("https://login.microsoftonline.com/common/oauth2/token?api-version=1.0", headers=headers, data=token_data)
    token_json = token_resp.json()

    if "error" in token_json:
        if token_json["error"] == "authorization_pending":
            # Still waiting on user
            continue
        elif token_json["error"] == "authorization_declined":
            print("[-] You declined the authorization.")
            sys.exit(1)
        elif token_json["error"] == "expired_token":
            print("[-] The device code expired. Run the script again.")
            sys.exit(1)
        else:
            print(f"[-] An unexpected error occurred: {token_json.get('error_description', token_json['error'])}")
            sys.exit(1)
            
    # Success!
    if "refresh_token" in token_json:
        print("\n[+] Authentication Successful!")
        print("-" * 40)
        print(f"Refresh Token:\n{token_json['refresh_token']}")
        print("-" * 40)
        break
    else:
        print("[-] Authenticated, but no refresh token was returned. Check tenant policies.")
        print(token_json)
        break
