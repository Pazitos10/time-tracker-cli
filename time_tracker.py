import os
import argparse
import json
from datetime import datetime, timedelta

def new_timestamp():
    return datetime.now().strftime("%d/%m/%y - %H:%M:%S")

def new_session():
    return {"start": new_timestamp(), "end": None}

def get_project(project, data):
    for p in data.get("projects"):
        if p.get("project_name") == project:
            return p

def create_project(project_name, data=None):
    data = data or {"projects": []}
    data.get("projects").append({
            "project_name": project_name,
            "sessions": [new_session()],
        })
    return data

def update_project(project, data):
    for i, p in enumerate(data.get("projects")):
        if p.get("project_name") == project.get("project_name"):
            data.get("projects")[i] = project
            break
    return data

def save(data, path):
    with open(path, "w+") as f:
        json.dump(data, f)

def load(project_name, path):
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.loads(f.read())
            project = get_project(project_name, data)
            if project:
                project = add_timestamp(project)
                return update_project(project, data)
            else:
                return create_project(project_name, data)
    else:
        return create_project(project_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="project name")
    parser.add_argument("-p", "--path", help="Path to the JSON data file", default="data.json")
    args = parser.parse_args()
    project = args.project
    path = args.path
    if project and path:
        print(f"working on \'{project}\'")
        data = load(project, path)
        save(data, path)
        print(data)

def add_timestamp(project):
    last_session = project.get("sessions")[-1]
    if last_session.get("start") and last_session.get("end"):
        project.get("sessions").append(new_session())
    elif not last_session.get("end"):
        last_session.update({"end": new_timestamp()})
    return project

def calculate_subtotal():
    pass

def calculate_total():
    pass

if __name__ == '__main__':
  main()
