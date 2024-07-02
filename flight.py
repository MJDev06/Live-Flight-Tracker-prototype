import requests
import tkinter as tk
from tkinter import ttk

# Define the OpenSky API URL
opensky_api_url = "YOUR-API"

# Example dictionary mapping ICAO24 prefixes to country names
icao24_to_country = {
    "3c": "Germany",
    "4b": "Switzerland",
    "a2": "United States",
    "e4": "Mexico",
    "7c": "Australia",
    # Add more mappings as needed
}

def get_flight_data():
    try:
        # Make a GET request to the API
        response = requests.get(opensky_api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            flight_data = response.json()
            return flight_data
        else:
            print(f"Failed to get data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_additional_flight_info(icao24):
    country_prefix = icao24[:2].lower()
    country = icao24_to_country.get(country_prefix, "Unknown")
    destination = "Destination info unavailable"  # Placeholder for actual destination info
    return {
        "country": country,
        "destination": destination
    }

def update_flight_data():
    flight_data = get_flight_data()
    if flight_data and "states" in flight_data:
        flight_list.delete(*flight_list.get_children())
        for flight in flight_data['states'][:10]:
            icao24 = flight[0]
            additional_info = get_additional_flight_info(icao24)
            flight_list.insert("", "end", values=(
                icao24, 
                flight[6],  # Latitude
                flight[5],  # Longitude
                flight[13],  # Altitude
                additional_info.get("country", "N/A"),
                additional_info.get("destination", "N/A")
            ))
    root.after(5000, update_flight_data)  # Update every 5 seconds

# Set up the main application window
root = tk.Tk()
root.title("Live Flight Tracker")

# Set up the tree view to display flight data
columns = ("icao24", "latitude", "longitude", "altitude", "country", "destination")
flight_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    flight_list.heading(col, text=col)
    flight_list.column(col, anchor="center")

flight_list.pack(fill=tk.BOTH, expand=True)

# Start the live updating
root.after(0, update_flight_data)

# Run the application
root.mainloop()
