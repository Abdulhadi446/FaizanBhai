import webview
import subprocess
import time
import requests

url = "http://127.0.0.1:5000/"

# Function to check if the server is running and accessible
def check_server_ready(url):
    try:
        response = requests.get(url)
        # If the server responds with status code 200, it is ready
        if response.status_code == 200:
            return True
    except:
        # If connection error occurs, the server is not ready yet
        print(f"Error connecting to server: ")
    return False

# Launch the external process (e.g., main.exe)
process = subprocess.Popen("main.exe", shell=True)

# Wait until the server is ready
while not check_server_ready(url):
    print("Waiting for server to be ready...")
    time.sleep(1)  # Check every second if the server is up

# Create a webview window once the server is ready
window = webview.create_window("Jarvis", url)
print("Webview window created successfully.")
webview.start()

# Terminate the process once the app is closed
process.terminate()