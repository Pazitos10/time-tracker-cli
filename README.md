# Time tracker

It's a Python script that allows you to track the time spent working in a given project.
At the moment, this script doesn't have external dependencies so it's ready to run.

#### How to use:

**Help menu:**

`$ python time_tracker.py -h`

```
usage: time_tracker.py [-h] [-p PATH] [-r] project

positional arguments:
  project               project name

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the JSON data file
  -r, --report          Calculate and display a report of the time spent in the project
```

**Start/end working session**:

`$ python time_tracker.py "my_project" "~/Documents/my_project_time_tracker_data.json"`

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
$ python time_tracker.py "my_project" -r

Time spent working on project: 'test'
1 day, 7:52:19
Ongoing sessions: True
Time spent in ongoing session: 0:04:10.492647
```

#### TODO:

- [x] Add more functions to estimate the time spent working in a project (total, mean per day).
- [x] Add an argument to request a "report" of the time spent working in a project.
- [ ] Define behavior for unfinished sessions.
- [ ] Add more documentation.
- [ ] Add a simple GUI (optional).