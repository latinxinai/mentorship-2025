# LatinX in AI Mentorship Program 2025

Welcome to the LatinX in AI Mentorship Program! This repository manages mentor-mentee pairs using **GitHub Projects** for modern, efficient tracking and collaboration.

## 🚀 Getting Started

### Option 1: Create via GitHub Issue (Recommended)
1. Click [New Mentorship Pair](../../issues/new?template=new_mentorship_pair.md)
2. Fill out the template completely
3. Submit - automation handles the rest!

### Option 2: Manual Script Usage
```bash
# Create a new project
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action create-project

# Add a new pair
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action create-card \
  --project-id 123 \
  --pair-data templates/pair_template.json
```

### Option 3: Migrate from Existing Pairings
```bash
# Migrate old pairings/ folder
python scripts/migrate_pairings_to_projects.py \
  --pairings-path pairings \
  --owner latinxinai \
  --repo mentorship-2025 \
  --create-project \
  --generate-folders
```

## 📊 Project Management

### GitHub Projects Features:
- **Kanban board** view for visual progress tracking
- **Custom fields** for mentor/mentee info, dates, status
- **Filtering and sorting** by program track, status, dates
- **Milestone tracking** with deadlines
- **Progress reports** and analytics

### Folder Structure (Auto-generated):
```
pairs/jane_doe_john_smith/
├── README.md                    # Pair overview and contact info
├── goals.md                     # Goals and milestones tracker  
├── meetings/                    # Meeting notes and recordings
│   ├── meeting_template.md
│   └── 2025-01-15_kickoff.md
├── deliverables/               # Project outcomes
│   ├── development_plan.md
│   └── capstone_project/
└── resources/                  # Shared materials
    └── reading_list.md
```

## 🔧 Setup & Configuration

### Prerequisites:
- Python 3.7+
- GitHub repository access
- GitHub token with Projects permissions

### Environment Variables:
```bash
export GITHUB_TOKEN="your_github_token"
```

### Dependencies:
```bash
pip install requests
```

## 🎯 Usage Examples

### Create New Project:
```bash
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action create-project \
  --project-title "Mentorship 2025"
```

### List Existing Projects:
```bash
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action list-projects
```

### Generate Folder Structure:
```bash
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action generate-folders \
  --pair-data my_pair.json
```

## 🤝 Contributing

1. **Report issues**: Use GitHub issues for bugs or feature requests
2. **Submit PRs**: Follow standard GitHub PR process
3. **Documentation**: Help improve guides and examples
4. **Testing**: Test scripts with your mentorship data

## 📞 Support

- **📋 Create an issue**: [Report problems or request features](../../issues/new)
- **📖 Check docs**: [Complete workflow documentation](docs/github_projects_workflow.md)
- **💬 Discussions**: Use GitHub Discussions for questions
- **🏷️ Tag coordinators**: Use `@mentorship-coordinators` for urgent issues

## 🏆 Benefits Over Traditional Approach

| Feature | Old (pairings/ folder) | New (GitHub Projects) |
|---------|----------------------|----------------------|
| **Visibility** | Hidden in folders | Visual project board |
| **Tracking** | Manual file updates | Automated tracking |
| **Search** | File system search | GitHub search & filters |
| **Integration** | None | Issues, Actions, API |
| **Reports** | Manual compilation | Automated generation |
| **Collaboration** | File conflicts | Real-time updates |
| **Mobile** | Limited | GitHub mobile app |
| **Notifications** | Email only | Multiple channels |

## 📈 Program Analytics

The system automatically tracks:
- **Pair progress** and goal completion rates
- **Meeting frequency** and engagement levels  
- **Deliverable completion** timelines
- **Program success metrics** and outcomes
- **Mentor/mentee satisfaction** indicators

## 🎓 Program Tracks Supported

- **Machine Learning & AI**
- **Data Science & Analytics** 
- **Software Engineering**
- **Research & Academia**
- **Career Development**
- **Leadership & Management**
- **Entrepreneurship**
- **Custom tracks** as needed

---

**🌟 Ready to get started?** [Create your first mentorship pair](../../issues/new?template=new_mentorship_pair.md) or [explore the documentation](docs/github_projects_workflow.md)!
