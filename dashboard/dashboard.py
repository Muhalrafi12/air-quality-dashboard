import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Beijing Air Quality Dashboard", page_icon="🌍", layout="wide")

# Set style seaborn
sns.set(style='dark')

# Fungsi Load Data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "air_quality_df.csv")
    
    data = pd.read_csv(file_path)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['date'] = data['datetime'].dt.date
    data['Hour'] = data['datetime'].dt.hour
    data['year'] = data['datetime'].dt.year
    data['month_year'] = data['datetime'].dt.strftime('%b %Y')
    return data

# Color mapping following IQAir standards
color_map = {
    'Good': '#00e400',
    'Moderate': '#ffff00',
    'Unhealthy for Sensitive Groups': '#ff7e00',
    'Unhealthy': '#ff0000',
    'Very Unhealthy': '#8f3f97',
    'Hazardous': '#7e0023'
}

# Health recommendations by category
health_recommendations = {
    'Good': 'Air quality is satisfactory, and air pollution poses little or no risk.',
    'Moderate': 'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.',
    'Unhealthy for Sensitive Groups': 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.',
    'Unhealthy': 'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.',
    'Very Unhealthy': 'Health alert: The risk of health effects is increased for everyone.',
    'Hazardous': 'Health warning of emergency conditions: everyone is more likely to be affected.'
}

# Load data
data = load_data()

# Calculate AQI and add categories
def calculate_aqi(row):
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    valid_values = [row[p] for p in pollutants if p in row and pd.notna(row[p])]
    return sum(valid_values) / len(valid_values) if valid_values else 0

def categorize_air_quality(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 150: return 'Unhealthy for Sensitive Groups'
    elif aqi <= 200: return 'Unhealthy'
    elif aqi <= 300: return 'Very Unhealthy'
    else: return 'Hazardous'

data['aqi'] = data.apply(calculate_aqi, axis=1)
data['Category'] = data['aqi'].apply(categorize_air_quality)

# ==================== HEADER ====================
st.title('🌍 Beijing Air Quality Dashboard')
st.markdown("**Comprehensive Analysis of Air Pollution Levels Across Beijing Districts (2013-2017)**")
st.markdown('---')

# ==================== SIDEBAR ====================
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://cdn0.iconfinder.com/data/icons/woman-avatar-with-mask-1/512/chinese_girl-_woman-_user-_avatar-_people-_mask-1024.png", width=100)
    
    st.header('🎛️ Filters')
    
    # Station filter
    selected_station = st.selectbox('Select Station', 
                                  ['All Stations'] + list(data['station'].unique()))
    
    # AQI Category filter
    selected_categories = st.selectbox('Select AQI Categories',
                                     ['Overall Category'] + list(color_map.keys()),
                                     key='aqi_category')
    
    # Hour filter
    selected_hour = st.selectbox('Select Hour', 
                               list(range(24)),
                               format_func=lambda x: f"{x:02d}:00")
    
    # Date range with fixed dates
    st.subheader('📅 Date Range')
    min_date = datetime(2013, 3, 1).date()
    max_date = datetime(2017, 2, 28).date()
    
    start_date = st.date_input('Start Date', 
                              min_date,
                              min_value=min_date,
                              max_value=max_date)
    
    end_date = st.date_input('End Date', 
                            max_date,
                            min_value=min_date,
                            max_value=max_date)

# Filter data based on all selections
filtered_data = data[
    (data['date'] >= start_date) & 
    (data['date'] <= end_date) &
    (data['Hour'] == selected_hour)
]

if selected_station != 'All Stations':
    filtered_data = filtered_data[filtered_data['station'] == selected_station]

if selected_categories != 'Overall Category':
    filtered_data = filtered_data[filtered_data['Category'] == selected_categories]

# ==================== CURRENT STATUS ====================
st.header('📊 Current Air Quality Status')
if not filtered_data.empty:
    latest_data = filtered_data.iloc[-1]
    latest_aqi = latest_data['aqi']
    latest_category = latest_data['Category']

    cols = st.columns(3)
    with cols[0]:
        st.metric('Average AQI', f"{latest_aqi:.1f}")
    with cols[1]:
        st.markdown(f"**Category:** <span style='color:{color_map[latest_category]}'>{latest_category}</span>", 
                   unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"**Station:** {selected_station}")

    st.info(f"ℹ️ {health_recommendations[latest_category]}")
else:
    st.warning("⚠️ No data available for the selected filters.")

st.markdown('---')

# ==================== POLLUTANT TRENDS ====================
st.markdown("<h2 style='text-align: center;'>📈 Pollutant Trends Over Time</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Peak levels of SO2, NO2, CO, and O3 across the observation period</p>", unsafe_allow_html=True)

if not filtered_data.empty:
    pollutants_trend = ['SO2', 'NO2', 'CO', 'O3']
    
    fig = go.Figure()
    
    for pollutant in pollutants_trend:
        monthly_data = filtered_data.groupby('month_year')[pollutant].mean().reset_index()
        
        fig.add_trace(go.Scatter(
            x=monthly_data['month_year'],
            y=monthly_data[pollutant],
            mode='lines+markers',
            name=pollutant,
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title='Trend Polutan SO2, NO2, CO, dan O3 per Periode Waktu',
        xaxis_title='Time Period (Month-Year)',
        yaxis_title='Concentration (μg/m³)',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Peak values summary
    st.subheader('🔝 Peak Values Summary')
    peak_cols = st.columns(4)
    for idx, pollutant in enumerate(pollutants_trend):
        with peak_cols[idx]:
            max_idx = filtered_data[pollutant].idxmax()
            max_value = filtered_data.loc[max_idx, pollutant]
            max_date = filtered_data.loc[max_idx, 'datetime'].strftime('%b %Y')
            st.metric(f"{pollutant} Peak", f"{max_value:.2f}", delta=max_date)

st.markdown('---')

# ==================== PM2.5 vs PM10 COMPARISON ====================
st.markdown("<h2 style='text-align: center;'>📉 PM2.5 vs PM10 Annual Comparison</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Yearly average comparison of particulate matter levels (2013-2017)</p>", unsafe_allow_html=True)

if not filtered_data.empty:
    yearly_avg = filtered_data.groupby('year').agg({
        'PM2.5': 'mean',
        'PM10': 'mean'
    }).reset_index()
    
    fig_pm = go.Figure()
    
    fig_pm.add_trace(go.Scatter(
        x=yearly_avg['year'],
        y=yearly_avg['PM2.5'],
        mode='lines+markers+text',
        name='PM2.5',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=12),
        text=[f"{val:.1f}" for val in yearly_avg['PM2.5']],
        textposition='bottom center',
        textfont=dict(size=10, color='#2ecc71')
    ))
    
    fig_pm.add_trace(go.Scatter(
        x=yearly_avg['year'],
        y=yearly_avg['PM10'],
        mode='lines+markers+text',
        name='PM10',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=12, symbol='square'),
        text=[f"{val:.1f}" for val in yearly_avg['PM10']],
        textposition='top center',
        textfont=dict(size=10, color='#e74c3c')
    ))
    
    fig_pm.update_layout(
        title='Perbandingan Rata-rata Tahunan PM2.5 dan PM10 (2013-2017)',
        xaxis_title='Year',
        yaxis_title='Concentration (µg/m³)',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_pm, use_container_width=True)
    
    # Comparison table
    st.subheader('📋 Yearly Comparison Table')
    yearly_avg['Difference'] = yearly_avg['PM10'] - yearly_avg['PM2.5']
    yearly_avg['PM2.5'] = yearly_avg['PM2.5'].round(2)
    yearly_avg['PM10'] = yearly_avg['PM10'].round(2)
    yearly_avg['Difference'] = yearly_avg['Difference'].round(2)
    st.dataframe(yearly_avg, use_container_width=True)

st.markdown('---')

# ==================== AIR QUALITY DISTRIBUTION ====================
st.markdown("<h2 style='text-align: center;'>🥧 Air Quality Distribution</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Overall air quality category breakdown (2013-2017)</p>", unsafe_allow_html=True)

if not filtered_data.empty:
    category_dist = filtered_data['Category'].value_counts()
    category_percentages = (category_dist / len(filtered_data) * 100).round(1)
    
    fig_dist = go.Figure(data=[go.Pie(
        labels=category_dist.index,
        values=category_dist.values,
        hole=0.3,
        marker=dict(colors=[color_map[cat] for cat in category_dist.index]),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig_dist.update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Category statistics
    st.subheader('📊 Category Statistics')
    stats_cols = st.columns(len(category_dist))
    for idx, (cat, count) in enumerate(category_dist.items()):
        with stats_cols[idx]:
            pct = category_percentages[cat]
            st.markdown(f"<div style='background-color:{color_map[cat]}; padding:10px; border-radius:5px; text-align:center;'>"
                       f"<h4 style='color:white; margin:0;'>{cat}</h4>"
                       f"<p style='color:white; margin:0;'>{count} ({pct}%)</p></div>", 
                       unsafe_allow_html=True)

st.markdown('---')

# ==================== DISTRICT COMPARISON ====================
st.markdown("<h2 style='text-align: center;'>🏙️ Air Quality by District</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Comparative analysis of air quality levels across Beijing districts</p>", unsafe_allow_html=True)

if not filtered_data.empty:
    district_quality = pd.crosstab(
        filtered_data['station'],
        filtered_data['Category'],
        normalize='index'
    ) * 100
    
    ordered_categories = [cat for cat in color_map.keys() if cat in district_quality.columns]
    district_quality = district_quality[ordered_categories]
    
    fig_district = go.Figure()
    
    for category in ordered_categories:
        fig_district.add_trace(go.Bar(
            name=category,
            x=district_quality.index,
            y=district_quality[category],
            marker_color=color_map[category],
            hovertemplate='<b>%{x}</b><br>' + category + ': %{y:.1f}%<extra></extra>'
        ))
    
    fig_district.update_layout(
        title='Air Quality Distribution by District (2013-2017)',
        xaxis_title='District',
        yaxis_title='Percentage (%)',
        barmode='stack',
        height=600,
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig_district.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_district, use_container_width=True)
    
    # Best and worst districts
    st.markdown("<h3 style='text-align: center;'>🏆 Best and Worst Districts</h3>", unsafe_allow_html=True)
    
    district_aqi = filtered_data.groupby('station')['aqi'].mean().sort_values()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success('**🌟 Healthiest Districts (Lowest AQI)**')
        for i, (district, aqi) in enumerate(district_aqi.head(3).items(), 1):
            st.write(f"{i}. **{district}**: {aqi:.2f}")
    
    with col2:
        st.error('**⚠️ Most Polluted Districts (Highest AQI)**')
        for i, (district, aqi) in enumerate(district_aqi.tail(3).iloc[::-1].items(), 1):
            st.write(f"{i}. **{district}**: {aqi:.2f}")

st.markdown('---')

# ==================== FOOTER ====================
st.markdown('---')
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p style='font-size: 14px;'>📊 <strong>Beijing Air Quality Dashboard</strong> | Data Period: March 2013 - February 2017</p>
    <p style='font-size: 12px;'>Created by Muhammad Ridwan Alrafi</p>
</div>
""", unsafe_allow_html=True)