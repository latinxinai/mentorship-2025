#!/usr/bin/env python3
"""
GitHub Projects Mentorship Management Script

This script helps manage mentor-mentee pairs using GitHub Projects instead of
the traditional pairings/ folder structure. It can create, update, and track
mentorship pairs with all required information.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class MentorshipProjectManager:
    """Manages mentorship pairs through GitHub Projects API"""
    
    def __init__(self, owner: str, repo: str, token: str):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.base_url = 'https://api.github.com'
        
    def create_mentorship_project(self, title: str = "Mentorship 2025") -> Dict:
        """Create a new GitHub Project for mentorship tracking"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/projects"
        
        data = {
            "name": title,
            "body": "Tracking mentor-mentee pairs for 2025 mentorship program",
            "state": "open"
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"✅ Created project: {title}")
            return response.json()
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            print(response.text)
            return {}
    
    def create_mentorship_card(self, project_id: int, pair_data: Dict) -> Dict:
        """Create a project card for a mentor-mentee pair"""
        url = f"{self.base_url}/projects/{project_id}/cards"
        
        # Format card content with all required fields
        card_content = self._format_card_content(pair_data)
        
        data = {
            "note": card_content
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"✅ Created card for {pair_data.get('mentor', 'Unknown')} - {pair_data.get('mentee', 'Unknown')}")
            return response.json()
        else:
            print(f"❌ Failed to create card: {response.status_code}")
            return {}
    
    def _format_card_content(self, pair_data: Dict) -> str:
        """Format the content for a mentorship pair card"""
        mentor = pair_data.get('mentor', 'TBD')
        mentee = pair_data.get('mentee', 'TBD')
        goals = pair_data.get('goals', [])
        progress = pair_data.get('progress', 'Not started')
        meetings = pair_data.get('meetings', [])
        deliverables = pair_data.get('deliverables', [])
        last_updated = pair_data.get('last_updated', datetime.now().isoformat())
        
        # Format goals
        goals_text = '\n'.join([f"- {goal}" for goal in goals]) if goals else "- TBD"
        
        # Format meetings
        meetings_text = '\n'.join([f"- {meeting}" for meeting in meetings]) if meetings else "- No meetings scheduled"
        
        # Format deliverables
        deliverables_text = '\n'.join([f"- {deliverable}" for deliverable in deliverables]) if deliverables else "- TBD"
        
        return f"""# {mentor} ↔ {mentee}

## 📋 Goals
{goals_text}

## 📊 Progress
{progress}

## 🤝 Meetings
{meetings_text}

## 📦 Deliverables
{deliverables_text}

## 🕒 Last Updated
{last_updated}

---
*This card tracks the mentorship pair progress. Update regularly to maintain current status.*
"""
    
    def update_card(self, card_id: int, pair_data: Dict) -> Dict:
        """Update an existing mentorship card"""
        url = f"{self.base_url}/projects/cards/{card_id}"
        
        card_content = self._format_card_content(pair_data)
        
        data = {
            "note": card_content
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"✅ Updated card for {pair_data.get('mentor', 'Unknown')} - {pair_data.get('mentee', 'Unknown')}")
            return response.json()
        else:
            print(f"❌ Failed to update card: {response.status_code}")
            return {}
    
    def list_projects(self) -> List[Dict]:
        """List all projects in the repository"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/projects"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to list projects: {response.status_code}")
            return []
    
    def generate_pair_folders(self, pair_data: Dict, base_path: str = "pairs") -> str:
        """Generate folder structure for a mentor-mentee pair"""
        mentor = pair_data.get('mentor', 'unknown_mentor').replace(' ', '_').lower()
        mentee = pair_data.get('mentee', 'unknown_mentee').replace(' ', '_').lower()
        
        pair_folder = f"{base_path}/{mentor}_{mentee}"
        
        # Create directory structure
        os.makedirs(f"{pair_folder}/meetings", exist_ok=True)
        os.makedirs(f"{pair_folder}/deliverables", exist_ok=True)
        os.makedirs(f"{pair_folder}/resources", exist_ok=True)
        
        # Create placeholder files
        self._create_pair_files(pair_folder, pair_data)
        
        print(f"✅ Generated folder structure: {pair_folder}")
        return pair_folder
    
    def _create_pair_files(self, pair_folder: str, pair_data: Dict):
        """Create placeholder files for the pair"""
        # README.md
        readme_content = f"""# {pair_data.get('mentor', 'TBD')} ↔ {pair_data.get('mentee', 'TBD')} Mentorship

## Overview
This folder contains all materials and documentation for the mentorship relationship between {pair_data.get('mentor', 'TBD')} (mentor) and {pair_data.get('mentee', 'TBD')} (mentee).

## Folder Structure
- `meetings/` - Meeting notes and recordings
- `deliverables/` - Project deliverables and milestones
- `resources/` - Shared resources and references

## Goals
{chr(10).join([f"- {goal}" for goal in pair_data.get('goals', ['TBD'])])}

## Contact Information
- **Mentor**: {pair_data.get('mentor', 'TBD')}
- **Mentee**: {pair_data.get('mentee', 'TBD')}

## Progress Tracking
Track progress in the GitHub Project card for this pair.
"""
        
        with open(f"{pair_folder}/README.md", 'w') as f:
            f.write(readme_content)
        
        # Meeting template
        meeting_template = """# Meeting Notes Template

**Date**: 
**Duration**: 
**Attendees**: 
- Mentor: 
- Mentee: 

## Agenda
- [ ] Item 1
- [ ] Item 2

## Discussion Points


## Action Items
- [ ] Action for mentor:
- [ ] Action for mentee:

## Next Meeting
**Date**: 
**Time**: 
**Agenda Preview**: 
"""
        
        with open(f"{pair_folder}/meetings/meeting_template.md", 'w') as f:
            f.write(meeting_template)
        
        # Goals tracker
        goals_content = f"""# Goals and Milestones

## Primary Goals
{chr(10).join([f"- [ ] {goal}" for goal in pair_data.get('goals', ['Define specific goals'])])}

## Milestones
- [ ] Initial meeting completed
- [ ] Goals defined and agreed upon
- [ ] Mid-program check-in
- [ ] Final deliverable completed
- [ ] Program completion

## Progress Notes
*Update this section regularly with progress notes*

"""
        
        with open(f"{pair_folder}/goals.md", 'w') as f:
            f.write(goals_content)


def main():
    parser = argparse.ArgumentParser(description='Manage mentorship pairs through GitHub Projects')
    parser.add_argument('--owner', required=True, help='GitHub repository owner')
    parser.add_argument('--repo', required=True, help='GitHub repository name')
    parser.add_argument('--token', help='GitHub token (or set GITHUB_TOKEN env var)')
    parser.add_argument('--action', choices=['create-project', 'create-card', 'list-projects', 'generate-folders'], 
                       required=True, help='Action to perform')
    parser.add_argument('--project-id', type=int, help='Project ID for card operations')
    parser.add_argument('--pair-data', help='JSON file containing pair data')
    parser.add_argument('--project-title', default='Mentorship 2025', help='Title for new project')
    
    args = parser.parse_args()
    
    # Get token from argument or environment
    token = args.token or os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GitHub token required. Use --token argument or set GITHUB_TOKEN environment variable")
        return
    
    manager = MentorshipProjectManager(args.owner, args.repo, token)
    
    if args.action == 'create-project':
        result = manager.create_mentorship_project(args.project_title)
        if result:
            print(f"Project ID: {result.get('id')}")
    
    elif args.action == 'list-projects':
        projects = manager.list_projects()
        print(f"Found {len(projects)} projects:")
        for project in projects:
            print(f"- {project['name']} (ID: {project['id']})")
    
    elif args.action == 'create-card':
        if not args.project_id or not args.pair_data:
            print("❌ --project-id and --pair-data required for create-card action")
            return
        
        with open(args.pair_data, 'r') as f:
            pair_data = json.load(f)
        
        manager.create_mentorship_card(args.project_id, pair_data)
    
    elif args.action == 'generate-folders':
        if not args.pair_data:
            print("❌ --pair-data required for generate-folders action")
            return
        
        with open(args.pair_data, 'r') as f:
            pair_data = json.load(f)
        
        manager.generate_pair_folders(pair_data)


if __name__ == '__main__':
    main()