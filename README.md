
<p align="center">
  <img height=180 src="./readme_assets/logo.png">
</p>

It's a Python script that allows you to track the time spent working in your projects or tasks.
At the moment, this script doesn't have external dependencies so it's ready to run.

#### Installation: 

`$ pip install time-tracker-cli`

#### How to use:

**Help menu:**

`$ time-tracker-cli -h`

```
usage: time-tracker-cli [-h] [-p PATH] [-r] project

positional arguments:
  project               project name

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the JSON data file
  -r, --report          Calculate and display a report of the time spent in the project
```

**Start/end working session**:

`$ time-tracker-cli -p "~/Documents/my_project_time_tracker_data.json" "my_project"`

The file or project within the file will be created automatically if it doesn't exist.


#### Behavior

The script saves "timestamps" for the working sessions in a JSON file with the following structure:

```
{
   "projects": [
       {
           "project_name": "a_project_name",
           "sessions": [
              {
                  "start": "dd/mm/yy - H:M:S" ,
                  "end": "dd/mm/yy - H:M:S"
              }
           ]
       }
   ]
}
```
Unfinished sessions will have a `null` value in the `end` field.

#### Report

To calculate the time spent working in a project, run:

```
$ time-tracker-cli -r -p "~/Documents/my_project_time_tracker_data.json" "my_project" 

Time spent working on project: 'my_project'
1 day, 7:52:19
Ongoing sessions: True
Time spent in ongoing session: 0:04:10.492647
```

#### TODO:

- [x] Add more functions to estimate the time spent working in a project (total, mean per day).
- [x] Add an argument to request a "report" of the time spent working in a project.
- [x] Add more documentation.
- [x] Add a simple GUI (optional). 
- [ ] Define behavior for unfinished sessions.

#### GUI version

Check out [Time Tracker](https://github.com/pazitos10/time-tracker)
