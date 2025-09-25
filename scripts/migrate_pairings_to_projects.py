#!/usr/bin/env python3
"""
Migration Script: Pairings Folder to GitHub Projects

This script helps migrate from the old pairings/ folder structure to the new
GitHub Projects-based mentorship tracking system.
"""

import os
import json
import glob
import re
from datetime import datetime
from typing import Dict, List
import argparse
from manage_mentorship_projects import MentorshipProjectManager


class PairingsMigrator:
    """Migrates from pairings/ folder structure to GitHub Projects"""
    
    def __init__(self, pairings_path: str = "pairings"):
        self.pairings_path = pairings_path
        
    def scan_pairings_folder(self) -> List[Dict]:
        """Scan the pairings/ folder and extract mentorship data"""
        pairs = []
        
        if not os.path.exists(self.pairings_path):
            print(f"⚠️  Pairings folder not found: {self.pairings_path}")
            return pairs
        
        # Look for pair folders or files
        pair_patterns = [
            f"{self.pairings_path}/*_*",  # mentor_mentee format
            f"{self.pairings_path}/*/",   # subdirectories
            f"{self.pairings_path}/*.md", # markdown files
            f"{self.pairings_path}/*.txt" # text files
        ]
        
        found_items = []
        for pattern in pair_patterns:
            found_items.extend(glob.glob(pattern))
        
        for item in found_items:
            pair_data = self._extract_pair_data(item)
            if pair_data:
                pairs.append(pair_data)
                
        print(f"📁 Found {len(pairs)} mentor-mentee pairs")
        return pairs
    
    def _extract_pair_data(self, path: str) -> Dict:
        """Extract mentorship data from a file or folder"""
        pair_data = {
            "mentor": "Unknown",
            "mentee": "Unknown", 
            "goals": [],
            "progress": "Migrated from pairings folder",
            "meetings": [],
            "deliverables": [],
            "last_updated": datetime.now().isoformat(),
            "migration_source": path
        }
        
        # Extract names from path
        basename = os.path.basename(path.rstrip('/'))
        
        # Try to parse mentor_mentee format
        if '_' in basename:
            parts = basename.replace('.md', '').replace('.txt', '').split('_')
            if len(parts) >= 2:
                pair_data["mentor"] = parts[0].replace('-', ' ').title()
                pair_data["mentee"] = parts[1].replace('-', ' ').title()
        
        # If it's a file, try to extract more information
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract goals
                goals_match = re.search(r'(?:goals?|objectives?):?\s*\n((?:[-*]\s*.+\n?)+)', content, re.IGNORECASE)
                if goals_match:
                    goals_text = goals_match.group(1)
                    goals = [line.strip('- *').strip() for line in goals_text.split('\n') if line.strip()]
                    pair_data["goals"] = [goal for goal in goals if goal]
                
                # Extract progress information
                progress_match = re.search(r'(?:progress|status):?\s*(.+)', content, re.IGNORECASE)
                if progress_match:
                    pair_data["progress"] = progress_match.group(1).strip()
                
                # Extract meetings
                meetings_match = re.search(r'(?:meetings?|sessions?):?\s*\n((?:[-*]\s*.+\n?)+)', content, re.IGNORECASE)
                if meetings_match:
                    meetings_text = meetings_match.group(1)
                    meetings = [line.strip('- *').strip() for line in meetings_text.split('\n') if line.strip()]
                    pair_data["meetings"] = [meeting for meeting in meetings if meeting]
                    
            except Exception as e:
                print(f"⚠️  Could not read file {path}: {e}")
        
        # If it's a directory, scan for additional files
        elif os.path.isdir(path):
            try:
                files = os.listdir(path)
                if 'README.md' in files:
                    readme_path = os.path.join(path, 'README.md')
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Similar extraction logic as above
                        
                # Look for meeting notes
                meeting_files = [f for f in files if 'meeting' in f.lower() or 'session' in f.lower()]
                if meeting_files:
                    pair_data["meetings"] = [f"Meeting file: {f}" for f in meeting_files]
                    
            except Exception as e:
                print(f"⚠️  Could not scan directory {path}: {e}")
        
        return pair_data
    
    def create_migration_report(self, pairs: List[Dict], output_file: str = "migration_report.md"):
        """Create a migration report"""
        report_content = f"""# Pairings Migration Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: {self.pairings_path}
**Pairs Found**: {len(pairs)}

## Migration Summary

| Mentor | Mentee | Goals | Meetings | Status |
|--------|--------|-------|----------|--------|
"""
        
        for pair in pairs:
            mentor = pair.get('mentor', 'Unknown')
            mentee = pair.get('mentee', 'Unknown') 
            goals_count = len(pair.get('goals', []))
            meetings_count = len(pair.get('meetings', []))
            progress = pair.get('progress', 'Unknown')
            
            report_content += f"| {mentor} | {mentee} | {goals_count} | {meetings_count} | {progress} |\n"
        
        report_content += f"""
## Detailed Information

"""
        
        for i, pair in enumerate(pairs, 1):
            report_content += f"""### Pair {i}: {pair.get('mentor', 'Unknown')} ↔ {pair.get('mentee', 'Unknown')}

**Source**: `{pair.get('migration_source', 'Unknown')}`
**Goals**: {len(pair.get('goals', []))} found
**Meetings**: {len(pair.get('meetings', []))} found
**Progress**: {pair.get('progress', 'Unknown')}

#### Goals
{chr(10).join([f"- {goal}" for goal in pair.get('goals', ['No goals found'])])}

#### Meetings
{chr(10).join([f"- {meeting}" for meeting in pair.get('meetings', ['No meetings found'])])}

---

"""
        
        with open(output_file, 'w') as f:
            f.write(report_content)
        
        print(f"📄 Migration report created: {output_file}")
    
    def export_pairs_json(self, pairs: List[Dict], output_file: str = "migrated_pairs.json"):
        """Export pairs data as JSON for further processing"""
        with open(output_file, 'w') as f:
            json.dump(pairs, f, indent=2)
        
        print(f"💾 Pairs data exported: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Migrate pairings folder to GitHub Projects')
    parser.add_argument('--pairings-path', default='pairings', help='Path to pairings folder')
    parser.add_argument('--owner', help='GitHub repository owner')
    parser.add_argument('--repo', help='GitHub repository name')
    parser.add_argument('--token', help='GitHub token (or set GITHUB_TOKEN env var)')
    parser.add_argument('--project-id', type=int, help='Existing project ID to add cards to')
    parser.add_argument('--create-project', action='store_true', help='Create new project')
    parser.add_argument('--project-title', default='Mentorship 2025 - Migrated', help='Title for new project')
    parser.add_argument('--scan-only', action='store_true', help='Only scan and report, do not migrate')
    parser.add_argument('--generate-folders', action='store_true', help='Generate new folder structure')
    
    args = parser.parse_args()
    
    # Initialize migrator
    migrator = PairingsMigrator(args.pairings_path)
    
    # Scan pairings folder
    pairs = migrator.scan_pairings_folder()
    
    if not pairs:
        print("❌ No pairs found to migrate")
        return
    
    # Create migration report
    migrator.create_migration_report(pairs)
    migrator.export_pairs_json(pairs)
    
    if args.scan_only:
        print("✅ Scan complete. Use migration report to review findings.")
        return
    
    # If GitHub integration is requested
    if args.owner and args.repo:
        token = args.token or os.getenv('GITHUB_TOKEN')
        if not token:
            print("❌ GitHub token required for project operations")
            return
        
        manager = MentorshipProjectManager(args.owner, args.repo, token)
        
        # Create project if requested
        project_id = args.project_id
        if args.create_project:
            result = manager.create_mentorship_project(args.project_title)
            if result:
                project_id = result.get('id')
                print(f"📋 Created project with ID: {project_id}")
        
        # Create cards for each pair
        if project_id:
            for pair in pairs:
                manager.create_mentorship_card(project_id, pair)
        
        # Generate folder structure if requested
        if args.generate_folders:
            for pair in pairs:
                manager.generate_pair_folders(pair)
    
    print("✅ Migration complete!")


if __name__ == '__main__':
    main()