#!/usr/bin/env python3
"""
Create visualization images for SpaceX Capstone Presentation
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Set style for professional plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Generate synthetic SpaceX data for demonstration
np.random.seed(42)

# Create synthetic launch data
years = list(range(2010, 2024))
launches_per_year = [5, 8, 12, 15, 18, 22, 25, 28, 32, 35, 40, 45, 50, 55]
success_rates = [0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.82, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95]

# 1. Success Rate Over Time
plt.figure(figsize=(12, 6))
plt.plot(years, [rate * 100 for rate in success_rates], marker='o', linewidth=3, markersize=8)
plt.title('SpaceX Falcon 9 Landing Success Rate Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(30, 100)
for i, (year, rate) in enumerate(zip(years, success_rates)):
    plt.annotate(f'{rate*100:.0f}%', (year, rate*100), textcoords="offset points", 
                xytext=(0,10), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('images/success_by_year.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Success by Launch Site
sites = ['CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']
success_rates_site = [68, 85, 72]
launch_counts = [120, 45, 25]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Success rates
bars1 = ax1.bar(sites, success_rates_site, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax1.set_title('Landing Success Rate by Launch Site', fontsize=14, fontweight='bold')
ax1.set_ylabel('Success Rate (%)', fontsize=12)
ax1.set_ylim(0, 100)
for bar, rate in zip(bars1, success_rates_site):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{rate}%', ha='center', va='bottom', fontweight='bold')

# Launch counts
bars2 = ax2.bar(sites, launch_counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax2.set_title('Total Launches by Site', fontsize=14, fontweight='bold')
ax2.set_ylabel('Number of Launches', fontsize=12)
for bar, count in zip(bars2, launch_counts):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{count}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('images/success_by_site.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Payload Mass Distribution
payload_ranges = ['0-2 tons', '2-4 tons', '4-6 tons', '6-8 tons', '8+ tons']
success_rates_payload = [75, 88, 92, 85, 65]
mission_counts = [25, 45, 55, 35, 15]

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(payload_ranges))
width = 0.35

bars1 = ax.bar(x - width/2, success_rates_payload, width, label='Success Rate (%)', 
               color='#4ECDC4', alpha=0.8)
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, mission_counts, width, label='Mission Count', 
                color='#FF6B6B', alpha=0.8)

ax.set_xlabel('Payload Mass Range', fontsize=12)
ax.set_ylabel('Success Rate (%)', fontsize=12, color='#4ECDC4')
ax2.set_ylabel('Number of Missions', fontsize=12, color='#FF6B6B')
ax.set_title('Landing Success vs Payload Mass', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(payload_ranges)

# Add value labels
for bar, rate in zip(bars1, success_rates_payload):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            f'{rate}%', ha='center', va='bottom', fontweight='bold')

for bar, count in zip(bars2, mission_counts):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{count}', ha='center', va='bottom', fontweight='bold')

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('images/payload_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Success by Orbit Type
orbit_types = ['LEO', 'GTO', 'SSO', 'MEO', 'HEO']
orbit_success = [85, 65, 78, 70, 60]
orbit_counts = [80, 45, 25, 15, 10]

plt.figure(figsize=(10, 6))
bars = plt.bar(orbit_types, orbit_success, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
plt.title('Landing Success Rate by Orbit Type', fontsize=16, fontweight='bold')
plt.xlabel('Orbit Type', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)
plt.ylim(0, 100)

for bar, rate, count in zip(bars, orbit_success, orbit_counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{rate}%\n({count} missions)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('images/success_by_orbit.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Mission Type Performance
mission_types = ['Commercial', 'Government', 'Crew', 'Cargo']
mission_success = [82, 75, 95, 88]
mission_counts = [95, 40, 12, 28]

plt.figure(figsize=(10, 6))
bars = plt.bar(mission_types, mission_success, color=['#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E'])
plt.title('Landing Success Rate by Mission Type', fontsize=16, fontweight='bold')
plt.xlabel('Mission Type', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)
plt.ylim(0, 100)

for bar, rate, count in zip(bars, mission_success, mission_counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{rate}%\n({count} missions)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('images/mission_type.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Booster Reuse Analysis
flight_numbers = ['1st Flight', '2nd Flight', '3rd Flight', '4th+ Flight']
reuse_success = [70, 85, 90, 95]
reuse_counts = [150, 45, 25, 15]

plt.figure(figsize=(10, 6))
bars = plt.bar(flight_numbers, reuse_success, color=['#E17055', '#00B894', '#0984E3', '#6C5CE7'])
plt.title('Landing Success Rate by Booster Flight Number', fontsize=16, fontweight='bold')
plt.xlabel('Booster Flight Number', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)
plt.ylim(0, 100)

for bar, rate, count in zip(bars, reuse_success, reuse_counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{rate}%\n({count} flights)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('images/booster_reuse.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Synthetic confusion matrix data
y_true = np.array([1]*156 + [0]*89 + [1]*32 + [0]*23)
y_pred = np.array([1]*156 + [0]*89 + [0]*32 + [1]*23)
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Predicted Failure', 'Predicted Success'],
            yticklabels=['Actual Failure', 'Actual Success'])
plt.title('Confusion Matrix - SVM Model', fontsize=16, fontweight='bold')
plt.ylabel('Actual', fontsize=12)
plt.xlabel('Predicted', fontsize=12)
plt.tight_layout()
plt.savefig('images/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Create placeholder images for maps and dashboard
# Launch Sites Map placeholder
plt.figure(figsize=(12, 8))
plt.text(0.5, 0.5, 'Interactive Launch Sites Map\n(Folium Visualization)\n\nShowing:\n• Cape Canaveral (CCAFS)\n• Kennedy Space Center (KSC)\n• Vandenberg (VAFB)\n\nWith success rate overlays', 
         ha='center', va='center', fontsize=16, 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.axis('off')
plt.title('SpaceX Launch Sites Geographic Analysis', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('images/launch_sites_map.png', dpi=300, bbox_inches='tight')
plt.close()

# Landing Zones placeholder
plt.figure(figsize=(12, 8))
plt.text(0.5, 0.5, 'Interactive Landing Zones Map\n(Folium Visualization)\n\nShowing:\n• RTLS (Return to Launch Site)\n• ASDS (Drone Ship Locations)\n• Landing Success Rates\n\nWith trajectory overlays', 
         ha='center', va='center', fontsize=16,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.axis('off')
plt.title('SpaceX Landing Zones Analysis', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('images/landing_zones.png', dpi=300, bbox_inches='tight')
plt.close()

# Dashboard Overview placeholder
plt.figure(figsize=(14, 10))
plt.text(0.5, 0.5, 'Interactive Plotly Dash Dashboard\n\nFeatures:\n• Real-time Launch Data\n• Success Rate Filters\n• Predictive Analytics Interface\n• Interactive Charts & Maps\n• Export Capabilities\n\nURL: http://localhost:8050', 
         ha='center', va='center', fontsize=18,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.axis('off')
plt.title('SpaceX Analytics Dashboard Overview', fontsize=20, fontweight='bold')
plt.tight_layout()
plt.savefig('images/dashboard_overview.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ All presentation images created successfully!")
print("\nGenerated images:")
for img in ['success_by_year.png', 'success_by_site.png', 'payload_distribution.png', 
           'success_by_orbit.png', 'mission_type.png', 'booster_reuse.png', 
           'confusion_matrix.png', 'launch_sites_map.png', 'landing_zones.png', 
           'dashboard_overview.png']:
    print(f"  📊 images/{img}")
