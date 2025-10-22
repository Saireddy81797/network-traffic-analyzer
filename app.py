# app.py
import streamlit as st
import pandas as pd
import os

from src.packet_capture import simulate_live_packets
from src.packet_analysis import analyze_packets
from src.visualizer import plot_protocol_distribution, plot_bandwidth_over_time
from src.utils import filter_by_protocol, filter_by_ip

# ------------------- Page Config -------------------
st.set_page_config(page_title="Network Traffic Analyzer", page_icon="🛰️", layout="wide")

# ------------------- Styles -------------------
if os.path.exists("assets/styles.css"):
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------- Header -------------------
if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=100)
st.title("🛰️ Network Traffic Analyzer & Performance Dashboard")
st.write("Monitor and visualize simulated real-time network packets — demo and simulated live capture modes.")

# ------------------- Sidebar Filters -------------------
st.sidebar.header("🔍 Filters")
protocol_choice = st.sidebar.selectbox(
    "Filter by Protocol",
    ["All", "TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "ICMP"]
)
ip_filter = st.sidebar.text_input("Filter by IP (src or dst)")
mode = st.radio("Select Mode:", ["Demo (sample data)", "Live Capture (simulated)"])

# ------------------- Session State -------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])
if "running" not in st.session_state:
    st.session_state.running = False

# ------------------- Controls -------------------
col1, col2 = st.columns([1, 3])
with col1:
    duration = st.slider("Capture Duration (seconds)", 5, 60, 15)
    start = st.button("▶️ Start Capture")
    stop = st.button("⏹️ Stop")
with col2:
    st.markdown("### Controls")
    st.write("Choose Demo to load the sample CSV, or Live Capture (simulated) for streaming data.")

# ------------------- Start/Stop Capture -------------------
if start:
    st.session_state.running = True
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])

if stop:
    st.session_state.running = False

# ------------------- Load Demo Data -------------------
if mode == "Demo (sample data)":
    try:
        df_demo = pd.read_csv("data/sample_packets.csv")
        st.session_state.df = df_demo
    except Exception as e:
        st.error("Could not load sample_packets.csv: " + str(e))

# ------------------- Anomaly Detection -------------------
THRESHOLDS = {
    "TCP": 1500,
    "UDP": 1200,
    "HTTP": 2000,
    "HTTPS": 2000,
    "DNS": 512,
    "SSH": 1200,
    "FTP": 2000,
    "ICMP": 1500
}

def detect_anomalies(df):
    df['length'] = pd.to_numeric(df['length'], errors='coerce').fillna(0)
    df['anomaly'] = df.apply(lambda row: row['length'] > THRESHOLDS.get(row['protocol'], 1500), axis=1)
    return df

def highlight_anomalies(row):
    return ['background-color: #FFB6C1' if row.anomaly else '' for _ in row]

# Protocol icons
PROTOCOL_ICONS = {
    "TCP": "🌐",
    "UDP": "📡",
    "HTTP": "🌍",
    "HTTPS": "🔒",
    "DNS": "🧭",
    "SSH": "🔑",
    "FTP": "📁",
    "ICMP": "📶"
}

# ------------------- Function to Display Dashboard -------------------
def display_dashboard(df_input):
    if df_input.empty:
        st.info("No packets to display.")
        return

    filtered_df = filter_by_protocol(df_input, protocol_choice)
    filtered_df = filter_by_ip(filtered_df, ip_filter)

    # Detect anomalies
    filtered_df = detect_anomalies(filtered_df)
    filtered_df['protocol_icon'] = filtered_df['protocol'].map(PROTOCOL_ICONS).fillna("❓")

    # Analysis
    summary, proto_summary = analyze_packets(filtered_df)

    # Metrics cards
    total_packets = len(filtered_df)
    total_anomalies = filtered_df['anomaly'].sum()
    protocols_used = filtered_df['protocol'].nunique()
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="metric-card">📦 Total Packets<br>{total_packets}</div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card">⚠️ Anomalies<br>{total_anomalies}</div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card">🧩 Protocols<br>{protocols_used}</div>', unsafe_allow_html=True)

    # Show anomaly summary
    if total_anomalies > 0:
        st.warning(f"⚠️ {total_anomalies} anomalous packet(s) detected.")

    # Plots side by side
    plot_cols = st.columns(2)
    with plot_cols[0]:
        st.markdown("### Protocol Usage")
        proto_fig = plot_protocol_distribution(proto_summary)
        if proto_fig:
            st.plotly_chart(proto_fig, use_container_width=True)
    with plot_cols[1]:
        st.markdown("### Bandwidth Over Time")
        bw_fig = plot_bandwidth_over_time(filtered_df)
        if bw_fig:
            st.plotly_chart(bw_fig, use_container_width=True)

    # Raw packets table
    st.markdown("### Raw Packets (latest)")
    st.dataframe(
        filtered_df[['protocol_icon','timestamp','src_ip','dst_ip','protocol','length','anomaly']]
            .tail(40)
            .style.apply(highlight_anomalies, axis=1),
        use_container_width=True
    )

    # CSV Export
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="network_traffic.csv",
        mime="text/csv"
    )

# ------------------- Run Dashboard -------------------
if mode == "Live Capture (simulated)" and st.session_state.running:
    placeholder_table = st.empty()
    protocol_chart = st.empty()
    bandwidth_chart = st.empty()
    progress_bar = st.progress(0)

    for i, df_live in enumerate(simulate_live_packets(duration)):
        st.session_state.df = df_live
        display_dashboard(st.session_state.df)
        progress_bar.progress((i + 1) / duration)
        if not st.session_state.running:
            break
    st.success("Simulated live capture finished or stopped.")
else:
    display_dashboard(st.session_state.df)
