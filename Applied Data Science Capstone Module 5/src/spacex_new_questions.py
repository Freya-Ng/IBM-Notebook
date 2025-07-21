#!/usr/bin/env python3
"""
SpaceX API Analysis - New Questions
"""

import requests
import pandas as pd

print("🚀 SpaceX API Analysis - New Questions")
print("=" * 60)

# Get SpaceX launches data
print("\n📡 Fetching SpaceX API data...")
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.json_normalize(data)
print(f"✅ Retrieved {len(df)} total launches")

# Get launchpads data for Question 1
print("\n📍 Fetching launchpads data...")
launchpads_url = "https://api.spacexdata.com/v4/launchpads"
launchpads_response = requests.get(launchpads_url)
launchpads_data = launchpads_response.json()
launchpads_df = pd.json_normalize(launchpads_data)

print("Available launchpads:")
for pad in launchpads_data:
    print(f"- {pad['name']} ({pad['id']}): {pad['full_name']}")

# Question 1: How many launches came from CCAFS SLC 40?
print("\n" + "="*60)
print("QUESTION 1: Launches from CCAFS SLC 40")
print("="*60)

# Find CCAFS SLC 40 launchpad ID
ccafs_slc40 = None
for pad in launchpads_data:
    if 'CCAFS SLC 40' in pad['name'] or 'SLC-40' in pad['name'] or 'SLC 40' in pad['name']:
        ccafs_slc40 = pad['id']
        print(f"Found CCAFS SLC 40: {pad['name']} ({pad['id']})")
        break

if ccafs_slc40:
    ccafs_launches = df[df['launchpad'] == ccafs_slc40]
    ccafs_count = len(ccafs_launches)
    print(f"✅ ANSWER Q1: {ccafs_count}")
else:
    # Try alternative search
    print("Searching for SLC-40 alternatives...")
    for pad in launchpads_data:
        if '40' in pad['name'] and ('SLC' in pad['name'] or 'CCAFS' in pad['name']):
            print(f"Alternative: {pad['name']} ({pad['id']})")
            alt_launches = df[df['launchpad'] == pad['id']]
            print(f"Launches from {pad['name']}: {len(alt_launches)}")

# Question 2: What was the success rate?
print("\n" + "="*60)
print("QUESTION 2: Success rate")
print("="*60)

total_launches = len(df)
successful_launches = len(df[df['success'] == True])
success_rate = (successful_launches / total_launches) * 100

print(f"Total launches: {total_launches}")
print(f"Successful launches: {successful_launches}")
print(f"Success rate: {success_rate:.1f}%")
print(f"✅ ANSWER Q2: {success_rate:.0f}%")

# Question 3: How many launches went to geosynchronous orbit?
print("\n" + "="*60)
print("QUESTION 3: Launches to geosynchronous orbit")
print("="*60)

# Check orbit information
print("Checking orbit data...")
if 'orbit' in df.columns:
    orbit_counts = df['orbit'].value_counts()
    print("Orbit distribution:")
    for orbit, count in orbit_counts.items():
        print(f"- {orbit}: {count}")
    
    # Look for GEO, GTO, or geosynchronous variants
    geo_orbits = df[df['orbit'].str.contains('GEO|GTO|geosynchronous', case=False, na=False)]
    geo_count = len(geo_orbits)
    print(f"✅ ANSWER Q3: {geo_count}")
else:
    print("No direct orbit column found, checking other fields...")
    # Check if orbit info is in other columns
    orbit_columns = [col for col in df.columns if 'orbit' in col.lower()]
    print(f"Orbit-related columns: {orbit_columns}")

# Question 4: How many missions successfully landed to a drone ship?
print("\n" + "="*60)
print("QUESTION 4: Successful drone ship landings")
print("="*60)

# Check cores data for landing information
drone_ship_landings = 0
landing_details = []

for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list):
        for core in cores:
            if isinstance(core, dict):
                landing_type = core.get('landing_type')
                landing_success = core.get('landing_success')
                
                if landing_type and landing_success:
                    landing_details.append({
                        'landing_type': landing_type,
                        'landing_success': landing_success
                    })
                    
                    # Check for drone ship landing
                    if 'ASDS' in str(landing_type) or 'drone' in str(landing_type).lower():
                        if landing_success:
                            drone_ship_landings += 1

print("Landing type distribution:")
landing_df = pd.DataFrame(landing_details)
if not landing_df.empty:
    landing_summary = landing_df.groupby(['landing_type', 'landing_success']).size().reset_index(name='count')
    for _, row in landing_summary.iterrows():
        print(f"- {row['landing_type']} (Success: {row['landing_success']}): {row['count']}")

print(f"✅ ANSWER Q4: {drone_ship_landings}")

# Alternative method for Q4 - check landing platform names
print("\nAlternative method - checking landing platforms...")
asds_landings = 0
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list):
        for core in cores:
            if isinstance(core, dict):
                landing_success = core.get('landing_success')
                landpad = core.get('landpad')
                
                if landing_success and landpad:
                    # Get landpad details
                    # This would require another API call to get landpad names
                    pass

print(f"Alternative count (ASDS): {asds_landings}")

# Summary
print("\n" + "="*60)
print("🎯 FINAL ANSWERS")
print("="*60)
print(f"Question 1: {ccafs_count if 'ccafs_count' in locals() else 'Check above'}")
print(f"Question 2: {success_rate:.0f}%")
print(f"Question 3: {geo_count if 'geo_count' in locals() else 'Check above'}")
print(f"Question 4: {drone_ship_landings}")
print("="*60)
