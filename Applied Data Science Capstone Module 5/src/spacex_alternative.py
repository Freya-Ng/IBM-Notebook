#!/usr/bin/env python3
"""
SpaceX API Alternative Analysis - Try different interpretations
"""

import requests
import pandas as pd

print("🔄 SpaceX API Alternative Analysis")
print("=" * 60)

# Get data
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)
data = response.json()
df = pd.json_normalize(data)

print(f"Total launches: {len(df)}")

# Question 2 Alternative: Maybe they want ONLY successful Falcon 9?
print("\n" + "="*60)
print("QUESTION 2 ALTERNATIVES")
print("="*60)

# Get rocket data
rocket_url = "https://api.spacexdata.com/v4/rockets"
rockets = requests.get(rocket_url).json()
falcon9_id = next(r['id'] for r in rockets if r['name'] == 'Falcon 9')

# Alternative 1: All Falcon 9 (current answer)
falcon9_all = df[df['rocket'] == falcon9_id]
print(f"Alt 1 - All Falcon 9 launches: {len(falcon9_all)}")

# Alternative 2: Only successful Falcon 9
falcon9_success = df[(df['rocket'] == falcon9_id) & (df['success'] == True)]
print(f"Alt 2 - Successful Falcon 9 launches: {len(falcon9_success)}")

# Alternative 3: Exclude Falcon 1 from total (not just count Falcon 9)
falcon1_id = next(r['id'] for r in rockets if r['name'] == 'Falcon 1')
non_falcon1 = df[df['rocket'] != falcon1_id]
falcon9_from_non_falcon1 = non_falcon1[non_falcon1['rocket'] == falcon9_id]
print(f"Alt 3 - Falcon 9 after removing Falcon 1: {len(falcon9_from_non_falcon1)}")

# Alternative 4: Maybe they want total non-Falcon 1 launches?
print(f"Alt 4 - All non-Falcon 1 launches: {len(non_falcon1)}")

# Question 3 Alternative: Different ways to count missing landingPad
print("\n" + "="*60)
print("QUESTION 3 ALTERNATIVES")
print("="*60)

# Alternative 1: Current method (cores[0]['landpad'])
landpads_1 = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list) and len(cores) > 0:
        landpad = cores[0].get('landpad')
        landpads_1.append(landpad)
    else:
        landpads_1.append(None)

missing_1 = pd.Series(landpads_1).isnull().sum()
print(f"Alt 1 - Missing landpad (current): {missing_1}")

# Alternative 2: Only count launches that attempted landing
attempted_landings = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list) and len(cores) > 0:
        core = cores[0]
        if core.get('landing_attempt', False):
            attempted_landings.append(core.get('landpad'))

missing_2 = pd.Series(attempted_landings).isnull().sum()
print(f"Alt 2 - Missing landpad (only attempted landings): {missing_2}")
print(f"Alt 2 - Total attempted landings: {len(attempted_landings)}")

# Alternative 3: Count all cores, not just first core
all_landpads = []
for i in range(len(df)):
    cores = df['cores'].iloc[i]
    if isinstance(cores, list):
        for core in cores:
            if isinstance(core, dict):
                all_landpads.append(core.get('landpad'))

missing_3 = pd.Series(all_landpads).isnull().sum()
print(f"Alt 3 - Missing landpad (all cores): {missing_3}")
print(f"Alt 3 - Total cores: {len(all_landpads)}")

# Alternative 4: Only Falcon 9 landpads
falcon9_landpads = []
falcon9_df = df[df['rocket'] == falcon9_id]
for i in range(len(falcon9_df)):
    cores = falcon9_df['cores'].iloc[i]
    if isinstance(cores, list) and len(cores) > 0:
        landpad = cores[0].get('landpad')
        falcon9_landpads.append(landpad)

missing_4 = pd.Series(falcon9_landpads).isnull().sum()
print(f"Alt 4 - Missing landpad (Falcon 9 only): {missing_4}")
print(f"Alt 4 - Total Falcon 9 launches: {len(falcon9_landpads)}")

# Alternative 5: Check if they mean something else by "landingPad"
print(f"\nChecking other possible interpretations...")
print(f"Columns containing 'land': {[col for col in df.columns if 'land' in col.lower()]}")

# Maybe they want launchpad instead?
if 'launchpad' in df.columns:
    missing_launchpad = df['launchpad'].isnull().sum()
    print(f"Alt 5 - Missing launchpad: {missing_launchpad}")

# Summary of most likely alternatives
print("\n" + "="*60)
print("🎯 MOST LIKELY ALTERNATIVES")
print("="*60)
print("Question 2 possibilities:")
print(f"  - 195 (all Falcon 9)")
print(f"  - {len(falcon9_success)} (successful Falcon 9)")
print(f"  - 200 (all non-Falcon 1)")

print("\nQuestion 3 possibilities:")
print(f"  - 54 (missing landpad, all launches)")
print(f"  - {missing_2} (missing landpad, attempted landings only)")
print(f"  - {missing_4} (missing landpad, Falcon 9 only)")

# Let's try the most common alternative answers
common_q2_answers = [195, len(falcon9_success), 200, len(non_falcon1)]
common_q3_answers = [54, missing_2, missing_4, 28, 35]

print(f"\nCommon Q2 answers to try: {common_q2_answers}")
print(f"Common Q3 answers to try: {common_q3_answers}")
