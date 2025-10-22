# src/packet_capture.py
from scapy.all import sniff, IP, TCP, UDP, ICMP
import pandas as pd
import time

def capture_packets(duration=10):
    """Capture network packets for a given duration (in seconds)."""
    packets = sniff(timeout=duration)
    data = []
    for pkt in packets:
        if IP in pkt:
            proto = 'OTHER'
            if TCP in pkt:
                proto = 'TCP'
            elif UDP in pkt:
                proto = 'UDP'
            elif ICMP in pkt:
                proto = 'ICMP'
            data.append({
                'timestamp': time.strftime('%H:%M:%S', time.localtime(pkt.time)),
                'src': pkt[IP].src,
                'dst': pkt[IP].dst,
                'proto': proto,
                'length': len(pkt)
            })
    return pd.DataFrame(data)
