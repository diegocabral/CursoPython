#!/usr/bin/env python3
"""
Quick Start Script for Google Maps Route Planner

This script helps users quickly set up and test the route planning system.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        ('googlemaps', 'googlemaps'),
        ('folium', 'folium'), 
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('flask', 'flask')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} (missing)")
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies(missing_packages):
    """Install missing dependencies"""
    if not missing_packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            '--upgrade', 'pip'
        ])
        
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            '-r', 'requirements.txt'
        ])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists and is configured"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        
        # Create .env from template
        env_example = Path('.env.example')
        if env_example.exists():
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created from template")
            print("⚠️  Please edit .env file and add your Google Maps API key")
            return False
        else:
            print("❌ .env.example template not found")
            return False
    
    # Check if API key is configured
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_google_maps_api_key_here' in content:
            print("⚠️  Please replace 'your_google_maps_api_key_here' with your actual API key in .env")
            return False
        elif 'GOOGLE_MAPS_API_KEY=' in content and len(content.split('GOOGLE_MAPS_API_KEY=')[1].split('\n')[0].strip()) > 10:
            print("✅ .env file configured")
            return True
        else:
            print("⚠️  GOOGLE_MAPS_API_KEY appears to be empty in .env file")
            return False

def create_directories():
    """Create necessary directories"""
    directories = ['static/maps', 'static/exports', 'templates']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Required directories created")

def test_system():
    """Test the route planning system"""
    print("\n🧪 Testing route planning system...")
    
    try:
        from route_planner import RouteOptimizer
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        
        if not api_key or api_key == 'your_google_maps_api_key_here':
            print("❌ API key not configured properly")
            return False
        
        # Quick test
        optimizer = RouteOptimizer(api_key)
        
        # Test with a simple address
        success = optimizer.add_address("New York, NY")
        
        if success:
            print("✅ Google Maps API connection successful")
            return True
        else:
            print("❌ Failed to connect to Google Maps API")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_next_steps(test_passed):
    """Show next steps to the user"""
    print("\n" + "="*50)
    print("🚀 QUICK START COMPLETE")
    print("="*50)
    
    if test_passed:
        print("\n✅ System is ready to use!")
        print("\n📝 What you can do now:")
        print("\n1. Run the command-line interface:")
        print("   python route_planner.py")
        
        print("\n2. Start the web application:")
        print("   python web_app.py")
        print("   Then open: http://localhost:5000")
        
        print("\n3. Run example scripts:")
        print("   python example_usage.py")
        
        print("\n4. Use programmatically:")
        print("   from route_planner import RouteOptimizer")
        
    else:
        print("\n⚠️  Setup incomplete. Please resolve the issues above.")
        print("\n📖 For help, check the README.md file or:")
        print("   - Verify your Google Maps API key is correct")
        print("   - Ensure required APIs are enabled in Google Cloud Console")
        print("   - Check your internet connection")

def main():
    """Main setup and test function"""
    print("🗺️  Google Maps Route Planner - Quick Start")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    print("\n🔍 Checking dependencies...")
    missing_packages = check_dependencies()
    
    # Install missing dependencies
    if missing_packages:
        install_success = install_dependencies(missing_packages)
        if not install_success:
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            return
    else:
        print("✅ All dependencies are installed")
    
    # Create directories
    print("\n📁 Setting up directories...")
    create_directories()
    
    # Check environment configuration
    print("\n🔑 Checking API configuration...")
    env_configured = check_env_file()
    
    # Test system if environment is configured
    test_passed = False
    if env_configured:
        test_passed = test_system()
    
    # Show next steps
    show_next_steps(test_passed)
    
    if not env_configured:
        print(f"\n🔧 To configure your API key:")
        print(f"   1. Edit the .env file")
        print(f"   2. Replace 'your_google_maps_api_key_here' with your actual API key")
        print(f"   3. Run this script again to test the connection")

if __name__ == "__main__":
    main()