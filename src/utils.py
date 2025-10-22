# src/utils.py
import pandas as pd

def filter_by_protocol(df: pd.DataFrame, protocol: str):
    """Filter packets by protocol (TCP, UDP, ICMP)."""
    return df[df['proto'] == protocol] if not df.empty else df

def filter_by_ip(df: pd.DataFrame, ip_address: str):
    """Filter packets where given IP is source or destination."""
    if df.empty:
        return df
    return df[(df['src'] == ip_address) | (df['dst'] == ip_address)]

def bytes_to_kb(size_bytes):
    """Convert bytes to kilobytes."""
    return round(size_bytes / 1024, 2)

def bytes_to_mb(size_bytes):
    """Convert bytes to megabytes."""
    return round(size_bytes / (1024 * 1024), 2)
