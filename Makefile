# LatinX in AI Mentorship Program - Makefile
# Shortcuts for common operations

.PHONY: help install test-syntax demo-folders clean migrate-demo

# Default target
help:
	@echo "LatinX in AI Mentorship Program - Available Commands:"
	@echo ""
	@echo "  make install       - Install Python dependencies"
	@echo "  make test-syntax   - Test script syntax"
	@echo "  make demo-folders  - Generate demo folder structure"
	@echo "  make clean         - Clean up demo files"
	@echo "  make migrate-demo  - Demo migration from pairings folder"
	@echo ""
	@echo "GitHub Project Management:"
	@echo "  make create-project OWNER=owner REPO=repo - Create new project"
	@echo "  make list-projects OWNER=owner REPO=repo  - List existing projects"
	@echo ""
	@echo "Required environment variables:"
	@echo "  GITHUB_TOKEN - Your GitHub personal access token"
	@echo "  OWNER        - GitHub repository owner (e.g., latinxinai)"
	@echo "  REPO         - GitHub repository name (e.g., mentorship-2025)"

# Install dependencies
install:
	pip install requests

# Test script syntax
test-syntax:
	python -m py_compile scripts/*.py
	@echo "✅ All scripts compile successfully"

# Generate demo folder structure
demo-folders:
	python -c "from scripts.manage_mentorship_projects import MentorshipProjectManager; import json; manager = MentorshipProjectManager('demo', 'demo', 'token'); manager.generate_pair_folders(json.load(open('templates/pair_template.json')), 'demo_pairs')"
	@echo "✅ Demo folders generated in demo_pairs/"

# Clean demo files
clean:
	rm -rf demo_pairs/ test_pairs/ migration_report.md migrated_pairs.json
	@echo "✅ Demo files cleaned up"

# Demo migration (creates fake pairings folder first)
migrate-demo:
	@echo "Creating demo pairings folder..."
	mkdir -p demo_pairings
	echo "# Jane Doe - John Smith\n\nGoals:\n- Learn machine learning\n- Complete project\n\nProgress: Getting started" > demo_pairings/jane-doe_john-smith.md
	echo "# Maria Garcia - Alex Chen\n\nGoals:\n- Data science skills\n- Career development\n\nProgress: Mid-program" > demo_pairings/maria-garcia_alex-chen.md
	python scripts/migrate_pairings_to_projects.py --pairings-path demo_pairings --scan-only
	@echo "✅ Migration demo complete - check migration_report.md"

# GitHub Projects commands (require GITHUB_TOKEN, OWNER, REPO)
create-project:
ifndef GITHUB_TOKEN
	$(error GITHUB_TOKEN environment variable is required)
endif
ifndef OWNER
	$(error OWNER parameter is required. Usage: make create-project OWNER=latinxinai REPO=mentorship-2025)
endif
ifndef REPO
	$(error REPO parameter is required. Usage: make create-project OWNER=latinxinai REPO=mentorship-2025)
endif
	python scripts/manage_mentorship_projects.py --owner $(OWNER) --repo $(REPO) --action create-project

list-projects:
ifndef GITHUB_TOKEN
	$(error GITHUB_TOKEN environment variable is required)
endif
ifndef OWNER
	$(error OWNER parameter is required. Usage: make list-projects OWNER=latinxinai REPO=mentorship-2025)
endif
ifndef REPO
	$(error REPO parameter is required. Usage: make list-projects OWNER=latinxinai REPO=mentorship-2025)
endif
	python scripts/manage_mentorship_projects.py --owner $(OWNER) --repo $(REPO) --action list-projects

# Generate folders from template
generate-folders:
	python scripts/manage_mentorship_projects.py --owner demo --repo demo --action generate-folders --pair-data templates/pair_template.json