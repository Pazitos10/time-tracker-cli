import os
import argparse
import json
from functools import reduce
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


def load(path):
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="project name")
    parser.add_argument("-p", "--path", help="Path to the JSON data file", default="data.json")
    parser.add_argument("-s", "--summary", help="Calculate and display summary of projects in data file", type=bool, default=False)
    args = parser.parse_args()
    project = args.project
    path = args.path
    summary = args.summary
    if project and path:
        if os.path.exists(path):
            data = load(path)
            if not data:
                data = create_project(project)

            if summary:
                get_summary(data, project)
            else:
                p = get_project(project, data)
                if p:
                    p = add_timestamp(p)
                    data = update_project(p, data)
                else:
                    data = create_project(project, data)    
                
                save(data, path)
                print(f"working on \'{project}\'")
                print(data)
                return data

def add_timestamp(project):
    last_session = project.get("sessions")[-1]
    if last_session.get("start") and last_session.get("end"):
        project.get("sessions").append(new_session())
    elif not last_session.get("end"):
        last_session.update({"end": new_timestamp()})
    return project

def format_date(timestamp):
    return datetime.strptime(timestamp, "%d/%m/%y - %H:%M:%S")

def sum_deltas(deltas):
    initial = timedelta(days=0, hours=0, minutes=0, seconds=0)
    return reduce(lambda d1, d2: d1+d2, deltas, initial)

def get_summary(data, project_name):
    total = calculate_total(data, project_name)
    #import ipdb; ipdb.set_trace()
    print(f"Time spent working on project: '{project_name}'")
    hours = total.seconds // 3600
    minutes = total.seconds // 60
    seconds = total.seconds % 60
    print(f"{total.days} days, {hours} hs, {minutes} min, {seconds} secs.")

def calculate_total(data, project_name):
    projects = data.get("projects")
    for i, p in enumerate(projects):
        if p.get("project_name") == project_name:
            proj = data.get("projects")[i]
            deltas = []
            for s in proj.get("sessions"):
                start = format_date(s.get("start"))
                end = format_date(s.get("end"))
                delta = end - start
                deltas.append(delta)
            return sum_deltas(deltas)
        else:
            print("Project '{project_name}' was not found in data file")

if __name__ == '__main__':
  main()
