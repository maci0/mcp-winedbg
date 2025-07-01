import httpx
import json
import os
import time

def main():
    base_url = "http://127.0.0.1:8080"
    test_app_path = os.path.join(os.path.dirname(__file__), 'test_app.exe')

    if not os.path.exists(test_app_path):
        print(f"Test application not found at {test_app_path}")
        print("Please compile it first.")
        return

    with httpx.Client() as client:
        # Wait for the server to start
        print("Waiting for server to start...")
        while True:
            try:
                response = client.get(f"{base_url}/tools")
                if response.status_code == 200:
                    print("Server started")
                    break
            except httpx.ConnectError:
                time.sleep(0.1)
        
        # 1. Get the list of tools
        print("Getting tool list...")
        print(f"Server response: {response.status_code}")
        print(response.json())

        # 2. Set the debug channels
        print("\nSetting debug channels...")
        response = client.post(
            f"{base_url}/set_debug_channel",
            json={"channels": "+relay,-heap"}
        )
        print(f"Server response: {response.status_code}")
        print(response.text)

        # 3. Get the debug channels
        print("\nGetting debug channels...")
        response = client.post(f"{base_url}/get_debug_channels")
        print(f"Server response: {response.status_code}")
        print(response.text)

        # 4. Run the test application
        print("\nStarting winedbg with the test application...")
        response = client.post(
            f"{base_url}/run",
            json={"executable": test_app_path}
        )
        print(f"Server response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print(response.text)

        # 5. Get process info
        print("\nGetting process info...")
        response = client.post(f"{base_url}/info_proc")
        print(f"Server response: {response.status_code}")
        print(response.text)

        # 6. Quit winedbg
        print("\nQuitting winedbg...")
        response = client.post(f"{base_url}/quit")
        print(f"Server response: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    main()

