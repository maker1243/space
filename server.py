#!/usr/bin/env python3
"""
SALVAGE STATION — Local LAN Server
Serves salvage_station.html so other devices on the same network can join.

Usage:
    python server.py            # default port 8080
    python server.py 3000       # custom port
"""
import http.server
import socketserver
import socket
import sys
import os
import webbrowser
from pathlib import Path

# Force UTF-8 stdout on Windows so unicode chars print without crashing.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8080))
DIRECTORY = str(Path(__file__).parent.resolve())


def get_lan_ips():
    """Return list of likely LAN IPs (not 127.0.0.1)."""
    ips = []
    # Primary: connect to a public IP to find outbound interface
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    # All interfaces
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip not in ips and not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    return ips


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Disable caching so edits reload
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Quieter log
        sys.stdout.write("  %s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


def main():
    os.chdir(DIRECTORY)
    # Bind on all interfaces so LAN devices can reach it
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        BAR = "=" * 62
        print(BAR)
        print("  SALVAGE STATION - LOCAL SERVER")
        print(BAR)
        print(f"  Directory: {DIRECTORY}")
        print(f"  Port:      {PORT}")
        print()
        print("  Open on THIS device:")
        print(f"     http://localhost:{PORT}/salvage_station.html")
        print()
        lan_ips = get_lan_ips()
        if lan_ips:
            print("  Share with OTHER devices on the SAME Wi-Fi / LAN:")
            for ip in lan_ips:
                print(f"     http://{ip}:{PORT}/salvage_station.html")
        else:
            print("  (No LAN IP detected — check network connection)")
        print()
        print("  Tips:")
        print("   - Other devices must be on the same Wi-Fi / router.")
        print("   - Windows Firewall may prompt to allow Python — click ALLOW.")
        print("   - Ctrl+C to stop.")
        print(BAR)
        # Auto-open browser on this device
        try:
            webbrowser.open(f"http://localhost:{PORT}/salvage_station.html")
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
