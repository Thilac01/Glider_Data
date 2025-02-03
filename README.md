# Real-Time Arduino Sensor Data Fetcher and Display

This project demonstrates how to fetch real-time sensor data from an Arduino, store it in a JSON file on a cloud Linux server, and display it in a mobile-friendly interface built using the **Flet** Python framework.

The goal of this application is to allow users to monitor real-time sensor values from an Arduino board remotely, providing them with easy-to-read data in a visually appealing interface.

## Features

- **Real-Time Data Fetching**: Fetches sensor data from an Arduino, stored as JSON on a remote cloud Linux machine.
- **Mobile-Friendly Interface**: Built using the Flet framework for easy access on mobile devices.
- **Automatic Data Refresh**: Updates the displayed data at a user-specified interval.
- **Error Handling**: Includes robust error handling for invalid inputs and connection issues.
- **Data Display**: Displays fetched sensor data in a structured table format with timestamps and values.

## Requirements

### Software Requirements

- **Python** (version 3.7 or higher)
- **Flet**: A framework for building real-time web apps.
- **Paramiko**: A library for making SSH connections to remote servers.

### Installation

To get started with the application, you need to install the required Python dependencies:

```bash
pip install flet paramiko
