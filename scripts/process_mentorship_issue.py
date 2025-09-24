#!/usr/bin/env python3
"""
Process Mentorship Issues

This script processes GitHub issues that contain new mentorship pair information
and automatically creates project cards and folder structures.
"""

import os
import re
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import argparse
from manage_mentorship_projects import MentorshipProjectManager


class MentorshipIssueProcessor:
    """Processes GitHub issues for mentorship pair creation"""
    
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
        self.manager = MentorshipProjectManager(owner, repo, token)
    
    def get_issue(self, issue_number: int) -> Dict:
        """Fetch issue details from GitHub API"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch issue #{issue_number}: {response.status_code}")
            return {}
    
    def parse_mentorship_issue(self, issue_body: str) -> Optional[Dict]:
        """Parse mentorship pair information from issue body"""
        if not issue_body:
            return None
        
        pair_data = {
            "mentor": "",
            "mentee": "",
            "goals": [],
            "progress": "New pair from issue",
            "meetings": [],
            "deliverables": [],
            "last_updated": datetime.now().isoformat()
        }
        
        # Parse mentor information
        mentor_match = re.search(r'(?:\*\*mentor\*\*|mentor:)\s*(.+)', issue_body, re.IGNORECASE)
        if mentor_match:
            pair_data["mentor"] = mentor_match.group(1).strip()
        
        # Parse mentee information  
        mentee_match = re.search(r'(?:\*\*mentee\*\*|mentee:)\s*(.+)', issue_body, re.IGNORECASE)
        if mentee_match:
            pair_data["mentee"] = mentee_match.group(1).strip()
        
        # Parse goals
        goals_pattern = r'(?:\*\*goals?\*\*|goals?:)\s*\n((?:[-*]\s*.+\n?)+)'
        goals_match = re.search(goals_pattern, issue_body, re.IGNORECASE)
        if goals_match:
            goals_text = goals_match.group(1)
            goals = [line.strip('- *').strip() for line in goals_text.split('\n') if line.strip()]
            pair_data["goals"] = [goal for goal in goals if goal]
        
        # Parse program track/focus area
        track_match = re.search(r'(?:\*\*(?:track|focus|area)\*\*|(?:track|focus|area):)\s*(.+)', issue_body, re.IGNORECASE)
        if track_match:
            pair_data["program_track"] = track_match.group(1).strip()
        
        # Parse expected deliverables
        deliverables_pattern = r'(?:\*\*deliverables?\*\*|deliverables?:)\s*\n((?:[-*]\s*.+\n?)+)'
        deliverables_match = re.search(deliverables_pattern, issue_body, re.IGNORECASE)
        if deliverables_match:
            deliverables_text = deliverables_match.group(1)
            deliverables = [line.strip('- *').strip() for line in deliverables_text.split('\n') if line.strip()]
            pair_data["deliverables"] = [deliverable for deliverable in deliverables if deliverable]
        
        # Parse timeline/dates
        start_date_match = re.search(r'(?:\*\*start\s*date\*\*|start\s*date:)\s*(.+)', issue_body, re.IGNORECASE)
        if start_date_match:
            pair_data["start_date"] = start_date_match.group(1).strip()
        
        end_date_match = re.search(r'(?:\*\*end\s*date\*\*|end\s*date:)\s*(.+)', issue_body, re.IGNORECASE)
        if end_date_match:
            pair_data["end_date"] = end_date_match.group(1).strip()
        
        # Validate we have minimum required information
        if not pair_data["mentor"] or not pair_data["mentee"]:
            print("⚠️  Missing mentor or mentee information in issue")
            return None
        
        return pair_data
    
    def find_mentorship_project(self) -> Optional[int]:
        """Find existing mentorship project or return None"""
        projects = self.manager.list_projects()
        
        for project in projects:
            if 'mentorship' in project['name'].lower():
                return project['id']
        
        return None
    
    def process_issue(self, issue_number: int) -> bool:
        """Process a mentorship issue and create project card"""
        # Fetch issue
        issue = self.get_issue(issue_number)
        if not issue:
            return False
        
        # Check if it's a mentorship-related issue
        title = issue.get('title', '').lower()
        if 'mentorship' not in title and 'mentor' not in title:
            print(f"ℹ️  Issue #{issue_number} doesn't appear to be mentorship-related")
            return False
        
        # Parse issue body
        pair_data = self.parse_mentorship_issue(issue.get('body', ''))
        if not pair_data:
            print(f"❌ Could not parse mentorship information from issue #{issue_number}")
            return False
        
        print(f"✅ Parsed mentorship pair: {pair_data['mentor']} ↔ {pair_data['mentee']}")
        
        # Find or create project
        project_id = self.find_mentorship_project()
        if not project_id:
            print("📋 Creating new mentorship project...")
            result = self.manager.create_mentorship_project("Mentorship 2025")
            if result:
                project_id = result.get('id')
            else:
                print("❌ Failed to create project")
                return False
        
        # Create project card
        card_result = self.manager.create_mentorship_card(project_id, pair_data)
        if not card_result:
            print("❌ Failed to create project card")
            return False
        
        # Generate folder structure
        try:
            folder_path = self.manager.generate_pair_folders(pair_data)
            print(f"📁 Generated folder structure: {folder_path}")
        except Exception as e:
            print(f"⚠️  Failed to generate folders: {e}")
        
        # Add comment to issue
        self.add_processing_comment(issue_number, pair_data, project_id, card_result.get('id'))
        
        # Close the issue if it was successfully processed
        self.close_issue(issue_number)
        
        return True
    
    def add_processing_comment(self, issue_number: int, pair_data: Dict, project_id: int, card_id: int):
        """Add a comment to the issue indicating successful processing"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        
        comment_body = f"""✅ **Mentorship Pair Successfully Processed**

**Mentor**: {pair_data.get('mentor', 'Unknown')}
**Mentee**: {pair_data.get('mentee', 'Unknown')}

📋 **Project Card Created**: [View in Project](https://github.com/{self.owner}/{self.repo}/projects)
🎯 **Goals**: {len(pair_data.get('goals', []))} goals identified
📁 **Folder Structure**: Generated automatically

## Next Steps
1. Check the project card for tracking progress
2. Review the generated folder structure in the repository
3. Schedule initial mentor-mentee meeting
4. Update project card with meeting notes and progress

---
*This pair was automatically processed from this issue.*
"""
        
        data = {"body": comment_body}
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"💬 Added processing comment to issue #{issue_number}")
        else:
            print(f"⚠️  Failed to add comment: {response.status_code}")
    
    def close_issue(self, issue_number: int):
        """Close the processed issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        
        data = {
            "state": "closed",
            "state_reason": "completed"
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"🔒 Closed issue #{issue_number}")
        else:
            print(f"⚠️  Failed to close issue: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(description='Process mentorship issues')
    parser.add_argument('--owner', required=True, help='GitHub repository owner')
    parser.add_argument('--repo', required=True, help='GitHub repository name')
    parser.add_argument('--token', help='GitHub token (or set GITHUB_TOKEN env var)')
    parser.add_argument('--issue-number', type=int, required=True, help='Issue number to process')
    
    args = parser.parse_args()
    
    # Get token from argument or environment
    token = args.token or os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GitHub token required. Use --token argument or set GITHUB_TOKEN environment variable")
        return
    
    processor = MentorshipIssueProcessor(args.owner, args.repo, token)
    
    success = processor.process_issue(args.issue_number)
    if success:
        print(f"✅ Successfully processed issue #{args.issue_number}")
    else:
        print(f"❌ Failed to process issue #{args.issue_number}")


if __name__ == '__main__':
    main()