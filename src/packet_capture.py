# src/packet_capture.py
import pandas as pd
import random
import time

def simulate_live_packets(duration=10):
    """Simulate incremental packet stream for 'duration' seconds.
       Yields the cumulative DataFrame each second.
    """
    protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "ICMP"]
    data = []
    for second in range(duration):
        # simulate variable packet count per second
        count = random.randint(5, 12)
        for _ in range(count):
            pkt = {
                "timestamp": time.strftime("%H:%M:%S"),
                "src_ip": f"192.168.{random.randint(0,3)}.{random.randint(2,254)}",
                "dst_ip": f"172.16.{random.randint(0,3)}.{random.randint(1,254)}",
                "protocol": random.choice(protocols),
                "length": random.randint(64, 1500)
            }
            data.append(pkt)
        yield pd.DataFrame(data)
        time.sleep(1)
