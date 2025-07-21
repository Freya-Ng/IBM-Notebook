#!/usr/bin/env python3
"""
Setup Script for Applied Data Science Capstone Module 5
SpaceX Falcon 9 Launch Success Prediction Project
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header():
    """Print project header"""
    print("🚀" + "=" * 60 + "🚀")
    print("    Applied Data Science Capstone - Module 5")
    print("    SpaceX Falcon 9 Launch Success Prediction")
    print("🚀" + "=" * 60 + "🚀")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  Warning: Python 3.8+ recommended")
        return False
    else:
        print("✅ Python version OK")
        return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing Required Packages...")
    
    # Core packages for the project
    packages = [
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'plotly>=5.0.0',
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.0',
        'scikit-learn>=1.0.0',
        'jupyter>=1.0.0'
    ]
    
    for package in packages:
        try:
            print(f"📥 Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_directory_structure():
    """Create project directory structure"""
    print("\n📁 Creating Directory Structure...")
    
    directories = [
        "notebooks",
        "src", 
        "data",
        "images",
        "presentation"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"📂 Created: {directory}/")
    
    print("✅ Directory structure created")

def generate_images():
    """Generate presentation images"""
    print("\n🎨 Generating Presentation Images...")
    
    try:
        script_path = Path("src/create_presentation_images.py")
        if script_path.exists():
            subprocess.run([sys.executable, str(script_path)], check=True)
            print("✅ Images generated successfully")
        else:
            print("⚠️  Image generation script not found")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate images: {e}")
        return False
    
    return True

def run_spacex_analysis():
    """Run SpaceX data analysis"""
    print("\n🔍 Running SpaceX Data Analysis...")
    
    scripts = [
        "src/spacex_simple.py",
        "src/spacex_analysis.py"
    ]
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            try:
                print(f"🏃 Running {script}...")
                subprocess.run([sys.executable, str(script_path)], check=True)
                print(f"✅ {script} completed")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  {script} failed: {e}")
        else:
            print(f"⚠️  {script} not found")

def convert_presentation():
    """Convert presentation to PDF"""
    print("\n📄 Converting Presentation to PDF...")
    
    try:
        script_path = Path("src/convert_to_pdf.py")
        if script_path.exists():
            subprocess.run([sys.executable, str(script_path)], check=True)
            print("✅ Presentation converted")
        else:
            print("⚠️  PDF conversion script not found")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  PDF conversion failed: {e}")
        print("💡 You can manually convert the presentation later")

def create_sample_notebooks():
    """Create sample notebook templates"""
    print("\n📓 Creating Sample Notebooks...")
    
    notebooks = [
        ("01_data_collection.ipynb", "SpaceX API Data Collection"),
        ("02_data_wrangling.ipynb", "Data Cleaning and Preprocessing"),
        ("03_eda_sql.ipynb", "SQL Analysis and Queries"),
        ("04_eda_visualization.ipynb", "Exploratory Data Analysis"),
        ("05_interactive_analytics.ipynb", "Folium Maps and Plotly Charts"),
        ("06_dashboard.ipynb", "Dash Interactive Dashboard"),
        ("07_machine_learning.ipynb", "Predictive Modeling")
    ]
    
    for filename, title in notebooks:
        notebook_path = Path("notebooks") / filename
        if not notebook_path.exists():
            # Create basic notebook structure
            notebook_content = f'''{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# {title}\\n",
    "\\n",
    "## Objective\\n",
    "This notebook covers {title.lower()} for the SpaceX Falcon 9 launch success prediction project.\\n",
    "\\n",
    "## Contents\\n",
    "1. Setup and imports\\n",
    "2. Data loading\\n",
    "3. Analysis\\n",
    "4. Results\\n",
    "5. Conclusions"
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "outputs": [],
   "source": [
    "# Import required libraries\\n",
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# Set display options\\n",
    "pd.set_option('display.max_columns', None)\\n",
    "plt.style.use('seaborn-v0_8')"
   ]
  }}
 ],
 "metadata": {{
  "kernelspec": {{
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }},
  "language_info": {{
   "name": "python",
   "version": "3.8.0"
  }}
 }},
 "nbformat": 4,
 "nbformat_minor": 4
}}'''
            
            with open(notebook_path, 'w') as f:
                f.write(notebook_content)
            
            print(f"📓 Created: {filename}")
    
    print("✅ Sample notebooks created")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Next Steps:")
    print("=" * 50)
    print("1. 📝 Complete all 7 Jupyter notebooks in notebooks/")
    print("2. 🔍 Review and customize the presentation in presentation/")
    print("3. 📄 Convert presentation to PDF using src/convert_to_pdf.py")
    print("4. 🌐 Upload project to GitHub repository")
    print("5. 📋 Complete Coursera submission using Coursera_Submission_Template.md")
    print("6. 👥 Submit for peer review")
    
    print("\n📚 Key Files:")
    print("- 📊 presentation/SpaceX_Capstone_Presentation.md")
    print("- 📄 presentation/SpaceX_Capstone_Final.pdf (after conversion)")
    print("- 🌐 GitHub_README.md (for repository)")
    print("- 📋 Coursera_Submission_Template.md (for submission)")
    print("- 🎨 images/ (all visualization images)")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        print("⚠️  Consider upgrading Python for best compatibility")
    
    # Install requirements
    if not install_requirements():
        print("❌ Package installation failed. Please install manually.")
        return False
    
    # Create directories
    create_directory_structure()
    
    # Generate images
    generate_images()
    
    # Run analysis
    run_spacex_analysis()
    
    # Create sample notebooks
    create_sample_notebooks()
    
    # Convert presentation
    convert_presentation()
    
    # Print next steps
    print_next_steps()
    
    print("\n🎉 Project setup completed successfully!")
    print("🚀 Ready for Applied Data Science Capstone Module 5!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
