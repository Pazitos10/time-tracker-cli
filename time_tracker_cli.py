import os
import argparse
import json
from functools import reduce
from datetime import datetime, timedelta

def new_timestamp():
    # Creates a new timestamp with a specific format.
    return datetime.now().strftime("%d/%m/%y - %H:%M:%S")

def new_session():
    # Creates a new working session dictionary.
    return {"start": new_timestamp(), "end": None}

def get_project(project, data):
    # Returns a specific project from the data dictionary.
    for p in data.get("projects"):
        if p.get("project_name") == project:
            return p

def create_project(project_name, data=None):
    # Creates a new project dictionary and adds it to the data dictionary.
    data = data or {"projects": []}
    data.get("projects").append({
            "project_name": project_name,
            "sessions": [new_session()],
        })
    return data

def update_project(project, data):
    # Replaces an existing project dicionary with a new one.
    for i, p in enumerate(data.get("projects")):
        if p.get("project_name") == project.get("project_name"):
            data.get("projects")[i] = project
            break
    return data

def save_data(data, path):
    # Writes the data dictionary in a JSON file.
    with open(path, "w+") as f:
        json.dump(data, f)


def load_data(path):
    # Reads the data from a JSON file
    if os.path.exists(path):
        f = open(path, "r")
        data = json.loads(f.read())
        f.close()
        return data

def has_ongoing_sessions(project_name, data):
    # Returns True if the data structure has ongoing sessions for a given project. 
    # Otherwise, returns False.
    ongoing = False
    for p in data.get("projects"):
        if p.get("project_name") == project_name:
            for s in p.get("sessions"):
                if s.get("end") is None:
                    ongoing = True
    return ongoing

def get_last_session_timedelta(project_name, data):
    # Returns timedelta and True if the last session is ongoing. Otherwise, returns False.
    p = get_project(project_name, data)
    if p:
        last_session = p.get("sessions")[-1]
        start = format_date(last_session.get("start"))
        if last_session.get("end") is not None:
            end = format_date(last_session.get("end"))
            return end - start, False
        else:
            end = datetime.now()
            return end - start, True
    else:
        return '0:00:00', False

def get_project_names(data):
    # Returns a list with the names of all the projects.
    return [p.get("project_name") for p in data.get("projects")]

def get_total_timedelta(project_name, data):
    # Returns the total time spent working in a project.
    total = calculate_total(project_name, data)
    if total:
        return total.get("completed_sessions")
    else:
        return '0:00:00'

def add_timestamp(project):
    # Adds a new timestamp to a project (start/end). 
    last_session = project.get("sessions")[-1]
    if last_session.get("start") and last_session.get("end"):
        project.get("sessions").append(new_session())
    elif not last_session.get("end"):
        last_session.update({"end": new_timestamp()})
    return project

def format_date(timestamp):
    # Applies a specific format to a date object.
    return datetime.strptime(timestamp, "%d/%m/%y - %H:%M:%S")

def sum_deltas(deltas):
    # Sumarize the timedeltas in a list of deltas.
    initial = timedelta(days=0, hours=0, minutes=0, seconds=0)
    return reduce(lambda d1, d2: d1+d2, deltas, initial)

def get_report(project_name, data):
    # Prints a report for a specific project.
    total = calculate_total(project_name, data)
    if total:
        print(f"Time spent working on project: '{project_name}'")
        print(total.get('completed_sessions'))
        print(f"Ongoing sessions: {total['ongoing_sessions']}")
        print(f"Time spent in ongoing session: {total['ongoing_delta']}")
    else:
        print(f"Project '{project_name}' was not found in data file")

def calculate_total(project_name, data):
    # Calculates the total time spent working in a project.
    projects = data.get("projects")
    project_found = False
    for i, p in enumerate(projects):
        if p.get("project_name") == project_name:
            project_found = True
            proj = data.get("projects")[i]
            deltas = []
            ongoing = False
            ongoing_delta = 0
            for s in proj.get("sessions"):
                if s.get("end") is not None:
                    start = format_date(s.get("start"))
                    end = format_date(s.get("end"))
                    delta = end - start
                    deltas.append(delta)
                else:
                    ongoing = True
                    time_ongoing = datetime.now()
                    ongoing_delta = time_ongoing - format_date(s.get("start"))
            return {
                'completed_sessions': sum_deltas(deltas), 
                'ongoing_sessions': ongoing,
                'ongoing_delta': ongoing_delta
            }
    if not project_found:
        return None

def get_project_index(project_name, data):
    # Returns project index in data file or -1 if not found.
    res = -1
    for idx, p in enumerate(data["projects"]):
        if p["project_name"] == project_name:
            res = idx
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="project name")
    parser.add_argument("-p", "--path", help="Path to the JSON data file", default="data.json")
    parser.add_argument("-r", "--report", help="Calculate and display a report of the time spent in the project", action="store_true")
    args = parser.parse_args()
    project = args.project
    path = args.path
    report = args.report
    if project and path:
        if os.path.exists(path):
            data = load_data(path)
            if not data:
                data = create_project(project)

            if report:
                get_report(project, data)
            else:
                p = get_project(project, data)
                if p:
                    p = add_timestamp(p)
                    data = update_project(p, data)
                else:
                    data = create_project(project, data)    
                
                save_data(data, path)
                print(f"working on \'{project}\'")
                print(data)
                return data


if __name__ == '__main__':
  main()
