import flet as ft
import paramiko
import time
import threading
import json

def get_data_from_server():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("170.64.176.75", username="streamlit", password="DEcrc@78172")
        sftp = ssh.open_sftp()
        file_path = "Thilac/DATA/data.json"
        with sftp.file(file_path, "r") as file:
            content = json.load(file)
        sftp.close()
        ssh.close()
        return content
    except Exception as e:
        return {"error": str(e)}

def main(page: ft.Page):
    # Mobile-Friendly UI Adjustments
    page.title = "GLIDER DATA"
    page.bgcolor = "#1E1E2E"
    page.padding = 10
    page.window.width = 400
    page.window.height = 600
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Title
    title = ft.Text("GLIDER DATA", size=24, weight="bold", color="#FFFFFF")
    
    # Interval input field
    interval_field = ft.TextField(
        label="Update Interval (seconds)", 
        value="5", 
        keyboard_type="number",
        bgcolor="#2E2E3E",
        color="#FFFFFF",
        border_color="#A1A1C1",
        width=250
    )
    
    # Connect button
    connect_button = ft.ElevatedButton(
        "Connect", 
        on_click=lambda e: start_fetching_data(),
        bgcolor="#3A86FF",
        color="#FFFFFF",
        width=250
    )
    
    # Status text area
    text_area = ft.Text(
        value="Click Connect to Fetch Data", 
        selectable=True, 
        color="#FFFFFF",
        size=16,
        text_align="center"
    )
    
    # DataTable to display fetched data
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Timestamp", color="#FFFFFF")),
            ft.DataColumn(ft.Text("Value", color="#FFFFFF"))
        ],
        rows=[],
        width=350,
        height=300,
        bgcolor="#2E2E3E"
    )
    
    # Layout container
    container = ft.Column(
        [title, interval_field, connect_button, text_area, data_table],
        alignment="center",
        horizontal_alignment="center",
        spacing=15
    )
    
    page.add(container)
    
    def start_fetching_data():
        try:
            interval = int(interval_field.value)
        except ValueError:
            text_area.value = "Invalid interval! Please enter a number."
            page.update()
            return
        
        def update_data():
            last_content = None  # Initialize to None
            while True:
                content = get_data_from_server()
                if content != last_content and isinstance(content, list):  # Ensure it's a list
                    rows = []
                    for entry in content:  # Loop through the list directly
                        try:
                            timestamp = entry["timestamp"]
                            value = entry["value"]
                            rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(timestamp, color="#FFFFFF")),
                                                           ft.DataCell(ft.Text(str(value), color="#FFFFFF"))]))
                        except (KeyError, ValueError):
                            continue
                    
                    # Update the DataTable with the fetched rows
                    data_table.rows = rows
                    page.update()
                    last_content = content
                time.sleep(interval)
        
        threading.Thread(target=update_data, daemon=True).start()

ft.app(target=main)
