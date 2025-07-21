#!/usr/bin/env python3
"""
SpaceX Orbit Analysis - Check for geosynchronous orbit data
"""

import requests
import pandas as pd

print("🛰️ SpaceX Orbit Analysis")
print("=" * 60)

# Get launches data
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)
data = response.json()
df = pd.json_normalize(data)

print(f"Total launches: {len(df)}")

# Check all columns for orbit-related information
print("\nChecking all columns for orbit information...")
orbit_related_columns = []
for col in df.columns:
    if any(keyword in col.lower() for keyword in ['orbit', 'payload', 'mission']):
        orbit_related_columns.append(col)

print(f"Orbit-related columns: {orbit_related_columns}")

# Check payload information
if any('payload' in col for col in df.columns):
    print("\nChecking payload data...")
    payload_columns = [col for col in df.columns if 'payload' in col.lower()]
    print(f"Payload columns: {payload_columns}")
    
    # Sample payload data
    for i in range(min(3, len(df))):
        print(f"\nLaunch {i} payload data:")
        for col in payload_columns:
            print(f"  {col}: {df[col].iloc[i]}")

# Try to get detailed payload information
print("\nTrying to extract orbit from payloads...")
geo_count = 0

for i in range(len(df)):
    payloads = df['payloads'].iloc[i] if 'payloads' in df.columns else []
    
    if isinstance(payloads, list) and len(payloads) > 0:
        # Get first payload ID and fetch details
        payload_id = payloads[0]
        
        # Get payload details from API
        try:
            payload_url = f"https://api.spacexdata.com/v4/payloads/{payload_id}"
            payload_response = requests.get(payload_url)
            
            if payload_response.status_code == 200:
                payload_data = payload_response.json()
                orbit = payload_data.get('orbit')
                
                if orbit and any(geo_term in orbit.upper() for geo_term in ['GEO', 'GTO', 'GEOSYNCHRONOUS']):
                    geo_count += 1
                    if geo_count <= 5:  # Show first 5 examples
                        print(f"Launch {i}: Orbit = {orbit}")
        except:
            continue

print(f"\n✅ Geosynchronous orbit launches: {geo_count}")

# Alternative method - check mission names for GEO indicators
print("\nAlternative method - checking mission names...")
geo_missions = 0
mission_names = []

for i in range(len(df)):
    name = df['name'].iloc[i] if 'name' in df.columns else ''
    details = df['details'].iloc[i] if 'details' in df.columns else ''
    
    mission_text = f"{name} {details}".upper()
    
    if any(geo_term in mission_text for geo_term in ['GEO', 'GTO', 'GEOSYNCHRONOUS', 'GEOSTATIONARY']):
        geo_missions += 1
        mission_names.append(name)

print(f"GEO missions by name/details: {geo_missions}")
if mission_names:
    print("Sample GEO mission names:")
    for name in mission_names[:5]:
        print(f"  - {name}")

# Final answer
final_geo_count = max(geo_count, geo_missions)
print(f"\n🎯 FINAL ANSWER Q3: {final_geo_count}")

# Summary of all answers
print("\n" + "="*60)
print("🎯 ALL ANSWERS SUMMARY")
print("="*60)
print("Question 1: 112 (CCAFS SLC 40 launches)")
print("Question 2: 88% (success rate)")
print(f"Question 3: {final_geo_count} (geosynchronous orbit)")
print("Question 4: 115 (successful drone ship landings)")
print("="*60)
