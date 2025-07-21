#!/usr/bin/env python3
"""
SpaceX API Re-check - Double verify answers for Q2 and Q3
"""

import requests
import pandas as pd
import json

print("🔍 SpaceX API Re-check - Verifying Q2 and Q3")
print("=" * 60)

# Get SpaceX launches data
print("\n📡 Fetching SpaceX API data...")
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.json_normalize(data)
print(f"✅ Retrieved {len(df)} total launches")

# Question 2: Re-check Falcon 9 count
print("\n" + "="*60)
print("QUESTION 2 RE-CHECK: Falcon 9 launches count")
print("="*60)

# Method 1: Check rocket names directly in launches
print("Method 1: Checking rocket field in launches...")
print(f"Sample rocket IDs: {df['rocket'].head().tolist()}")

# Get all rockets data
rocket_url = "https://api.spacexdata.com/v4/rockets"
rocket_response = requests.get(rocket_url)
rockets_data = rocket_response.json()

print(f"\nAll available rockets:")
for rocket in rockets_data:
    print(f"- {rocket['name']}: {rocket['id']}")

# Find ALL Falcon 9 variants
falcon9_rockets = [r for r in rockets_data if 'falcon 9' in r['name'].lower()]
falcon9_ids = [r['id'] for r in falcon9_rockets]
print(f"\nFalcon 9 rocket IDs: {falcon9_ids}")

# Count launches for each rocket type
rocket_counts = df['rocket'].value_counts()
print(f"\nLaunch counts by rocket ID:")
for rocket_id, count in rocket_counts.items():
    rocket_name = next((r['name'] for r in rockets_data if r['id'] == rocket_id), 'Unknown')
    print(f"- {rocket_name} ({rocket_id}): {count}")

# Total Falcon 9 launches
falcon9_launches = df[df['rocket'].isin(falcon9_ids)]
falcon9_count = len(falcon9_launches)
print(f"\n✅ TOTAL FALCON 9 LAUNCHES: {falcon9_count}")

# Question 3: Re-check landing pad missing values
print("\n" + "="*60)
print("QUESTION 3 RE-CHECK: Missing values in landingPad")
print("="*60)

# Method 1: Check if there's a direct landingPad column
print("Checking for direct landingPad columns...")
landing_columns = [col for col in df.columns if 'landing' in col.lower() or 'pad' in col.lower()]
print(f"Landing-related columns: {landing_columns}")

# Method 2: Detailed analysis of cores structure
print("\nDetailed cores analysis...")
print("Sample cores structures:")
for i in range(min(5, len(df))):
    cores = df['cores'].iloc[i]
    print(f"Launch {i}: {cores}")

# Method 3: Extract landing pad data with multiple approaches
print("\nExtracting landing pad data...")

# Approach A: Check cores[0]['landpad']
landpads_method_a = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list) and len(cores) > 0:
        first_core = cores[0]
        if isinstance(first_core, dict):
            landpad = first_core.get('landpad')
            landpads_method_a.append(landpad)
        else:
            landpads_method_a.append(None)
    else:
        landpads_method_a.append(None)

missing_a = pd.Series(landpads_method_a).isnull().sum()
print(f"Method A (cores[0]['landpad']): {missing_a} missing values")

# Approach B: Check all cores for any landing pad
landpads_method_b = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    has_landpad = False
    if isinstance(cores, list):
        for core in cores:
            if isinstance(core, dict) and core.get('landpad') is not None:
                has_landpad = True
                break
    landpads_method_b.append(None if not has_landpad else 'has_landpad')

missing_b = pd.Series(landpads_method_b).isnull().sum()
print(f"Method B (any core has landpad): {missing_b} missing values")

# Approach C: Check landing_attempt field
landing_attempts = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list) and len(cores) > 0:
        first_core = cores[0]
        if isinstance(first_core, dict):
            landing_attempt = first_core.get('landing_attempt', False)
            landpad = first_core.get('landpad')
            # If landing was attempted but no landpad, count as missing
            if landing_attempt and landpad is None:
                landing_attempts.append(None)
            elif not landing_attempt:
                landing_attempts.append('no_attempt')
            else:
                landing_attempts.append(landpad)
        else:
            landing_attempts.append(None)
    else:
        landing_attempts.append(None)

missing_c = pd.Series(landing_attempts).isnull().sum()
print(f"Method C (landing attempts with missing pads): {missing_c} missing values")

print(f"\n✅ MOST LIKELY ANSWER FOR Q3: {missing_a}")

# Summary
print("\n" + "="*60)
print("🎯 CORRECTED ANSWERS")
print("="*60)
print(f"Question 2: {falcon9_count}")
print(f"Question 3: {missing_a}")
print("="*60)
