#!/usr/bin/env python3
"""
Simple SpaceX API Analysis - Get exact answers
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

print("🚀 SpaceX API Analysis - Getting Exact Answers")
print("=" * 60)

# Get SpaceX launches data
print("\n📡 Fetching SpaceX API data...")
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.json_normalize(data)
print(f"✅ Retrieved {len(df)} launches")

# Question 1: First row static_fire_date_utc year
print("\n" + "="*60)
print("QUESTION 1: First row static_fire_date_utc year")
print("="*60)

if 'static_fire_date_utc' in df.columns:
    first_date = df['static_fire_date_utc'].iloc[0]
    if pd.notna(first_date):
        year = pd.to_datetime(first_date).year
        print(f"✅ ANSWER: {year}")
    else:
        print("First row is null, checking first non-null...")
        first_non_null = df['static_fire_date_utc'].dropna()
        if len(first_non_null) > 0:
            year = pd.to_datetime(first_non_null.iloc[0]).year
            print(f"✅ ANSWER: {year}")
else:
    print("❌ Column not found")

# Question 2: Falcon 9 launches count
print("\n" + "="*60)
print("QUESTION 2: Falcon 9 launches count")
print("="*60)

# Get rocket data
rocket_url = "https://api.spacexdata.com/v4/rockets"
rocket_response = requests.get(rocket_url)
rockets_data = rocket_response.json()
rockets_df = pd.json_normalize(rockets_data)

# Find Falcon 9 rocket IDs
falcon9_rockets = rockets_df[rockets_df['name'].str.contains('Falcon 9', case=False, na=False)]
falcon9_ids = falcon9_rockets['id'].tolist()
print(f"Falcon 9 rocket IDs: {falcon9_ids}")

# Count Falcon 9 launches
falcon9_launches = df[df['rocket'].isin(falcon9_ids)]
falcon9_count = len(falcon9_launches)
print(f"✅ ANSWER: {falcon9_count}")

# Question 3: Missing values in landingPad
print("\n" + "="*60)
print("QUESTION 3: Missing values in landingPad")
print("="*60)

# Check cores data structure
print("Checking cores data structure...")
sample_cores = df['cores'].iloc[0]
print(f"Sample cores data: {sample_cores}")

# Extract landing pad data safely
landing_pads = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]

    # Handle different data types
    if cores is None or (isinstance(cores, float) and pd.isna(cores)):
        landing_pads.append(None)
    elif isinstance(cores, list) and len(cores) > 0:
        # Get first core's landing pad (check both possible names)
        first_core = cores[0]
        if isinstance(first_core, dict):
            # Try both 'landpad' and 'landing_pad'
            landpad = first_core.get('landpad') or first_core.get('landing_pad')
            landing_pads.append(landpad)
        else:
            landing_pads.append(None)
    else:
        landing_pads.append(None)

# Count missing values
landing_pad_series = pd.Series(landing_pads)
missing_count = landing_pad_series.isnull().sum()
total_count = len(landing_pad_series)

print(f"Total launches: {total_count}")
print(f"Missing landing pads: {missing_count}")
print(f"Non-missing landing pads: {total_count - missing_count}")
print(f"✅ ANSWER: {missing_count}")

# Question 4: Wikipedia soup.title
print("\n" + "="*60)
print("QUESTION 4: Wikipedia soup.title")
print("="*60)

wiki_url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
wiki_response = requests.get(wiki_url)
soup = BeautifulSoup(wiki_response.content, 'html.parser')
title_tag = soup.title

print(f"✅ ANSWER: {title_tag}")

# Summary
print("\n" + "="*60)
print("🎯 FINAL ANSWERS SUMMARY")
print("="*60)
print(f"Question 1: {year if 'year' in locals() else 'Check above'}")
print(f"Question 2: {falcon9_count}")
print(f"Question 3: {missing_count}")
print(f"Question 4: {title_tag}")
print("="*60)
