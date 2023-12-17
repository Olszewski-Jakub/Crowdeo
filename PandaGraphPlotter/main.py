# receive_and_plot.py
import serial
import json
import matplotlib.pyplot as plt

# Configure the serial port (adjust the port name and baud rate as needed)
ser = serial.Serial('COM4', 9600, timeout=1)

def receive_data():
    # Read data from the serial port
    raw_data = ser.readline().decode('utf-8').strip()

    try:
        # Attempt to parse the received data as JSON
        data = json.loads(raw_data)
        return data
    except json.JSONDecodeError:
        # Handle the case where the data is not valid JSON
        print("Received data is not valid JSON:", raw_data)
        return None

def plot_graph(device_counts, average_distances):
    # Plot device count graph
    plt.subplot(2, 1, 1)
    plt.plot(device_counts)
    plt.xlabel('Scans')
    plt.ylabel('Device Count')
    plt.title('Device Count Over Scans')
    plt.grid(True)

    # Plot average distance graph
    plt.subplot(2, 1, 2)
    plt.plot(average_distances)
    plt.xlabel('Scans')
    plt.ylabel('Average Distance (m)')
    plt.title('Average Distance Over Scans')
    plt.grid(True)

    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()

def main():
    device_counts = []
    average_distances = []

    while True:
        data = receive_data()

        if data is not None and "device_count" in data and "device_list" in data:
            # Received device count data
            device_count = data["device_count"]
            device_counts.append(device_count)

            # Calculate average distance
            device_list = data["device_list"]
            distances = [float(device["distance"]) for device in device_list]
            average_distance = sum(distances) / len(distances)
            average_distances.append(average_distance)

            # Print the entire received JSON for reference
            print(json.dumps(data, indent=2))

            # Plot the graph with cumulative counts and average distances
            plot_graph(device_counts, average_distances)

if __name__ == "__main__":
    main()
