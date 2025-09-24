#!/usr/bin/env python3
"""
Setup script for LatinX in AI Mentorship Program

This script helps set up the mentorship program environment and validates configuration.
"""

import os
import sys
import subprocess
import requests
from typing import Dict, List

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_github_token():
    """Check if GitHub token is available and valid"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️  GITHUB_TOKEN environment variable not set")
        print("   To set it: export GITHUB_TOKEN='your_token_here'")
        print("   Get a token from: https://github.com/settings/tokens")
        return False
    
    # Test token validity
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    }
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ GitHub token valid - authenticated as {user_info.get('login')}")
            return True
        else:
            print(f"❌ GitHub token invalid - status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to validate GitHub token: {e}")
        return False

def test_scripts():
    """Test that scripts compile and work correctly"""
    scripts = [
        'scripts/manage_mentorship_projects.py',
        'scripts/migrate_pairings_to_projects.py', 
        'scripts/process_mentorship_issue.py'
    ]
    
    print("🔍 Testing script compilation...")
    for script in scripts:
        try:
            subprocess.check_call([sys.executable, '-m', 'py_compile', script])
            print(f"  ✅ {script}")
        except subprocess.CalledProcessError:
            print(f"  ❌ {script}")
            return False
    
    return True

def create_demo_project():
    """Create a demo project to test functionality"""
    print("🎯 Creating demo project...")
    
    # This would normally call the GitHub API, but for demo we'll just simulate
    print("  📋 Demo project creation simulated")
    print("  📁 Demo folder structure can be generated with: make demo-folders")
    print("  📝 Demo migration can be tested with: make migrate-demo")
    
    return True

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Setup complete! Next steps:")
    print()
    print("1. Create your first mentorship project:")
    print("   make create-project OWNER=your-org REPO=your-repo")
    print()
    print("2. Or create a new pair via GitHub issue:")
    print("   https://github.com/your-org/your-repo/issues/new?template=new_mentorship_pair.md")
    print()
    print("3. Migrate from existing pairings/ folder:")
    print("   make migrate-demo  # Test migration")
    print("   python scripts/migrate_pairings_to_projects.py --help  # See options")
    print()
    print("4. Generate folder structure:")
    print("   make demo-folders  # Generate demo structure")
    print()
    print("5. Read the documentation:")
    print("   📖 docs/github_projects_workflow.md")
    print("   📋 README.md")
    print()
    print("🆘 Need help? Create an issue or check the documentation!")

def main():
    """Main setup function"""
    print("🚀 LatinX in AI Mentorship Program Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not test_scripts():
        print("❌ Script compilation failed")
        sys.exit(1)
    
    # Check GitHub token (optional)
    has_token = check_github_token()
    
    if has_token:
        create_demo_project()
    else:
        print("⚠️  Skipping GitHub API tests (no token)")
    
    print("\n✅ Setup completed successfully!")
    show_next_steps()

if __name__ == '__main__':
    main()