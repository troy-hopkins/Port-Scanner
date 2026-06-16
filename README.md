# 🛰️ Port Scanner

A simple TCP port scanner that checks a range of ports on a target IP address.

## ✨ Features
- Scans a user-defined port range on any specified IPv4 address
- Configurable timeout per port ⏱️
- Live "Scanning..." animation while running - first time using multi-threading!
- Reports open/closed status and total scan time
- Repeatable — scan again without restarting

## ⚙️ How It Works
For each port in the range, a TCP socket connection attempt is made; success means the port is open, a `socket.error` means it's closed. A background thread runs a loading animation while the scan completes.

## 🚀 Usage
```bash
python Port-Scanner-Main.py
```

## 🐍 Concepts Practised
Sockets, threading, exception handling, dictionaries, time tracking, input validation

## 📌 Status
Learning project, working and tested. For ethical use only — only scan devices you own or have permission to test ⚠️
