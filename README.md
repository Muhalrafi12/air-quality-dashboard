# Air Quality Beijing Data Analysis - Dicoding

![Dashboard Preview](dashboard_aq.gif)

## Air Quality Dashboard Streamlit App
## Table of Contents
* [Overview](#overview)
* [Structure of Project](#structure-of-project)
* [Installation](#installation)
* [Usage](#usage)
* [Data Sources](#data-sources)
* [Key Insight](#key-insight)
* [Tools](#tools)
* [Author](#author)

## Overview
This project is a data analysis and visualization project focused on air quality data at 12 Districts in Beijing. The data analysis process includes Preparing data, Data Wrangling, Exploratory Data Analysis, Visualization & Explanatory Analysis, and Creating an Attractive Dashboard.

## Structure of Project
* `data/`: Directory containing the raw CSV data files.
* `notebook.py`: Python scripts for data wrangling, EDA, and answering analysis questions.
* `app.py`: The Streamlit dashboard application.
* `README.md`: This documentation file.

## Installation 
```bash
# Clone the repository
git clone https://github.com/yourusername/air-quality-analysis.git
# Install required packages
pip install -r requirements.txt
# Run the Streamlit dashboard
streamlit run app.py
```

## Usage
1. Data Wrangling: scripts are available in the dashboard_air_quality.py file to prepare and clean the data.
2. Exploratory Data Analysis (EDA): Explore and analyze the data using the provided Python scripts. EDA insights can guide your understanding of air quality patterns.
3. Visualization: Run the Streamlit dashboard for interactive data exploration:
streamlit run dashboard_air_quality.py
Access the dashboard in your web browser at http://localhost:8501.

## Data Sources
The dataset used in this project is from the Beijing Air Quality dataset:
* Original Source: [Beijing Air Quality Dataset](https://github.com/marceloreis/HTI) by Marcelo Reis (HTI: Hackathon da Carreiras TI - Positivo)
* Dataset provided through: Dicoding's Data Analysis with Python Final Project

## Key Insights
* Distrik yang memiliki kualitas udara terbaik yakni Dingling dan distrik kualitas udara terburuk berada di Wanshouxigong
* Rata-rata Average Pollutant Levels tertinggi adalah karbon monoksida(CO) dan terendah yaitu ozone(03)
* Terdapat korelasi positif kuat antara PM2.5 dan PM10 (0.88), CO memiliki korelasi positif sedang hingga kuat dengan PM2.5 (0.79) dan NO2 (0.71)

## Tools
Python 3.x
Streamlit
Pandas
Plotly
Matplotlib
Seaborn

## Author
Muhammad Ridwan Alrafi
