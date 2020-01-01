# Time tracker

It's a Python script that allows you to track the time spent working in a given project.
At the moment, this script doesn't have external dependencies so it's ready to run.

#### How to use:

Simply run the script as follows:

`$ python time_tracker.py "my_project" "~/Documents/my_project_time_tracker_data.json"`

This will start a new working session (and a new project if necessary) or finish the last one.

**Help menu:**

`$ python time_tracker.py -h`

```
usage: time_tracker.py [-h] [-p PATH] project

positional arguments:
  project               project name

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the JSON data file
```

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

#### TODO:

- [ ] Add more functions to estimate the time spent working in a project (total, mean per day).
- [x] Add an argument to request a "report" of the time spent working in a project.
- [ ] Define behavior for unfinished sessions.
- [ ] Add more documentation.
- [ ] Add a simple GUI (optional).