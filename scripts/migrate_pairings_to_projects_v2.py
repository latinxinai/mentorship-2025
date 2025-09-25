import os
import json
import argparse
import requests

GITHUB_API = "https://api.github.com/graphql"

def run_query(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_API, json={"query": query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code}, {response.text}")
    return response.json()

def get_repo_id(owner, repo, token):
    query = f"""
    {{
      repository(owner: "{owner}", name: "{repo}") {{
        id
      }}
    }}
    """
    data = run_query(query, token)
    return data["data"]["repository"]["id"]

def create_project(repo_id, title, token):
    query = f"""
    mutation {{
      createProjectV2(input: {{
        ownerId: "{repo_id}",
        title: "{title}"
      }}) {{
        projectV2 {{
          id
          title
        }}
      }}
    }}
    """
    data = run_query(query, token)
    return data["data"]["createProjectV2"]["projectV2"]

def add_item(project_id, title, token):
    """Add a single item to a project"""
    mutation = f"""
    mutation {{
      addProjectV2ItemById(input: {{
        projectId: "{project_id}",
        content: {{
          title: "{title}"
        }}
      }}) {{
        item {{
          id
        }}
      }}
    }}
    """
    run_query(mutation, token)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--project-title", required=True)
    parser.add_argument("--pair-data", required=True, help="JSON file with mentor-mentee pairs")
    args = parser.parse_args()

    token = args.token
    repo_id = get_repo_id(args.owner, args.repo, token)
    project = create_project(repo_id, args.project_title, token)
    project_id = project["id"]
    print(f"✅ Created project: {project['title']} (ID: {project_id})")

    # Load mentor-mentee pairs
    with open(args.pair_data, "r") as f:
        pairs = json.load(f)

    for pair in pairs:
        mentor = pair["mentor_email"]
        mentee = pair["mentee_email"]
        title = f"{mentor} → {mentee}"
        add_item(project_id, title, token)

    print(f"💾 Added {len(pairs)} mentor-mentee pairs to project.")

if __name__ == "__main__":
    main()
