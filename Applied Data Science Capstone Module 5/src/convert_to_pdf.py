#!/usr/bin/env python3
"""
Convert SpaceX Capstone Presentation from Markdown to PDF
"""

import os
import subprocess
import sys
from pathlib import Path

def check_pandoc():
    """Check if pandoc is installed"""
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pandoc_instructions():
    """Print instructions for installing pandoc"""
    print("📋 Pandoc is required to convert Markdown to PDF")
    print("\n🔧 Installation Instructions:")
    print("\n🪟 Windows:")
    print("   Download from: https://pandoc.org/installing.html")
    print("   Or use chocolatey: choco install pandoc")
    print("\n🐧 Linux (Ubuntu/Debian):")
    print("   sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended")
    print("\n🍎 macOS:")
    print("   brew install pandoc")
    print("   brew install --cask mactex")

def convert_markdown_to_pdf():
    """Convert the presentation markdown to PDF"""
    
    # Paths
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    presentation_dir = project_root / "presentation"
    input_file = presentation_dir / "SpaceX_Capstone_Presentation.md"
    output_file = presentation_dir / "SpaceX_Capstone_Final.pdf"
    
    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        return False
    
    # Check pandoc installation
    if not check_pandoc():
        print("❌ Pandoc is not installed!")
        install_pandoc_instructions()
        return False
    
    print("🔄 Converting Markdown to PDF...")
    print(f"📄 Input: {input_file}")
    print(f"📄 Output: {output_file}")
    
    # Pandoc command with options for better PDF formatting
    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        '--pdf-engine=xelatex',  # Better Unicode support
        '--variable', 'geometry:margin=1in',
        '--variable', 'fontsize=11pt',
        '--variable', 'documentclass=article',
        '--variable', 'colorlinks=true',
        '--variable', 'linkcolor=blue',
        '--variable', 'urlcolor=blue',
        '--toc',  # Table of contents
        '--toc-depth=2',
        '--number-sections',
        '--highlight-style=github'
    ]
    
    try:
        # Run pandoc conversion
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ PDF conversion successful!")
        print(f"📁 Output saved to: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e}")
        print(f"📝 Error output: {e.stderr}")
        
        # Try alternative with pdflatex
        print("\n🔄 Trying alternative PDF engine...")
        cmd_alt = cmd.copy()
        cmd_alt[cmd_alt.index('--pdf-engine=xelatex')] = '--pdf-engine=pdflatex'
        
        try:
            subprocess.run(cmd_alt, capture_output=True, text=True, check=True)
            print("✅ PDF conversion successful with alternative engine!")
            print(f"📁 Output saved to: {output_file}")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"❌ Alternative conversion also failed: {e2}")
            print("\n💡 Alternative Solutions:")
            print("1. Use online Markdown to PDF converter")
            print("2. Copy content to Google Docs and export as PDF")
            print("3. Use VS Code with Markdown PDF extension")
            return False

def create_html_version():
    """Create HTML version as backup"""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    presentation_dir = project_root / "presentation"
    input_file = presentation_dir / "SpaceX_Capstone_Presentation.md"
    output_file = presentation_dir / "SpaceX_Capstone_Presentation.html"
    
    if not check_pandoc():
        return False
    
    print("🔄 Creating HTML backup...")
    
    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        '--standalone',
        '--css', 'https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-light.css',
        '--toc',
        '--toc-depth=2',
        '--number-sections',
        '--highlight-style=github'
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ HTML version created: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ HTML conversion failed: {e}")
        return False

def main():
    """Main conversion function"""
    print("🚀 SpaceX Capstone Presentation Converter")
    print("=" * 50)
    
    # Try PDF conversion
    pdf_success = convert_markdown_to_pdf()
    
    # Create HTML backup
    html_success = create_html_version()
    
    print("\n📊 Conversion Summary:")
    print(f"📄 PDF: {'✅ Success' if pdf_success else '❌ Failed'}")
    print(f"🌐 HTML: {'✅ Success' if html_success else '❌ Failed'}")
    
    if not pdf_success:
        print("\n💡 Manual Conversion Options:")
        print("1. 🌐 Online converters:")
        print("   - https://pandoc.org/try/")
        print("   - https://www.markdowntopdf.com/")
        print("2. 📝 Copy to Google Docs and export as PDF")
        print("3. 🔧 Use VS Code with 'Markdown PDF' extension")
        print("4. 📄 Print HTML version to PDF from browser")
    
    return pdf_success or html_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
