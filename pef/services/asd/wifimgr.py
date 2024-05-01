# wifimgr.py

import network
import socket
import ure
import time

from uart_handler import uart_write

ap_ssid = "WifiManager"
ap_password = "AP123456"


NETWORK_PROFILES = 'wifi.dat'

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None


def get_connection():
    """Return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta

    connected = False
    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = read_profiles()

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            uart_write("SSID: %s Channel: %d RSSI: %d Authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    uart_write("Skipping unknown encrypted network")
            else:  # open
                connected = do_connect(ssid, None)
            if connected:
                break

    except Exception as e:
        uart_write("Exception in get_connection: {}".format(e))

    # Start web server for connection manager:
    if not connected:
        connected = start()

    return wlan_sta if connected else None


def read_profiles():
    try:
        with open(NETWORK_PROFILES) as f:
            lines = f.readlines()
    except OSError as e:
        if e.args[0] == 2:  # File not found error
            uart_write("Profiles file not found, creating...")
            with open(NETWORK_PROFILES, 'w') as new_file:
                new_file.write('')
            return {}
        else:
            uart_write("Error reading profiles file: {}".format(e))
            return {}

    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    uart_write(str(profiles))
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
        uart_write(str(lines))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))



def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    uart_write('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        uart_write('.')
    if connected:
        uart_write('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        uart_write('\nFailed. Not Connected to: ' + ssid)
    return connected


def send_header(client, status_code=200, content_length=None):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
        client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()


def handle_root(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid = ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h5>
                <span style="color: #ff0000;">
                    Your ssid and password information will be saved into the
                    "%(filename)s" file in your ESP module for future usage.
                    Be careful about security!
                </span>
            </h5>
            <hr />
            <h2 style="color: #2e6c80;">
                Some useful infos:
            </h2>
            <ul>
                <li>
                    Original code from <a href="https://github.com/cpopp/MicroPythonSamples"
                        target="_blank" rel="noopener">cpopp/MicroPythonSamples</a>.
                </li>
                <li>
                    This code available at <a href="https://github.com/tayfunulu/WiFiManager"
                        target="_blank" rel="noopener">tayfunulu/WiFiManager</a>.
                </li>
            </ul>
        </html>
    """ % dict(filename=NETWORK_PROFILES))
    uart_write("Sending response")
    client.close()


def handle_configure(client, request):
    try:
        match = ure.search(r"ssid=([^&]+)(?:&password=([^&]*))?", request.decode('utf-8'))

        if match is None:
            uart_write("No match found for parameters")
            send_response(client, "Parameters not found", status_code=400)
            return False

        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!") if match.group(2) else ""
        #
        # ssid = "Dunlin-Student-WiFi"
        # password = "Dunlin2023!"
        uart_write("SSID:" + str(ssid))
        uart_write("Password:" + str(password))

        if len(ssid) == 0:
            send_response(client, "SSID must be provided", status_code=400)
            return False

        if do_connect(ssid, password):
            response = """\
                <html>
                    <center>
                        <br><br>
                        <h1 style="color: #5e9ca0; text-align: center;">
                            <span style="color: #ff0000;">
                                ESP successfully connected to WiFi network %(ssid)s.
                            </span>
                        </h1>
                        <br><br>
                    </center>
                </html>
            """ % dict(ssid=ssid)
            send_response(client, response)

            try:
                profiles = read_profiles()
                uart_write("Profiles: " + str(profiles))
            except OSError:
                profiles = {}
            profiles[ssid] = password
            # TODO uncomment this
            write_profiles(profiles)

            time.sleep(5)

            return True
        else:
            response = """\
                <html>
                    <center>
                        <h1 style="color: #5e9ca0; text-align: center;">
                            <span style="color: #ff0000;">
                                ESP could not connect to WiFi network %(ssid)s.
                            </span>
                        </h1>
                        <br><br>
                        <form>
                            <input type="button" value="Go back!" onclick="history.back()"></input>
                        </form>
                    </center>
                </html>
            """ % dict(ssid=ssid)
            send_response(client, response)
            return False

    except Exception as e:
        print("Exception in handle_configure:", e)
        return False


def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None


def start(port=80):
    uart_write("test1")
    global server_socket
    uart_write("test2")
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    uart_write("test3")
    stop()
    uart_write("test4")
    # Ensure that both WLAN interfaces are inactive before starting the server
    wlan_sta.active(False)
    uart_write("test5")
    wlan_ap.active(False)
    uart_write("test6")
    wlan_ap.config(essid=ap_ssid, password=ap_password)
    uart_write("test7")
    wlan_ap.active(True)
    uart_write("test8")
    server_socket = socket.socket()
    uart_write("test9")
    server_socket.bind(addr)
    uart_write("test10")
    server_socket.listen(1)

    uart_write('Connect to WiFi ssid ' + str(ap_ssid) + ', default password: ' + str(ap_password))
    uart_write('and access the Pic W via your favorite web browser at 192.168.4.1.')
    uart_write('Listening on:' + str(addr))

    while True:
        if wlan_sta.isconnected():
            return True

        client, addr = server_socket.accept()
        uart_write('client connected from' + str(addr))
        try:
            client.settimeout(5.0)

            request = b""
            try:
                while "\r\n\r\n" not in request:
                    data = client.recv(512)
                    if not data:
                        break
                    request += data
            except OSError:
                pass

            uart_write("Request is: " + str(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            try:
                # Use a regular expression to extract the URL from the request
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
            uart_write("URL is " + str(url))

            if url == "":
                handle_root(client)
            elif url == "configure":
                uart_write("Handling configure")
                handle_configure(client, request)
            else:
                handle_not_found(client, url)

        finally:
            client.close()
