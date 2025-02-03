import serial
import json
import datetime
import paramiko

# Setup for the serial port (adjust according to your Arduino's port)
ser = serial.Serial('COM6', 9600, timeout=1)  # Change 'COM6' to your Arduino port

# Establish SSH connection to the server
def ssh_connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("your server ip", username="your server name", password="your server pwd")
    return ssh

# Function to save data to JSON file
def save_data_to_json(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict = {"timestamp": timestamp, "value": data}

    # Fetch the current file contents and append the new data
    try:
        ssh = ssh_connect()
        sftp = ssh.open_sftp()
        file_path = '/home/streamlit/Thilac/DATA/data.json'

        try:
            # Try opening the file to load existing data
            with sftp.open(file_path, 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, initialize as an empty list
            current_data = []
        except json.JSONDecodeError:
            # If the file is empty or corrupted, also start with an empty list
            current_data = []

        current_data.append(data_dict)

        # Save updated data back to the file
        with sftp.open(file_path, 'w') as file:
            json.dump(current_data, file, indent=4)

        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"Error: {e}")

# Main function to read data and send to server
def main():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received Data: {line}")
                # Save the data to JSON file with timestamp
                save_data_to_json(line)

if __name__ == "__main__":
    main()
