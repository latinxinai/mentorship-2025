# GitHub Projects Mentorship Workflow

This document describes the new workflow for managing mentor-mentee pairs using GitHub Projects instead of the traditional `pairings/` folder structure.

## Overview

The new system provides:
- **Centralized tracking** via GitHub Projects
- **Automated folder generation** for each pair
- **Structured data format** for consistent information
- **Integration with GitHub Issues** for pair requests
- **Automated workflows** for maintenance

## Project Card Structure

Each mentor-mentee pair is represented by a project card containing:

### Required Fields
- **Pair Names**: Mentor ↔ Mentee
- **Goals**: List of specific objectives
- **Progress**: Current status and achievements
- **Meetings**: Scheduled and completed sessions
- **Deliverables**: Expected outcomes and deadlines
- **Last Updated**: Timestamp of most recent update

### Card Template Format
```markdown
# Jane Doe ↔ John Smith

## 📋 Goals
- Learn machine learning fundamentals
- Complete a capstone project
- Develop professional networking skills

## 📊 Progress
Initial meeting scheduled

## 🤝 Meetings
- 2025-01-15: Kickoff meeting - introductions and goal setting
- 2025-01-29: Weekly check-in #1

## 📦 Deliverables
- Personal development plan (Due: 2025-02-01)
- Mid-program presentation (Due: 2025-04-15)
- Final capstone project (Due: 2025-06-30)

## 🕒 Last Updated
2025-01-10T10:00:00Z
```

## Automated Workflows

### 1. Creating New Pairs

**Via GitHub Issues:**
1. Create an issue with title containing "New Mentorship Pair"
2. Use the issue template (see templates/new_pair_issue_template.md)
3. The automation will:
   - Parse the issue content
   - Create a project card
   - Generate folder structure
   - Close the issue with confirmation

**Via Manual Script:**
```bash
python scripts/manage_mentorship_projects.py \
  --owner latinxinai \
  --repo mentorship-2025 \
  --action create-card \
  --project-id 123 \
  --pair-data templates/pair_template.json
```

### 2. Migration from pairings/ Folder

For repositories with existing `pairings/` folders:

```bash
python scripts/migrate_pairings_to_projects.py \
  --pairings-path pairings \
  --owner latinxinai \
  --repo mentorship-2025 \
  --create-project \
  --generate-folders
```

This will:
- Scan the existing folder structure
- Extract mentorship information
- Create GitHub Project cards
- Generate new organized folder structure
- Create migration report

### 3. Automatic Folder Generation

Each pair gets a structured folder:
```
pairs/
├── jane_doe_john_smith/
│   ├── README.md              # Pair overview
│   ├── goals.md               # Goals and milestones tracker
│   ├── meetings/
│   │   ├── meeting_template.md
│   │   ├── 2025-01-15_kickoff.md
│   │   └── 2025-01-29_weekly.md
│   ├── deliverables/
│   │   ├── development_plan.md
│   │   ├── presentation/
│   │   └── capstone_project/
│   └── resources/
│       ├── reading_list.md
│       └── useful_links.md
```

## Using GitHub Projects

### Project Setup
1. Navigate to your repository
2. Click "Projects" tab
3. Create new project: "Mentorship 2025"
4. Add custom fields:
   - Priority (select): High, Medium, Low
   - Status (select): Not Started, In Progress, Completed
   - Mentor (text)
   - Mentee (text)
   - Last Contact (date)

### Managing Cards
- **Move cards** between columns to track progress
- **Add labels** for program tracks (ML, Data Science, etc.)
- **Set milestones** for important deadlines
- **Assign reviewers** for deliverable reviews

### Regular Maintenance
- Weekly sync runs automatically (Sundays at 12:00 UTC)
- Updates last_updated timestamps
- Checks for stale pairs
- Generates progress reports

## Integration Points

### GitHub Issues
- New pair requests
- Progress updates
- Problem escalations
- Program announcements

### GitHub Actions
- Automated project card creation
- Folder structure generation
- Regular sync and cleanup
- Report generation

### External Tools
- Calendar integration for meetings
- Slack/Discord notifications
- Email reminders
- Analytics dashboards

## Best Practices

### For Mentors
1. Update project cards after each meeting
2. Use consistent meeting note format
3. Track deliverable progress regularly
4. Set clear, measurable goals

### For Program Coordinators
1. Review project board weekly
2. Follow up on stale pairs
3. Monitor goal completion rates
4. Facilitate mentor/mentee matching

### For Mentees
1. Prepare agendas for meetings
2. Update personal progress
3. Ask for help when needed
4. Share achievements and blockers

## Troubleshooting

### Common Issues

**Project card not created:**
- Check GitHub token permissions
- Verify project exists
- Review issue format

**Folder generation failed:**
- Check file permissions
- Verify pair data format
- Review script logs

**Automation not working:**
- Check GitHub Actions status
- Verify webhook configuration
- Review workflow permissions

### Support
- Create an issue with "Support Request" label
- Include relevant error messages
- Provide steps to reproduce
- Tag @mentorship-coordinators

## Migration Timeline

1. **Week 1**: Set up new GitHub Project
2. **Week 2**: Run migration scripts
3. **Week 3**: Train coordinators on new system
4. **Week 4**: Migrate active pairs
5. **Week 5**: Full transition, disable old system

## Future Enhancements

- Integration with calendar systems
- Automated matching algorithms
- Progress analytics dashboard
- Mobile app for quick updates
- AI-powered insights and recommendations