import argparse
import json
import requests

def run_query(query, token, variables=None):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {token}"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    print("[DEBUG] GraphQL response:", json.dumps(result, indent=2))
    return result

def get_authenticated_user(token):
    query = """
    query {
      viewer {
        login
      }
    }
    """
    data = run_query(query, token)
    return data.get("data", {}).get("viewer", {}).get("login")

def get_repo_id(owner, repo, token):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
      }
    }
    """
    variables = {"owner": owner, "name": repo}
    data = run_query(query, token, variables)

    if data.get("data", {}).get("repository"):
        return data["data"]["repository"]["id"]

    # Repo not found under this owner
    print(f"[WARNING] Repo '{repo}' not found under '{owner}'. Trying authenticated user...")
    user = get_authenticated_user(token)
    variables = {"owner": user, "name": repo}
    data = run_query(query, token, variables)
    repo_data = data.get("data", {}).get("repository")
    if repo_data:
        print(f"[INFO] Found repo '{repo}' under user '{user}'")
        return repo_data["id"]
    else:
        errors = data.get("errors", [])
        raise Exception(f"Repository not found under owner '{owner}' or user '{user}'. Errors: {errors}")

def get_owner_id(owner, token):
    query = """
    query($login: String!) {
      user(login: $login) { id }
      organization(login: $login) { id }
    }
    """
    variables = {"login": owner}
    data = run_query(query, token, variables)

    if not data or "data" not in data:
        raise Exception("GraphQL returned no data; check token and login")

    user_data = data["data"].get("user")
    org_data = data["data"].get("organization")

    user_id = user_data.get("id") if user_data else None
    org_id = org_data.get("id") if org_data else None

    if user_id:
        print(f"[INFO] Resolved owner '{owner}' as USER")
        return user_id
    elif org_id:
        print(f"[INFO] Resolved owner '{owner}' as ORG")
        return org_id
    else:
        raise Exception(f"Could not resolve owner '{owner}'. GraphQL errors: {data.get('errors')}")


def create_project(owner, title, token):
    owner_id = get_owner_id(owner, token)
    mutation = f"""
    mutation {{
      createProjectV2(input: {{
        ownerId: "{owner_id}",
        title: "{title}"
      }}) {{
        projectV2 {{
          id
          title
        }}
      }}
    }}
    """
    data = run_query(mutation, token)
    if "errors" in data:
        raise Exception(f"GraphQL error creating project: {data['errors']}")
    project_v2 = data.get("data", {}).get("createProjectV2", {}).get("projectV2")
    if not project_v2:
        raise Exception(f"Failed to create project. Response: {data}")
    print(f"[INFO] Created project '{project_v2['title']}' with ID {project_v2['id']}")
    return project_v2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=False, help="Owner (user/org) of the repo/project")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--project-title", required=True)
    parser.add_argument("--action", choices=["create-project"], required=True)
    args = parser.parse_args()

    token = args.token
    owner = args.owner or get_authenticated_user(token)
    repo_id = get_repo_id(owner, args.repo, token)

    if args.action == "create-project":
        project = create_project(owner, args.project_title, token)

if __name__ == "__main__":
    main()
