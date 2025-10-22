# app.py
import streamlit as st
import pandas as pd
import os

from src.packet_capture import simulate_live_packets
from src.packet_analysis import analyze_packets
from src.visualizer import plot_protocol_distribution, plot_bandwidth_over_time
from src.utils import filter_by_protocol, filter_by_ip

st.set_page_config(page_title="Network Traffic Analyzer", page_icon="🛰️", layout="wide")

# optional styles (if you have assets/styles.css)
if os.path.exists("assets/styles.css"):
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# header
st.image("assets/logo.png", width=100) if os.path.exists("assets/logo.png") else None
st.title("🛰️ Network Traffic Analyzer & Performance Dashboard")
st.write("Monitor and visualize simulated real-time network packets — demo and simulated live capture modes.")

# Sidebar controls
st.sidebar.header("🔍 Filters")
protocol_choice = st.sidebar.selectbox("Filter by Protocol", ["All", "TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "ICMP"])
ip_filter = st.sidebar.text_input("Filter by IP (src or dst)")

mode = st.radio("Select Mode:", ["Demo (sample data)", "Live Capture (simulated)"])

# Use session state to hold dataframe and run state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])
if "running" not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns([1, 3])
with col1:
    duration = st.slider("Capture Duration (seconds)", 5, 60, 15)
    start = st.button("▶️ Start Capture")
    stop = st.button("⏹️ Stop")
with col2:
    st.markdown("### Controls")
    st.write("Choose Demo to load the sample CSV, or Live Capture (simulated) for streaming data.")

# load demo
if start:
    st.session_state.running = True
    st.session_state.df = pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "protocol", "length"])

if stop:
    st.session_state.running = False

if mode == "Demo (sample data)":
    try:
        df = pd.read_csv("data/sample_packets.csv")
        st.session_state.df = df
    except Exception as e:
        st.error("Could not load sample_packets.csv: " + str(e))

# If running simulated live, iterate generator
if mode == "Live Capture (simulated)" and st.session_state.running:
    placeholder_table = st.empty()
    protocol_chart = st.empty()
    bandwidth_chart = st.empty()
    progress_bar = st.progress(0)

    for i, df in enumerate(simulate_live_packets(duration)):
        # update session dataframe
        st.session_state.df = df

        # apply filters
        filtered = filter_by_protocol(st.session_state.df, protocol_choice)
        filtered = filter_by_ip(filtered, ip_filter)

        # analysis and visuals
        summary, proto_summary = analyze_packets(filtered)

        # left: metrics and proto pie
        with st.container():
            st.markdown("## Network Summary")
            st.json(summary)
        protocol_fig = plot_protocol_distribution(proto_summary)
        bandwidth_fig = plot_bandwidth_over_time(filtered)

        placeholder_table.dataframe(filtered.tail(15), use_container_width=True)
        if protocol_fig:
            protocol_chart.plotly_chart(protocol_fig, use_container_width=True)
        if bandwidth_fig:
            bandwidth_chart.plotly_chart(bandwidth_fig, use_container_width=True)

        progress_bar.progress((i + 1) / duration)
        if not st.session_state.running:
            break

    st.success("Simulated live capture finished or stopped.")

# If demo mode (or not running live) show static dashboard
if not st.session_state.running:
    df_show = st.session_state.df.copy()
    # apply filters
    df_show = filter_by_protocol(df_show, protocol_choice)
    df_show = filter_by_ip(df_show, ip_filter)

    summary, proto_summary = analyze_packets(df_show)

    st.markdown("## Network Summary")
    st.json(summary)

    cols = st.columns(2)
    with cols[0]:
        st.markdown("### Protocol Usage")
        fig = plot_protocol_distribution(proto_summary)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    with cols[1]:
        st.markdown("### Bandwidth Over Time")
        fig2 = plot_bandwidth_over_time(df_show)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Raw Packets (latest)")
    st.dataframe(df_show.tail(40), use_container_width=True)
