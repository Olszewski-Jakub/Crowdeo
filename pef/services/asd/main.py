# main.py

import wifimgr
import gc
import usocket as socket
from _thread import start_new_thread
from uart_handler import uart_write

uart_write("Raspberry Pi Pico W Starting")

uart_write("Raspberry Pi Pico W Connecting to WiFi")
wlan = wifimgr.get_connection()
if wlan is None:
    uart_write("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D
uart_write("Raspberry Pi Pico W OK")


def web_page():
    status_message = "Connected to Wi-Fi" if wlan.isconnected() else "Not connected to Wi-Fi"
    html = f"""<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {{
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }}
        .button {{
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }}
        .button1 {{
            background-color: #000000;
        }}
    </style>
</head>
<body>
    <h2>Raspberry Pi Pico Web Server</h2>
    <p>{status_message}</p>
</body>
</html>"""
    return html


# Web server logic
def run_web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        uart_write('Received HTTP GET connection request from %s' + str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        uart_write('GET Rquest Content = %s' + request)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        uart_write('Connection closed')


# Start the web server in a new thread
start_new_thread(run_web_server, ())

# Main loop
while True:
    try:
        # Your main loop logic here...

        # Check Wi-Fi connection status and update web page accordingly
        if wlan.isconnected():
            uart_write("Connected to Wi-Fi")
        else:
            uart_write("Not connected to Wi-Fi")

        # Additional logic...

    except OSError as e:
        # Handle OSError...
        pass
