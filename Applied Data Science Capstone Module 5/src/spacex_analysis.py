#!/usr/bin/env python3
"""
SpaceX API Analysis Script
Answers questions about SpaceX launches using real API data
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from datetime import datetime

def install_required_packages():
    """Install required packages if needed"""
    import subprocess
    import sys
    
    packages = ['requests', 'pandas', 'beautifulsoup4', 'lxml']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Install packages if needed
try:
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
except ImportError:
    install_required_packages()
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup

print("🚀 SpaceX API Analysis Starting...")
print("=" * 50)

# Question 1: Get SpaceX API data and find first static_fire_date_utc year
print("\n📡 Question 1: Getting SpaceX API data...")

try:
    # Get SpaceX launches data
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully retrieved {len(data)} launches")
        
        # Convert to DataFrame using pd.json_normalize
        df = pd.json_normalize(data)
        print(f"✅ DataFrame created with {len(df)} rows and {len(df.columns)} columns")
        
        # Check if static_fire_date_utc column exists
        if 'static_fire_date_utc' in df.columns:
            # Get first row's static_fire_date_utc
            first_static_fire = df['static_fire_date_utc'].iloc[0]
            if pd.notna(first_static_fire):
                # Extract year from the date
                year = pd.to_datetime(first_static_fire).year
                print(f"✅ First row static_fire_date_utc year: {year}")
            else:
                print("❌ First row static_fire_date_utc is null")
                # Find first non-null value
                first_non_null = df['static_fire_date_utc'].dropna().iloc[0] if not df['static_fire_date_utc'].dropna().empty else None
                if first_non_null:
                    year = pd.to_datetime(first_non_null).year
                    print(f"✅ First non-null static_fire_date_utc year: {year}")
        else:
            print("❌ Column 'static_fire_date_utc' not found")
            print("Available columns:", list(df.columns))
    else:
        print(f"❌ API request failed with status code: {response.status_code}")

except Exception as e:
    print(f"❌ Error in Question 1: {e}")

# Question 2: Count Falcon 9 launches (excluding Falcon 1)
print("\n🚀 Question 2: Counting Falcon 9 launches...")

try:
    # Filter for Falcon 9 launches only
    if 'rocket' in df.columns:
        # Get rocket details
        rocket_url = "https://api.spacexdata.com/v4/rockets"
        rocket_response = requests.get(rocket_url)
        
        if rocket_response.status_code == 200:
            rockets_data = rocket_response.json()
            rockets_df = pd.json_normalize(rockets_data)
            
            # Find Falcon 9 rocket ID
            falcon9_rockets = rockets_df[rockets_df['name'].str.contains('Falcon 9', case=False, na=False)]
            falcon9_ids = falcon9_rockets['id'].tolist()
            
            # Count launches with Falcon 9 rockets
            falcon9_launches = df[df['rocket'].isin(falcon9_ids)]
            falcon9_count = len(falcon9_launches)
            
            print(f"✅ Total Falcon 9 launches: {falcon9_count}")
        else:
            print("❌ Could not get rocket data")
    else:
        print("❌ Rocket column not found in launches data")

except Exception as e:
    print(f"❌ Error in Question 2: {e}")

# Question 3: Count missing values in landingPad column
print("\n🛬 Question 3: Checking missing values in landingPad...")

try:
    # Method 1: Check for direct landing pad columns
    landing_pad_columns = [col for col in df.columns if 'landing' in col.lower() and 'pad' in col.lower()]

    if landing_pad_columns:
        for col in landing_pad_columns:
            missing_count = df[col].isnull().sum()
            print(f"✅ Missing values in {col}: {missing_count}")
    else:
        # Method 2: Extract from cores data
        if 'cores' in df.columns:
            print("Extracting landing pad data from cores...")

            # Flatten cores data to get all landing pads
            all_landing_pads = []

            for idx, row in df.iterrows():
                cores = row['cores']
                if pd.notna(cores) and isinstance(cores, list) and len(cores) > 0:
                    # Get landing pad from first core (most common case)
                    first_core = cores[0]
                    if isinstance(first_core, dict):
                        landing_pad = first_core.get('landing_pad', None)
                        all_landing_pads.append(landing_pad)
                    else:
                        all_landing_pads.append(None)
                else:
                    all_landing_pads.append(None)

            # Count missing values
            landing_pad_series = pd.Series(all_landing_pads)
            missing_count = landing_pad_series.isnull().sum()
            total_count = len(landing_pad_series)

            print(f"✅ Total launches: {total_count}")
            print(f"✅ Missing values in landingPad: {missing_count}")
            print(f"✅ Non-missing values: {total_count - missing_count}")

        else:
            print("❌ No cores column found")
            print("Available columns:", [col for col in df.columns if any(keyword in col.lower() for keyword in ['land', 'pad', 'core'])])

except Exception as e:
    print(f"❌ Error in Question 3: {e}")
    import traceback
    traceback.print_exc()

# Question 4: Web scraping Falcon 9 Wikipedia page
print("\n🌐 Question 4: Scraping Falcon 9 Wikipedia page...")

try:
    wiki_url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
    wiki_response = requests.get(wiki_url)
    
    if wiki_response.status_code == 200:
        soup = BeautifulSoup(wiki_response.content, 'html.parser')
        title_tag = soup.title
        print(f"✅ soup.title output: {title_tag}")
        
        # Also show the string content
        if title_tag:
            print(f"✅ Title text: {title_tag.string}")
    else:
        print(f"❌ Wikipedia request failed with status code: {wiki_response.status_code}")

except Exception as e:
    print(f"❌ Error in Question 4: {e}")

print("\n" + "=" * 50)
print("🎯 Analysis Complete!")
print("\nSummary of Answers:")
print("Question 1: Check the year output above")
print("Question 2: Check the Falcon 9 count above") 
print("Question 3: Check the missing values count above")
print("Question 4: Check the soup.title output above")
