import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Improve performance with caching
@st.cache_data
def load_data():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwu_kEGTyY-xaOXcOfyPKuo9HaYK1qcIku9eUS7xv2Yui_xNlt_hegutcC1IsUT_OZI7uXhNXrQS66/pub?output=csv'
    data = pd.read_csv(url)
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    data['date'] = data['datetime'].dt.date
    data['Hour'] = data['datetime'].dt.hour
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

# UI Setup
st.title('Beijing Air Quality Dashboard')

# Sidebar filters
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://cdn0.iconfinder.com/data/icons/woman-avatar-with-mask-1/512/chinese_girl-_woman-_user-_avatar-_people-_mask-1024.png"
                 , width=100)
    with col3:
        st.write(' ')
    st.header('Filters')
    
    # Station filter
    selected_station = st.selectbox('Select Station', 
                                  ['All Stations'] + list(data['station'].unique()))
    
    # AQI Category filter - updated to match station filter style
    selected_categories = st.selectbox('Select AQI Categories',
                                     ['Overall Category'] + list(color_map.keys()),
                                     key='aqi_category')
    
    # Hour filter
    selected_hour = st.selectbox('Select Hour', 
                               list(range(24)),
                               format_func=lambda x: f"{x:02d}:00")
    
    # Date range with fixed dates
    st.subheader('Date Range')
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

# 1. Average AQI Status
st.header('Average Air Quality Status')
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

    # Health recommendations
    st.info(health_recommendations[latest_category])
else:
    st.warning("No data available for the selected filters.")

# 2. Pollutant Breakdown
st.header('Pollutant Levels')
if not filtered_data.empty:
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    latest_pollutants = latest_data[pollutants]

    fig_pollutants = go.Figure()
    for pollutant in pollutants:
        fig_pollutants.add_trace(go.Bar(
            name=pollutant,
            x=[pollutant],
            y=[latest_pollutants[pollutant]],
            text=[f"{latest_pollutants[pollutant]:.1f}"],
            textposition='auto',
        ))

    fig_pollutants.update_layout(
        title='Average Pollutant Levels',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_pollutants, use_container_width=True)


# 3. Historical Trends
st.header('Historical Trends')
if not filtered_data.empty:
    # Daily average AQI trend
    daily_aqi = filtered_data.groupby('date')['aqi'].mean().reset_index()
    fig_trend = px.line(
        daily_aqi,
        x='date',
        y='aqi',
        title='Daily Average AQI Trend'
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

# 4. Weather Impact
st.header('Weather Impact Analysis')

if not filtered_data.empty:
    # Wind direction impact
    wind_data = filtered_data.groupby(['wd', 'Category']).size().reset_index(name='count')
    fig_wind = go.Figure()
    
    # Check if we're using overall category or specific category
    categories_to_plot = list(color_map.keys()) if selected_categories == 'Overall Category' else [selected_categories]
    
    for category in categories_to_plot:
        category_data = wind_data[wind_data['Category'] == category]
        if not category_data.empty:
            fig_wind.add_trace(go.Barpolar(
                r=category_data['count'],
                theta=category_data['wd'],
                name=category,
                marker_color=color_map[category]
            ))
    
    fig_wind.update_layout(
        title='Air Quality by Wind Direction',
        height=400,
        showlegend=True,
        polar=dict(
            radialaxis=dict(showticklabels=True, ticks=''),
            angularaxis=dict(direction="clockwise")
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    st.plotly_chart(fig_wind, use_container_width=True)
    
    # Temperature impact
    fig_temp = px.scatter(
        filtered_data,
        x='TEMP',
        y='aqi',
        color='Category',
        title='AQI vs Temperature',
        color_discrete_map=color_map
    )
    fig_temp.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=True
    )
    st.plotly_chart(fig_temp, use_container_width=True)

# 5. Category Distribution
st.header('Air Quality Category Distribution')
if not filtered_data.empty:
    category_dist = filtered_data['Category'].value_counts()
    fig_dist = px.pie(
        values=category_dist.values,
        names=category_dist.index,
        title='Distribution of Air Quality Categories',
        color=category_dist.index,
        color_discrete_map=color_map
    )
    fig_dist.update_layout(height=400)
    st.plotly_chart(fig_dist, use_container_width=True)