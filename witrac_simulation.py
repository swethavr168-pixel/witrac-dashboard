"""
WITRAC - Wildlife Tracking System
Indian Star Tortoise Monitoring Dashboard
Version: 7.0 (Production Ready)
Author: WITRAC Team
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import os

# ===================== PAGE CONFIGURATION =====================
st.set_page_config(
    page_title="WITRAC - Wildlife Tracking System",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/witrac',
        'Report a bug': 'https://github.com/yourusername/witrac/issues',
        'About': "# WITRAC - Wildlife Tracking System\nVersion 7.0\nMonitoring Indian Star Tortoises with Energy Harvesting Tags"
    }
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
    /* Professional Color Scheme */
    :root {
        --primary: #2E7D32;
        --secondary: #81C784;
        --danger: #F44336;
        --warning: #FFC107;
        --info: #2196F3;
        --dark: #2c3e50;
        --light: #f8f9fa;
    }
    
    /* Main header with gradient */
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 1.8rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Status badges */
    .badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .badge-excellent { background: #4CAF50; color: white; }
    .badge-normal { background: #FFC107; color: black; }
    .badge-critical { background: #F44336; color: white; animation: blink 1s infinite; }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid var(--primary);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Alert boxes */
    .alert-critical {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid var(--danger);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        animation: slideIn 0.3s ease-out;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 5px solid var(--warning);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: var(--light);
        padding: 0.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(46, 125, 50, 0.1);
        transform: translateY(-1px);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
        padding: 0.5rem 1.5rem;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background: var(--dark);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 10px;
    }
    
    /* Divider styling */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        margin: 2rem 0;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        animation: slideDown 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ===================== INITIALIZE SESSION STATE =====================
def initialize_session_state():
    """Initialize all session state variables"""
    
    if 'initialized' not in st.session_state:
        # Pre-fill 24-hour historical data for demo
        historical_data = []
        base_time = datetime.now() - timedelta(hours=24)
        
        for i in range(24):
            time_point = base_time + timedelta(hours=i)
            # Simulate diurnal pattern
            hour = time_point.hour
            activity_base = 30 + 40 * np.sin((hour - 6) * np.pi / 12)  # Peak at noon
            temp_base = 28 + 6 * np.sin((hour - 12) * np.pi / 12)  # Peak at 2pm
            
            historical_data.append({
                "timestamp": time_point,
                "battery": 70 + 20 * np.sin(i / 12 * np.pi),
                "temperature": temp_base + random.uniform(-1, 1),
                "activity": max(10, min(90, activity_base + random.uniform(-10, 10))),
                "hydration": 65 + 15 * np.sin((i + 6) / 12 * np.pi),
                "condition": 60 + 10 * np.sin(i / 12 * np.pi)
            })
        
        # Realistic tortoise names with personality
        tortoise_profiles = [
            {"name": "Chitra", "pattern": "diurnal", "speed": 0.03, "color": "#4CAF50"},
            {"name": "Bheem", "pattern": "diurnal", "speed": 0.05, "color": "#2196F3"},
            {"name": "Raj", "pattern": "crepuscular", "speed": 0.02, "color": "#FF9800"},
            {"name": "Mini", "pattern": "diurnal", "speed": 0.04, "color": "#E91E63"},
            {"name": "Tuffy", "pattern": "crepuscular", "speed": 0.03, "color": "#9C27B0"}
        ]
        
        animals = []
        base_lat, base_lon = 12.9, 80.2
        
        for i, profile in enumerate(tortoise_profiles, 1):
            animal = {
                "ID": f"TORT_{i:03d}",
                "Name": profile["name"],
                "Color": profile["color"],
                "Latitude": base_lat + random.uniform(-0.03, 0.03),
                "Longitude": base_lon + random.uniform(-0.03, 0.03),
                "Battery": random.randint(75, 95),
                "Temperature": round(random.uniform(29, 34), 2),
                "Signal": random.randint(3, 5),
                "Activity": random.randint(40, 85),
                "Hydration": random.randint(60, 90),
                "LastUpdate": datetime.now(),
                "Speed": profile["speed"],
                "PathHistory": [],
                "DailyPattern": profile["pattern"],
                "MovementDirection": random.uniform(0, 360),
                "TotalDistance": 0.0,
                "LastPosition": None
            }
            
            # Initialize path
            animal["PathHistory"] = [(animal["Latitude"], animal["Longitude"])] * 10
            animal["LastPosition"] = (animal["Latitude"], animal["Longitude"])
            
            # Calculate body condition
            temp_score = max(0, min(100, ((animal["Temperature"] - 28) / 7 * 100)))
            animal["BodyCondition"] = round(
                (animal["Activity"] * 0.35 + animal["Hydration"] * 0.45 + temp_score * 0.2), 2
            )
            
            # Set status
            if animal["BodyCondition"] >= 75:
                animal["Status"] = "EXCELLENT"
            elif animal["BodyCondition"] >= 50:
                animal["Status"] = "NORMAL"
            else:
                animal["Status"] = "CRITICAL"
            
            animals.append(animal)
        
        st.session_state.animals = animals
        st.session_state.historical_data = historical_data
        st.session_state.alert_history = []
        st.session_state.last_alert_check = {}
        st.session_state.update_counter = 0
        st.session_state.initialized = True
        st.session_state.last_update = datetime.now()
        st.session_state.auto_refresh = False
        st.session_state.map_key = 0  # For forcing map refresh

# Initialize session
initialize_session_state()

# ===================== UTILITY FUNCTIONS =====================
def calculate_distance(pos1, pos2):
    """Calculate distance between two coordinates"""
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) * 111  # Rough km conversion

def get_health_status(value, thresholds):
    """Get health status based on thresholds"""
    if value < thresholds['critical']:
        return "CRITICAL", "🔴"
    elif value < thresholds['warning']:
        return "WARNING", "⚠️"
    else:
        return "GOOD", "✅"

def format_timestamp(dt):
    """Format timestamp for display"""
    return dt.strftime("%H:%M:%S")

# ===================== DATA UPDATE FUNCTION =====================
def update_animal_data():
    """Update all animal data with realistic simulation"""
    current_time = datetime.now()
    new_alerts = []
    
    for animal in st.session_state.animals:
        hour = current_time.hour
        
        # Activity based on pattern
        if animal["DailyPattern"] == "diurnal":
            activity_mult = 1.2 if 6 <= hour <= 18 else 0.3
        else:  # crepuscular
            activity_mult = 1.0 if (5 <= hour <= 7) or (17 <= hour <= 19) else 0.5
        
        # Movement
        old_pos = (animal["Latitude"], animal["Longitude"])
        angle_rad = np.radians(animal["MovementDirection"])
        
        # Change direction occasionally
        if random.random() < 0.05:
            animal["MovementDirection"] += random.uniform(-30, 30)
        
        # Move
        movement = animal["Speed"] * activity_mult * 0.001
        animal["Latitude"] += np.cos(angle_rad) * movement
        animal["Longitude"] += np.sin(angle_rad) * movement
        
        # Keep in bounds
        animal["Latitude"] = np.clip(animal["Latitude"], 12.85, 12.95)
        animal["Longitude"] = np.clip(animal["Longitude"], 80.15, 80.25)
        
        # Update distance
        new_pos = (animal["Latitude"], animal["Longitude"])
        animal["TotalDistance"] += calculate_distance(old_pos, new_pos)
        
        # Update path
        path = list(animal["PathHistory"])
        path.append(new_pos)
        if len(path) > 20:
            path.pop(0)
        animal["PathHistory"] = path
        
        # Battery simulation
        if 6 <= hour <= 18:
            animal["Battery"] = min(100, animal["Battery"] + random.uniform(0.1, 0.2))
        else:
            animal["Battery"] = max(0, animal["Battery"] - random.uniform(0.05, 0.1))
        
        # Temperature variation
        temp_variation = np.sin((hour - 14) * np.pi / 12) * 2
        animal["Temperature"] = round(31 + temp_variation + random.uniform(-0.3, 0.3), 2)
        
        # Activity
        base_activity = 50
        animal["Activity"] = np.clip(
            base_activity + (activity_mult - 1) * 30 + random.randint(-5, 5),
            0, 100
        )
        
        # Hydration
        if activity_mult > 0.8:
            animal["Hydration"] = max(0, animal["Hydration"] - random.uniform(0.2, 0.4))
        else:
            animal["Hydration"] = min(100, animal["Hydration"] + random.uniform(0.1, 0.2))
        
        animal["LastUpdate"] = current_time
        
        # Body condition
        temp_score = max(0, min(100, ((animal["Temperature"] - 28) / 7 * 100)))
        animal["BodyCondition"] = round(
            (animal["Activity"] * 0.35 + animal["Hydration"] * 0.45 + temp_score * 0.2), 2
        )
        
        # Status
        if animal["BodyCondition"] >= 75:
            animal["Status"] = "EXCELLENT"
        elif animal["BodyCondition"] >= 50:
            animal["Status"] = "NORMAL"
        else:
            animal["Status"] = "CRITICAL"
        
        # Check alerts
        animal_id = animal["ID"]
        alerts = []
        
        if animal["Battery"] < st.session_state.get('battery_threshold', 30):
            alerts.append(("🔋 Low Battery", f"{animal['Battery']:.1f}%", "warning"))
        
        temp_min = st.session_state.get('temp_min', 28)
        temp_max = st.session_state.get('temp_max', 35)
        if animal["Temperature"] < temp_min or animal["Temperature"] > temp_max:
            alerts.append(("🌡️ Abnormal Temp", f"{animal['Temperature']}°C", "critical"))
        
        if animal["Activity"] < st.session_state.get('activity_threshold', 20):
            alerts.append(("📉 Low Activity", str(animal['Activity']), "warning"))
        
        if animal["Hydration"] < st.session_state.get('hydration_threshold', 40):
            alerts.append(("💧 Low Hydration", f"{animal['Hydration']}%", "warning"))
        
        # New alerts
        last_check = st.session_state.last_alert_check.get(animal_id, [])
        for alert in alerts:
            if alert not in last_check:
                new_alerts.append({
                    "type": alert[0],
                    "animal": animal["Name"],
                    "value": alert[1],
                    "severity": alert[2],
                    "time": current_time
                })
        
        st.session_state.last_alert_check[animal_id] = alerts
    
    # Update alert history
    if new_alerts:
        st.session_state.alert_history.extend(new_alerts)
        st.session_state.alert_history = st.session_state.alert_history[-100:]
    
    # Update historical data
    snapshot = {
        "timestamp": current_time,
        "battery": np.mean([a["Battery"] for a in st.session_state.animals]),
        "temperature": np.mean([a["Temperature"] for a in st.session_state.animals]),
        "activity": np.mean([a["Activity"] for a in st.session_state.animals]),
        "hydration": np.mean([a["Hydration"] for a in st.session_state.animals]),
        "condition": np.mean([a["BodyCondition"] for a in st.session_state.animals])
    }
    
    st.session_state.historical_data.append(snapshot)
    if len(st.session_state.historical_data) > 500:
        st.session_state.historical_data = st.session_state.historical_data[-500:]
    
    st.session_state.last_update = current_time
    st.session_state.map_key += 1  # Force map refresh

# ===================== SIDEBAR =====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/turtle.png", width=100)
    st.title("🎮 Control Panel")
    
    # Update mode with tooltips
    st.markdown("### 🔄 Update Mode")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Manual", use_container_width=True,
                    help="Click to switch to manual update mode",
                    type="secondary" if st.session_state.auto_refresh else "primary"):
            st.session_state.auto_refresh = False
            st.rerun()
    with col2:
        if st.button("⚡ Auto", use_container_width=True,
                    help="Enable automatic updates",
                    type="primary" if st.session_state.auto_refresh else "secondary"):
            st.session_state.auto_refresh = True
            st.rerun()
    
    # Manual refresh button
    st.markdown("---")
    if st.button("🔄 REFRESH DATA", use_container_width=True, type="primary",
                 help="Click to manually update all sensor data"):
        st.session_state.update_counter += 1
        st.rerun()
    
    # Auto-refresh interval
    if st.session_state.auto_refresh:
        refresh_interval = st.select_slider(
            "Refresh Interval",
            options=["2 sec", "5 sec", "10 sec", "30 sec"],
            value="5 sec",
            help="How often to automatically refresh data"
        )
        st.caption(f"🔄 Auto-refreshing every {refresh_interval}")
    
    st.markdown("---")
    
    # Map settings
    st.markdown("### 🗺️ Map Settings")
    show_clusters = st.checkbox("Show Clusters", value=False,
                                help="Group nearby markers together")
    show_paths = st.checkbox("Show Paths", value=True,
                            help="Display animal movement trails")
    map_height = st.slider("Map Height", 400, 800, 500, step=50,
                          help="Adjust map display height")
    
    st.markdown("---")
    
    # Alert thresholds
    st.markdown("### ⚠️ Alert Thresholds")
    col1, col2 = st.columns(2)
    with col1:
        battery_threshold = st.slider("🔋 Battery", 0, 100, 30,
                                     help="Alert when battery below %",
                                     key="battery_threshold")
        temp_min = st.slider("🌡️ Min Temp", 20, 40, 28,
                            help="Minimum safe temperature",
                            key="temp_min")
        activity_threshold = st.slider("📊 Activity", 0, 100, 20,
                                      help="Alert when activity below",
                                      key="activity_threshold")
    with col2:
        hydration_threshold = st.slider("💧 Hydration", 0, 100, 40,
                                       help="Alert when hydration below %",
                                       key="hydration_threshold")
        temp_max = st.slider("🌡️ Max Temp", 20, 40, 35,
                            help="Maximum safe temperature",
                            key="temp_max")
    
    st.markdown("---")
    
    # System status
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Updates", st.session_state.update_counter,
                 help="Number of data updates")
        st.metric("Data Points", len(st.session_state.historical_data),
                 help="Historical data points stored")
    with col2:
        active_alerts = len([a for a in st.session_state.alert_history
                            if a.get('time', datetime.now()) > datetime.now() - timedelta(minutes=30)])
        st.metric("Active Alerts", active_alerts,
                 help="Alerts in last 30 minutes")
        st.metric("Animals", 5, help="Total animals tracked")
    
    # Reset button
    st.markdown("---")
    if st.button("⚠️ RESET SYSTEM", use_container_width=True,
                 help="Reset all data to initial state"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ===================== UPDATE DATA =====================
if st.session_state.update_counter > 0 or st.session_state.auto_refresh:
    update_animal_data()

df_animals = pd.DataFrame(st.session_state.animals)

# ===================== HEADER =====================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin:0; font-size: 2.5rem;">🐢 WITRAC</h1>
            <p style="margin:5px 0 0; opacity: 0.9; font-size: 1.1rem;">
                Wildlife Tracking System - Indian Star Tortoise Monitoring
            </p>
        </div>
        <div style="text-align: right;">
            <div class="tooltip">
                <span style="font-size: 1.2rem;">⚡ Energy Harvesting</span>
                <span class="tooltiptext">Solar: 80-100 mAh/day<br>Kinetic: 1-3 mAh/day</span>
            </div>
            <p style="margin:5px 0 0; opacity: 0.8;">Last: {}</p>
        </div>
    </div>
</div>
""".format(st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# ===================== METRICS ROW =====================
st.markdown("### 📊 Live System Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_battery = df_animals['Battery'].mean()
    st.metric("🔋 Avg Battery", f"{avg_battery:.1f}%",
             help="Average battery level across all animals")

with col2:
    avg_temp = df_animals['Temperature'].mean()
    st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C",
             delta=f"{avg_temp-31.5:+.1f}°C",
             delta_color="inverse",
             help="Average shell temperature")

with col3:
    avg_activity = df_animals['Activity'].mean()
    st.metric("📊 Avg Activity", f"{avg_activity:.1f}",
             help="Average activity index")

with col4:
    avg_hydration = df_animals['Hydration'].mean()
    st.metric("💧 Avg Hydration", f"{avg_hydration:.1f}%",
             help="Average hydration level")

with col5:
    avg_condition = df_animals['BodyCondition'].mean()
    st.metric("❤️ Body Condition", f"{avg_condition:.1f}",
             help="Average body condition score (0-100)")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ===================== MAIN TABS =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Live Tracking Map",
    "📋 Detailed Sensor Data",
    "📈 Analytics Dashboard",
    "📥 Export & Reports"
])

# ===================== TAB 1: LIVE MAP =====================
with tab1:
    map_col, alert_col = st.columns([2.5, 1])
    
    with map_col:
        st.markdown("### 🗺️ Real-time Animal Locations")
        
        # Create map with single instance
        m = folium.Map(location=[12.9, 80.2], zoom_start=13, control_scale=True)
        folium.TileLayer('OpenStreetMap').add_to(m)
        
        # Add marker layer
        if show_clusters:
            marker_cluster = MarkerCluster().add_to(m)
            target_layer = marker_cluster
        else:
            target_layer = m
        
        # Add paths
        if show_paths:
            for animal in st.session_state.animals:
                points = animal["PathHistory"]
                if len(points) > 1:
                    if animal['BodyCondition'] >= 75:
                        color = '#4CAF50'
                    elif animal['BodyCondition'] >= 50:
                        color = '#FFC107'
                    else:
                        color = '#F44336'
                    
                    folium.PolyLine(
                        points,
                        weight=2,
                        color=color,
                        opacity=0.6,
                        tooltip=f"{animal['Name']}'s path"
                    ).add_to(m)
        
        # Add markers
        for _, row in df_animals.iterrows():
            if row['BodyCondition'] >= 75:
                color = 'green'
            elif row['BodyCondition'] >= 50:
                color = 'orange'
            else:
                color = 'red'
            
            # Create popup
            popup_html = f"""
            <div style="font-family: Arial; width: 300px;">
                <div style="background: {row['Color']}; color: white; padding: 10px; border-radius: 8px 8px 0 0;">
                    <h4 style="margin:0;">🐢 {row['Name']}</h4>
                    <p style="margin:5px 0 0;">ID: {row['ID']}</p>
                </div>
                <div style="padding: 12px; background: white;">
                    <table style="width:100%;">
                        <tr><td>🔋 Battery:</td><td><b>{row['Battery']:.1f}%</b></td>
                            <td>{'✅' if row['Battery']>30 else '⚠️'}</td></tr>
                        <tr><td>🌡️ Temp:</td><td><b>{row['Temperature']}°C</b></td>
                            <td>{'✅' if 28<=row['Temperature']<=35 else '⚠️'}</td></tr>
                        <tr><td>📊 Activity:</td><td><b>{row['Activity']}</b></td>
                            <td>{'✅' if row['Activity']>20 else '⚠️'}</td></tr>
                        <tr><td>💧 Hydration:</td><td><b>{row['Hydration']}%</b></td>
                            <td>{'✅' if row['Hydration']>40 else '⚠️'}</td></tr>
                        <tr><td>❤️ Condition:</td><td colspan="2"><b>{row['BodyCondition']}</b></td></tr>
                    </table>
                    <p style="margin:10px 0 0; color: gray; font-size:0.8em;">
                        Updated: {row['LastUpdate'].strftime('%H:%M:%S')}
                    </p>
                </div>
            </div>
            """
            
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=350),
                icon=folium.Icon(color=color, icon='info-sign'),
                tooltip=f"{row['Name']} - {row['Status']}"
            ).add_to(target_layer)
        
        # Display map with unique key
        folium_static(m, width=800, height=map_height)
    
    with alert_col:
        st.markdown("### ⚠️ Live Alerts")
        
        # Recent alerts
        recent_alerts = [a for a in st.session_state.alert_history
                        if a.get('time', datetime.now()) > datetime.now() - timedelta(hours=1)]
        
        if recent_alerts:
            for alert in recent_alerts[-8:]:
                if alert['severity'] == 'critical':
                    st.markdown(f"""
                    <div class="alert-critical">
                        <strong>{alert['type']}</strong><br>
                        {alert['animal']}: {alert['value']}<br>
                        <small>⏱️ {alert['time'].strftime('%H:%M:%S')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-warning">
                        <strong>{alert['type']}</strong><br>
                        {alert['animal']}: {alert['value']}<br>
                        <small>⏱️ {alert['time'].strftime('%H:%M:%S')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("✅ All systems normal - No active alerts")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active", len(df_animals[df_animals['Activity'] > 50]))
            st.metric("Excellent Health", len(df_animals[df_animals['BodyCondition'] > 75]))
        with col2:
            st.metric("Low Battery", len(df_animals[df_animals['Battery'] < 30]))
            st.metric("Needs Attention", len(df_animals[df_animals['BodyCondition'] < 50]))

# ===================== TAB 2: DETAILED DATA =====================
with tab2:
    st.markdown("### 📋 Detailed Sensor Data")
    
    # Prepare data for display
    display_df = df_animals[[
        'Name', 'Battery', 'Temperature', 'Activity', 'Hydration',
        'BodyCondition', 'Status', 'Signal', 'TotalDistance', 'LastUpdate'
    ]].copy()
    
    display_df['LastUpdate'] = display_df['LastUpdate'].apply(lambda x: x.strftime('%H:%M:%S'))
    display_df['TotalDistance'] = display_df['TotalDistance'].apply(lambda x: f"{x:.2f} km")
    


    # Color coding
def color_cells(val):
    try:
        if float(val) < 30:
            return 'background-color: #ff4b4b; color: white'
        elif float(val) < 60:
            return 'background-color: #ffa500; color: white'
        else:
            return 'background-color: #90EE90'
    except:
        return ''

# Apply styling
styled_df = display_df.style.map(color_cells)

# Display
st.dataframe(styled_df, use_container_width=True, height=350)
    # Summary stats
st.markdown("### 📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**Battery Distribution**")
    fig = px.pie(values=[len(df_animals[df_animals['Battery']>70]),
                             len(df_animals[(df_animals['Battery']<=70) & (df_animals['Battery']>30)]),
                             len(df_animals[df_animals['Battery']<=30])],
                     names=['Good (>70%)', 'Fair (30-70%)', 'Critical (<30%)'],
                     color_discrete_sequence=['#4CAF50', '#FFC107', '#F44336'])
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.markdown("**Health Status**")
    fig = px.pie(values=[len(df_animals[df_animals['Status']=='EXCELLENT']),
                             len(df_animals[df_animals['Status']=='NORMAL']),
                             len(df_animals[df_animals['Status']=='CRITICAL'])],
                     names=['Excellent', 'Normal', 'Critical'],
                     color_discrete_sequence=['#4CAF50', '#2196F3', '#F44336'])
    st.plotly_chart(fig, use_container_width=True)
    
with col3:
    st.markdown("**Activity Levels**")
    fig = px.bar(df_animals, x='Name', y='Activity',
                    color='Activity',
                    color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
with col4:
    st.markdown("**Temperature Range**")
    fig = px.box(df_animals, y='Temperature',
                    title='Temperature Distribution',
                    points='all')
    fig.add_hline(y=temp_min, line_dash="dash", line_color="red")
    fig.add_hline(y=temp_max, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

# ===================== TAB 3: ANALYTICS =====================
with tab3:
    st.markdown("### 📈 Advanced Analytics")
    
    if len(st.session_state.historical_data) > 10:
        hist_df = pd.DataFrame(st.session_state.historical_data)
        
        # Time range selector
        range_options = ["Last Hour", "Last 6 Hours", "Last 12 Hours", "Last 24 Hours", "All"]
        selected_range = st.select_slider("Time Range", options=range_options, value="Last 24 Hours")
        
        # Filter data
        now = datetime.now()
        if selected_range == "Last Hour":
            plot_df = hist_df[hist_df['timestamp'] > now - timedelta(hours=1)]
        elif selected_range == "Last 6 Hours":
            plot_df = hist_df[hist_df['timestamp'] > now - timedelta(hours=6)]
        elif selected_range == "Last 12 Hours":
            plot_df = hist_df[hist_df['timestamp'] > now - timedelta(hours=12)]
        elif selected_range == "Last 24 Hours":
            plot_df = hist_df[hist_df['timestamp'] > now - timedelta(hours=24)]
        else:
            plot_df = hist_df
        
        # Multi-tab analytics
        anal_tab1, anal_tab2, anal_tab3, anal_tab4 = st.tabs([
            "📊 Time Series", "📉 Distributions", "🔄 Correlations", "📋 Health Matrix"
        ])
        
        with anal_tab1:
            # Multi-axis time series
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=plot_df['timestamp'], y=plot_df['activity'],
                mode='lines', name='Activity',
                line=dict(color='#2ecc71', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=plot_df['timestamp'], y=plot_df['temperature'],
                mode='lines', name='Temperature',
                line=dict(color='#e74c3c', width=2),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Scatter(
                x=plot_df['timestamp'], y=plot_df['hydration'],
                mode='lines', name='Hydration',
                line=dict(color='#3498db', width=2, dash='dot'),
                yaxis='y3'
            ))
            
            fig.update_layout(
                title='Multi-Parameter Trends',
                xaxis_title='Time',
                yaxis=dict(title='Activity', title_font=dict(color='#2ecc71')),
                yaxis2=dict(title='Temperature (°C)', title_font=dict(color='#e74c3c'),
                           overlaying='y', side='right'),
                yaxis3=dict(title='Hydration (%)', title_font=dict(color='#3498db'),
                           overlaying='y', side='right', position=0.95),
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Individual charts
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(plot_df, x='timestamp', y='activity',
                             title='Activity Trend',
                             color_discrete_sequence=['#2ecc71'])
                fig.add_hline(y=50, line_dash="dash", line_color="gray")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(plot_df, x='timestamp', y='temperature',
                             title='Temperature Trend',
                             color_discrete_sequence=['#e74c3c'])
                fig.add_hrect(y0=temp_min, y1=temp_max,
                             line_width=0, fillcolor="green", opacity=0.1)
                st.plotly_chart(fig, use_container_width=True)
        
        with anal_tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Activity distribution
                fig = px.histogram(plot_df, x='activity', nbins=30,
                                  title='Activity Distribution',
                                  color_discrete_sequence=['#2ecc71'],
                                  marginal='box')
                fig.add_vline(x=50, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
                
                # Hydration distribution
                fig = px.histogram(plot_df, x='hydration', nbins=30,
                                  title='Hydration Distribution',
                                  color_discrete_sequence=['#3498db'],
                                  marginal='box')
                fig.add_vline(x=70, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Temperature distribution
                fig = px.histogram(plot_df, x='temperature', nbins=30,
                                  title='Temperature Distribution',
                                  color_discrete_sequence=['#e74c3c'],
                                  marginal='box')
                fig.add_vline(x=temp_min, line_dash="dash", line_color="red")
                fig.add_vline(x=temp_max, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
                
                # Battery distribution
                fig = px.histogram(plot_df, x='battery', nbins=30,
                                  title='Battery Distribution',
                                  color_discrete_sequence=['#f39c12'],
                                  marginal='box')
                fig.add_vline(x=30, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with anal_tab3:
            st.markdown("#### 🔄 Correlation Analysis")
            
            if len(plot_df) > 20:
                # Correlation matrix
                corr_cols = ['activity', 'temperature', 'hydration', 'battery', 'condition']
                corr_df = plot_df[corr_cols].corr()
                
                fig = px.imshow(corr_df,
                               text_auto='.2f',
                               aspect="auto",
                               color_continuous_scale='RdBu_r',
                               title='Parameter Correlations',
                               zmin=-1, zmax=1)
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter matrix
                st.markdown("#### 📊 Multi-Parameter Relationships")
                fig = px.scatter_matrix(plot_df[corr_cols],
                                       dimensions=corr_cols,
                                       color='condition',
                                       color_continuous_scale='Viridis',
                                       title='Scatter Matrix')
                fig.update_traces(diagonal_visible=False)
                fig.update_layout(height=700)
                st.plotly_chart(fig, use_container_width=True)
                
                # Key insights
                st.markdown("#### 🔍 Key Insights")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    act_temp_corr = corr_df.loc['activity', 'temperature']
                    st.metric("Activity vs Temperature", f"{act_temp_corr:.2f}")
                
                with col2:
                    hyd_act_corr = corr_df.loc['hydration', 'activity']
                    st.metric("Hydration vs Activity", f"{hyd_act_corr:.2f}")
                
                with col3:
                    bat_cond_corr = corr_df.loc['battery', 'condition']
                    st.metric("Battery vs Condition", f"{bat_cond_corr:.2f}")
            else:
                st.info("Need more data points for correlation analysis")
        
        with anal_tab4:
            st.markdown("#### 📋 Health Assessment Matrix")
            
            # Current health status
            health_matrix = []
            for animal in st.session_state.animals:
                health_matrix.append({
                    'Name': animal['Name'],
                    'Battery': get_health_status(animal['Battery'],
                                                {'critical': 30, 'warning': 50})[1],
                    'Temperature': get_health_status(animal['Temperature'],
                                                    {'critical': temp_min, 'warning': temp_max})[1],
                    'Activity': get_health_status(animal['Activity'],
                                                 {'critical': 20, 'warning': 40})[1],
                    'Hydration': get_health_status(animal['Hydration'],
                                                  {'critical': 40, 'warning': 60})[1],
                    'Overall': animal['Status']
                })
            
            health_df = pd.DataFrame(health_matrix)
            st.dataframe(health_df, use_container_width=True, height=150)
            
            # Radar chart
            st.markdown("#### 📊 Individual Health Profiles")
            
            fig = go.Figure()
            categories = ['Battery', 'Temperature', 'Activity', 'Hydration', 'Condition']
            
            for animal in st.session_state.animals:
                values = [
                    animal['Battery']/20,
                    ((animal['Temperature'] - 20) / 20) * 5,
                    animal['Activity']/20,
                    animal['Hydration']/20,
                    animal['BodyCondition']/20
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=animal['Name'],
                    line=dict(color=animal['Color'])
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("📊 Collecting data... Click refresh to build analytics")

# ===================== TAB 4: EXPORT =====================
with tab4:
    st.markdown("### 📥 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📄 Current Snapshot")
        
        # CSV Download
        csv = df_animals.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"witrac_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="csv_download"
        )
        
        # Excel format
        st.download_button(
            label="📥 Download Excel",
            data=csv,
            file_name=f"witrac_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True,
            key="excel_download"
        )
    
    with col2:
        st.markdown("#### 📊 Historical Data")
        if len(st.session_state.historical_data) > 0:
            hist_export = pd.DataFrame(st.session_state.historical_data)
            hist_csv = hist_export.to_csv(index=False)
            
            st.download_button(
                label="📥 Download History",
                data=hist_csv,
                file_name=f"witrac_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="history_download"
            )
            
            st.caption(f"Records: {len(hist_export)}")
            st.caption(f"From: {hist_export['timestamp'].min().strftime('%Y-%m-%d %H:%M')}")
            st.caption(f"To: {hist_export['timestamp'].max().strftime('%Y-%m-%d %H:%M')}")
        else:
            st.info("No historical data yet")
    
    with col3:
        st.markdown("#### 📋 Comprehensive Report")
        
        # Generate report
        report = f"""WITRAC WILDLIFE TRACKING SYSTEM - COMPREHENSIVE REPORT
===========================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: 7.0 (Production)

SYSTEM OVERVIEW
===========================================================
Total Updates: {st.session_state.update_counter}
Data Points: {len(st.session_state.historical_data)}
Active Alerts: {active_alerts}
Auto-Refresh: {'Enabled' if st.session_state.auto_refresh else 'Disabled'}

CURRENT SNAPSHOT ({datetime.now().strftime('%H:%M:%S')})
===========================================================
Average Battery: {avg_battery:.1f}%
Average Temperature: {avg_temp:.1f}°C
Average Activity: {avg_activity:.1f}
Average Hydration: {avg_hydration:.1f}%
Average Body Condition: {avg_condition:.1f}

ANIMAL DETAILS
===========================================================
{df_animals.to_string(index=False)}

ALERT HISTORY (Last 10)
===========================================================
{chr(10).join([f"{a['time'].strftime('%H:%M:%S')} - {a['type']} - {a['animal']}: {a['value']}" 
               for a in st.session_state.alert_history[-10:]])}

ENERGY HARVESTING SYSTEM
===========================================================
Solar Panels: 50x35mm Monocrystalline (5V)
Daily Harvest: 80-100 mAh @ 3.7V
Kinetic Generator: 1-3 mAh/day
Battery: 150 mAh LiPo
Power Management: BQ25570

SENSORS ACTIVE
===========================================================
• TMP117 - Shell Temperature (±0.1°C)
• LIS3DH - 3-Axis Accelerometer
• MAX30001 - Bioimpedance (Hydration/Fat)

COMMUNICATION
===========================================================
• LoRa SX1276 - Long Range (2hr packets)
• BLE - Local Monitoring
• Gateway: LoRaWAN → The Things Network

END OF REPORT
===========================================================
"""
        
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name=f"witrac_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="report_download"
        )
        
        st.caption("Comprehensive system report with all details")
        
        # System info
        with st.expander("ℹ️ System Information"):
            st.markdown("""
            **WITRAC - Wildlife Tracking System**
            
            **Target Species:** Indian Star Tortoise
            **Tag Size:** 50×35×12mm
            **Tag Weight:** <5% of animal weight
            
            **Features:**
            - Energy Harvesting (Solar + Kinetic)
            - Real-time GPS Tracking
            - Health Monitoring
            - LoRaWAN Communication
            
            **Deployment Options:**
            1. Local: `streamlit run witrac_final.py`
            2. Cloud: Streamlit Community Cloud
            3. Docker: Available on request
            """)

# ===================== AUTO-REFRESH =====================
if st.session_state.auto_refresh:
    if 'refresh_interval' in locals():
        seconds = int(refresh_interval.split()[0])
        time.sleep(seconds)
        st.rerun()

# ===================== FOOTER =====================
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; max-width: 1200px; margin: 0 auto;">
        <div>
            <h3 style="margin:0;">🐢 WITRAC</h3>
            <p style="margin:10px 0 0; opacity: 0.9;">Wireless Wildlife Tracking System</p>
        </div>
        <div>
            <p style="margin:0;">⚡ Energy Harvesting Tags</p>
            <p style="margin:5px 0; opacity: 0.9;">📡 LoRaWAN Connected</p>
            <p style="margin:5px 0 0; opacity: 0.9;">🌡️ Real-time Health Monitoring</p>
        </div>
        <div>
            <p style="margin:0;">© 2024 WITRAC</p>
            <p style="margin:5px 0 0; opacity: 0.9;">Version 7.0 (Production)</p>
            <p style="margin:5px 0 0; opacity: 0.8;">Indian Star Tortoise Conservation</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Success message if just updated
if st.session_state.update_counter > 0:
    st.toast(f"✅ Data updated successfully! (Update #{st.session_state.update_counter})", icon="🐢")
