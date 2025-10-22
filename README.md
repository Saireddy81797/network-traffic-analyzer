# 🛰️ NETWORK TRAFFIC ANALYZER & PERFORMANCE DASHBOARD

### Monitor and Visualize Real-Time Network Packets — Demo & Live Capture

---

## Overview
The **Network Traffic Analyzer** is a **Streamlit-based interactive dashboard** that allows you to **monitor, analyze, and visualize network traffic** in real-time or via sample datasets. This tool is perfect for **network analysis, anomaly detection, and protocol monitoring** in simulated or real-world scenarios.

---

## Features
- **Real-Time Simulation:** Simulate live packet capture and streaming updates.
- **Protocol Filtering:** Filter traffic by TCP, UDP, HTTP, HTTPS, DNS, SSH, FTP, ICMP.
- **IP Filtering:** Focus analysis on specific source or destination IP addresses.
- **Anomaly Detection:** Flags packets exceeding protocol-specific thresholds.
- **Interactive Charts:**
  - Protocol Usage Distribution
  - Bandwidth Over Time
- **Raw Packet Table:** Detailed packet info including timestamp, source/destination IP, protocol, length, and anomaly flags.
- **Protocol Icons:** Quick visual identification of protocols.
- **CSV Export:** Download filtered or captured traffic for offline analysis.
- **Custom Styling:** Gradient metric cards, highlighted anomalies, modern dashboard design.

---

## Technologies Used

Python 3.x
Streamlit
Pandas
Plotly
CSV handling and data visualization

---

## Demo
Experience the live demo of the **Network Traffic Analyzer** here:  
[🚀 Click Here to Open Live Demo](https://saireddy81797-network-traffic-analyzer-app-1ztz4t.streamlit.app/)

---

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/yourusername/network-traffic-analyzer.git
Navigate to the project folder:

cd network-traffic-analyzer


Install dependencies:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run app.py

Folder Structure
network-traffic-analyzer/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .gitignore
├── README.md
├── LICENSE
│
├── src/                    # Python modules
│   ├── __init__.py
│   ├── packet_capture.py
│   ├── packet_analysis.py
│   ├── visualizer.py
│   ├── utils.py
│
├── data/                   # Sample CSV data
│   └── sample_packets.csv
│
├── assets/                 # Assets like logo & CSS
│   ├── logo.png
│   └── styles.css

