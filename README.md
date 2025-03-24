# ghmap: GitHub Event Mapping Tool

<!-- CI & QA -->
[![Tests](https://github.com/uhourri/ghmap/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/uhourri/ghmap/actions/workflows/python-package.yml)
[![Linting](https://github.com/uhourri/ghmap/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/uhourri/ghmap/actions/workflows/pylint.yml)
[![CodeQL](https://github.com/uhourri/ghmap/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/uhourri/ghmap/actions/workflows/codeql.yml)

<!-- Dependencies & Security -->
[![Dependencies](https://github.com/uhourri/ghmap/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=main)](https://github.com/uhourri/ghmap/actions/workflows/dependabot/dependabot-updates)
[![codecov](https://codecov.io/gh/uhourri/ghmap/branch/main/graph/badge.svg)](https://codecov.io/gh/uhourri/ghmap)

<!-- Meta -->
[![PyPI](https://badgen.net/pypi/v/ghmap?cachebuster=1)](https://pypi.org/project/ghmap)
[![Commits](https://badgen.net/github/last-commit/uhourri/ghmap)](https://github.com/uhourri/ghmap/commits/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/uhourri/ghmap/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/uhourri/ghmap)

ghmap is a Python-based tool designed to process raw GitHub event data and convert it into higher-level, structured actions & activities that reflect contributors’ real intent. By transforming low-level events like PullRequestEvent, CreateEvent, and PushEvent into more meaningful actions and activities, ghmap makes it easier to analyze and understand contributor behavior in large GitHub repositories. Full mappings for events → actions and actions → activities can be found in [event_to_action.json](https://github.com/uhourri/ghmap/blob/main/ghmap/config/event_to_action.json) and [action_to_activity.json](https://github.com/uhourri/ghmap/blob/main/ghmap/config/action_to_activity.json)

The dataset, **"A Dataset of Contributor Activities in the NumFocus Open-Source Community"**, was built using ghmap. It includes +2M activities from +180K contributors across 2.8K repositories and 58 projects over three years. Access it on [Zenodo](https://doi.org/10.5281/zenodo.14230406).


## Repository Structure

<pre><code>
```
.
├── LICENSE                       # Project license (MIT)
├── README.md                     # Project overview and documentation
├── ghmap/                        # Main Python package for GH mapping tool
│   ├── __init__.py               # Marks ghmap as a Python package
│   ├── cli.py                    # Command-line interface entry point
│   ├── config/                   # JSON configs for event/action mappings
│   │   ├── action_to_activity.json   # Rules to map actions → activities
│   │   └── event_to_action.json      # Rules to map events → actions
│   ├── mapping/                 # Logic for mapping events and actions
│   │   ├── __init__.py
│   │   ├── action_mapper.py      # Maps raw events to high-level actions
│   │   └── activity_mapper.py    # Groups actions into structured activities
│   ├── preprocess/              # Event preprocessing logic
│   │   ├── __init__.py
│   │   └── event_processor.py    # Cleans and filters GitHub events
│   └── utils.py                  # Utility functions (load/save helpers)
├── pyproject.toml                # Build system, dependencies, and metadata
├── requirements.txt              # List of Python dependencies
├── setup.py                      # Legacy install script for compatibility
└── tests/                        # Test suite for CLI and mapping logic
    ├── test_cli.py               # CLI integration test using sample data
    └── data/                     # Test fixtures and expected outputs
        ├── sample-events.json         # Input sample GitHub events
        ├── expected-actions.jsonl     # Expected mapped actions
        └── expected-activities.jsonl  # Expected final activities
```
</code></pre>


## Installation

To use this package, ensure you have the following installed:
- Python 3.10 or later

To use the ghmap tool, it's recommended to set up a virtual environment. Follow these steps to install the tool and its dependencies:

### 1. Create a Virtual Environment
If you haven't already, create a virtual environment for the project:

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment. Depending on your operating system, use one of the following commands:
- On macOS/Linux:
```bash
source .venv/bin/activate
```

- On Windows:
```bash
.\.venv\Scripts\activate
```

### 3. Install the Project Using pip

Once the virtual environment is activated, you can install the project and its dependencies from the GitHub repository:
```bash
pip install ghmap
```
This will install the tool along with its dependencies, including tqdm for progress tracking during long computations.

## Usage
Once installed, you can use the ghmap tool to process raw GitHub events. Here’s an example of how to run the tool:
```bash
ghmap --raw-events /path/to/raw-events \
      --output-actions /path/to/output-actions.jsonl \
      --output-activities /path/to/output-activities.jsonl
```

Arguments:

- --raw-events (Required): Path to the folder or file containing raw GitHub event data (.json format).
- --output-actions (Required): Path to save the mapped actions (JSONL format).
- --output-activities (Required): Path to save the mapped activities (JSONL format).
- --actors-to-remove (Optional): List of actors (contributors) to exclude from the events.
- --repos-to-remove (Optional): List of repositories to exclude from the events.
- --orgs-to-remove (Optional): List of organizations to exclude from the events.

## Mapping Process

### 1. Mapping GitHub Events to Actions
Use the schema defined in `ghmap/config/event_to_action.json` to transform raw GitHub events into granular actions. The process is demonstrated in the `ghmap/mapping/action_mapper.py` script.

The **Event-to-Action Mapping** is the first step in transforming raw GitHub events into structured and standardized actions. This process establishes a one-to-one correspondence between GitHub event types and meaningful actions that represent specific contributor operations. The mapping leverages the metadata in each event’s payload to determine the action type and extract relevant details. with this mapping process :

#### 1. Raw GitHub Event

A GitHub event represents an action taken by a contributor on the platform. Events are unstructured JSON objects containing various attributes, including the event type, metadata, and payload. For example:

```json
{
   "type":"IssuesEvent",
   "public":true,
   "payload":{
      "action":"closed",
      "issue":{
         "url":"https://api.github.com/repos/JuliaLang/julia/issues/48062",
         "repository_url":"https://api.github.com/repos/JuliaLang/julia",
         "labels_url":"https://api.github.com/repos/JuliaLang/julia/issues/48062/labels{/name}",
         "comments_url":"https://api.github.com/repos/JuliaLang/julia/issues/48062/comments",
         "events_url":"https://api.github.com/repos/JuliaLang/julia/issues/48062/events",
         "html_url":"https://github.com/JuliaLang/julia/issues/48062",
         "id":1515182791,
         "node_id":"I_kwDOABkWpM5aT9rH",
         "number":48062,
         "title":"Bad default number of BLAS threads on 1.9?",
         "user":{
            "login":"KristofferC",
            "id":1282691,
            "node_id":"MDQ6VXNlcjEyODI2OTE=",
            "avatar_url":"https://avatars.githubusercontent.com/u/1282691?v=4",
            "url":"https://api.github.com/users/KristofferC",
            "html_url":"https://github.com/KristofferC",
            "followers_url":"https://api.github.com/users/KristofferC/followers",
            "following_url":"https://api.github.com/users/KristofferC/following{/other_user}",
            "gists_url":"https://api.github.com/users/KristofferC/gists{/gist_id}",
            "starred_url":"https://api.github.com/users/KristofferC/starred{/owner}{/repo}",
            "subscriptions_url":"https://api.github.com/users/KristofferC/subscriptions",
            "organizations_url":"https://api.github.com/users/KristofferC/orgs",
            "repos_url":"https://api.github.com/users/KristofferC/repos",
            "events_url":"https://api.github.com/users/KristofferC/events{/privacy}",
            "received_events_url":"https://api.github.com/users/KristofferC/received_events",
            "type":"User",
            "site_admin":false
         },
         "labels":[
            {
               "id":61807486,
               "node_id":"MDU6TGFiZWw2MTgwNzQ4Ng==",
               "url":"https://api.github.com/repos/JuliaLang/julia/labels/linear%20algebra",
               "name":"linear algebra",
               "color":"f2b3db",
               "default":false,
               "description":"Linear algebra"
            }
         ],
         "state":"closed",
         "locked":false,
         "assignee":null,
         "assignees":[
            
         ],
         "milestone":{
            "url":"https://api.github.com/repos/JuliaLang/julia/milestones/44",
            "html_url":"https://github.com/JuliaLang/julia/milestone/44",
            "labels_url":"https://api.github.com/repos/JuliaLang/julia/milestones/44/labels",
            "id":7729972,
            "node_id":"MI_kwDOABkWpM4AdfM0",
            "number":44,
            "title":"1.9",
            "description":"",
            "creator":{
               "login":"vtjnash",
               "id":330950,
               "node_id":"MDQ6VXNlcjMzMDk1MA==",
               "avatar_url":"https://avatars.githubusercontent.com/u/330950?v=4",
               "url":"https://api.github.com/users/vtjnash",
               "html_url":"https://github.com/vtjnash",
               "followers_url":"https://api.github.com/users/vtjnash/followers",
               "following_url":"https://api.github.com/users/vtjnash/following{/other_user}",
               "gists_url":"https://api.github.com/users/vtjnash/gists{/gist_id}",
               "starred_url":"https://api.github.com/users/vtjnash/starred{/owner}{/repo}",
               "subscriptions_url":"https://api.github.com/users/vtjnash/subscriptions",
               "organizations_url":"https://api.github.com/users/vtjnash/orgs",
               "repos_url":"https://api.github.com/users/vtjnash/repos",
               "events_url":"https://api.github.com/users/vtjnash/events{/privacy}",
               "received_events_url":"https://api.github.com/users/vtjnash/received_events",
               "type":"User",
               "site_admin":false
            },
            "open_issues":12,
            "closed_issues":68,
            "state":"open",
            "created_at":"2022-03-02T19:34:37Z",
            "updated_at":"2023-01-01T20:19:58Z",
            "due_on":null,
            "closed_at":null
         },
         "comments":1,
         "created_at":"2022-12-31T18:49:47Z",
         "updated_at":"2023-01-01T20:19:58Z",
         "closed_at":"2023-01-01T20:19:57Z",
         "author_association":"MEMBER",
         "body":"Something looks strange with the number of BLAS threads on 1.9, I think.\n\n```julia\njulia> VERSION\nv\"1.9.0-beta2\"\n\njulia> LinearAlgebra.BLAS.get_num_threads()\n1\n```\n\n```julia\njulia> VERSION\nv\"1.8.4\"\n\njulia> LinearAlgebra.BLAS.get_num_threads()\n8\n```\n\nThis should just be with everything default.\n\ncc @staticfloat",
         "reactions":{
            "url":"https://api.github.com/repos/JuliaLang/julia/issues/48062/reactions",
            "total_count":0,
            "+1":0,
            "-1":0,
            "laugh":0,
            "hooray":0,
            "confused":0,
            "heart":0,
            "rocket":0,
            "eyes":0
         },
         "timeline_url":"https://api.github.com/repos/JuliaLang/julia/issues/48062/timeline",
         "performed_via_github_app":null,
         "state_reason":"completed"
      }
   },
   "repo":{
      "id":1644196,
      "name":"JuliaLang/julia",
      "url":"https://api.github.com/repos/JuliaLang/julia"
   },
   "actor":{
      "id":1282691,
      "login":"KristofferC",
      "avatar_url":"https://avatars.githubusercontent.com/u/1282691?",
      "url":"https://api.github.com/users/KristofferC"
   },
   "org":{
      "id":743164,
      "login":"JuliaLang",
      "avatar_url":"https://avatars.githubusercontent.com/u/743164?",
      "url":"https://api.github.com/orgs/JuliaLang"
   },
   "created_at":1672604398000,
   "id":"26170139709"
}
```

#### 2. Mapping Definition

The mapping file defines rules to translate the raw event into a structured action. These rules specify:
- The event type (IssuesEvent).
- Optional payload conditions ("action": "closed").
- Fields to extract and include in the resulting action.

Mapping for the CloseIssue action is defined as follows:
```json
"CloseIssue":{
   "event":{
      "type":"IssuesEvent",
      "payload":{
         "action":"closed"
      }
   },
   "attributes":{
      "include_common_fields":true,
      "details":{
         "issue":{
            "id":"payload.issue.id",
            "number":"payload.issue.number",
            "title":"payload.issue.title",
            "state":"payload.issue.state",
            "author":{
               "id":"payload.issue.user.id",
               "login":"payload.issue.user.login"
            },
            "labels":[
               {
                  "name":"payload.issue.labels.name",
                  "description":"payload.issue.labels.description"
               }
            ],
            "created_date":"payload.issue.created_at",
            "updated_date":"payload.issue.updated_at",
            "closed_date":"payload.issue.closed_at"
         }
      }
   }
}
```

#### 3. Resulting Action

The raw event is transformed into a structured action. Common fields (e.g., event_id, actor, repository) and action-specific details (e.g., issue metadata) are included:

```json
{
   "action":"CloseIssue",
   "event_id":"26170139709",
   "date":"2023-01-01T20:19:58Z",
   "actor":{
      "id":1282691,
      "login":"KristofferC"
   },
   "repository":{
      "id":1644196,
      "name":"JuliaLang/julia",
      "organisation":"JuliaLang",
      "organisation_id":743164
   },
   "details":{
      "issue":{
         "id":1515182791,
         "number":48062,
         "title":"Bad default number of BLAS threads on 1.9?",
         "state":"closed",
         "author":{
            "id":1282691,
            "login":"KristofferC"
         },
         "labels":[
            {
               "name":"linear algebra",
               "description":"Linear algebra"
            }
         ],
         "created_date":"2022-12-31T18:49:47Z",
         "updated_date":"2023-01-01T20:19:58Z",
         "closed_date":"2023-01-01T20:19:57Z"
      }
   }
}
```
### 2. Mapping Actions to Activities

Use the schema defined in `ghmap/config/action_to_activity.json` to aggregate granular actions into high-level activities. This process is demonstrated in the `ghmap/mapping/activity_mapper.py` script.

The **Action-to-Activity Mapping** is the second step in structuring GitHub contributor data. It builds on the Event-to-Action Mapping by grouping related actions into cohesive representations of high-level contributor tasks. Activities encapsulate the broader intent behind individual operations, making them valuable for understanding collaboration and task workflows. with the following mapping precess

#### 1. Actions as Input

Actions, derived from the Event-to-Action Mapping process, serve as the input for this stage. These actions are structured JSON objects containing metadata and detailed attributes. For example:

```json
{
   "action":"CloseIssue",
   "event_id":"26163458157",
   "date":"2023-01-01T00:06:24Z",
   "actor":{
      "id":15819577,
      "login":"mem48"
   },
   "repository":{
      "id":153765492,
      "name":"ropensci/opentripplanner",
      "organisation":"ropensci",
      "organisation_id":1200269
   },
   "details":{
      "issue":{
         "id":755698614,
         "number":78,
         "title":"r5",
         "state":"closed",
         "author":{
            "id":15819577,
            "login":"mem48"
         },
         "labels":[
            {
               "name":"enhancement",
               "description":"New feature or request"
            }
         ],
         "created_date":"2020-12-02T23:54:39Z",
         "updated_date":"2023-01-01T00:06:23Z",
         "closed_date":"2023-01-01T00:06:23Z"
      }
   }
}
```

#### 2. Mapping Definition

The mapping file defines the logic for grouping actions into activities. It specifies:
- The activity type (e.g., CloseIssue).
- Required actions that must occur to form the activity (e.g., CloseIssue).
- Optional actions that may provide additional context (e.g., CreateIssueComment).
- Validation rules to ensure logical consistency (e.g., matching issue numbers between actions).

Mapping for the CloseIssue action is defined as follows:

```json
{
   "name":"CloseIssue",
   "time_window":"3s",
   "actions":[
      {
         "action":"CloseIssue",
         "optional":false,
         "repeat":false
      },
      {
         "action":"CreateIssueComment",
         "optional":true,
         "repeat":false,
         "validate_with":[
            {
               "target_action":"CloseIssue",
               "fields":[
                  {
                     "field":"issue.number",
                     "target_field":"issue.number"
                  }
               ]
            }
         ]
      }
   ]
}
```

#### 3. Resulting Activity

A set of related actions is aggregated into a single activity. Each activity record contains:
- Common fields (e.g., start_date, end_date, actor, repository).
- The list of actions that make up the activity, maintaining traceability to the original operations.

```json
{
   "activity":"CloseIssue",
   "start_date":"2023-01-01T00:06:24Z",
   "end_date":"2023-01-01T00:06:24Z",
   "actor":{
      "id":15819577,
      "login":"mem48"
   },
   "repository":{
      "id":153765492,
      "name":"ropensci/opentripplanner",
      "organisation":"ropensci",
      "organisation_id":1200269
   },
   "actions":[
      {
         "action":"CloseIssue",
         "event_id":"26163458157",
         "date":"2023-01-01T00:06:24Z",
         "details":{
            "issue":{
               "id":755698614,
               "number":78,
               "title":"r5",
               "state":"closed",
               "author":{
                  "id":15819577,
                  "login":"mem48"
               },
               "labels":[
                  {
                     "name":"enhancement",
                     "description":"New feature or request"
                  }
               ],
               "created_date":"2020-12-02T23:54:39Z",
               "updated_date":"2023-01-01T00:06:23Z",
               "closed_date":"2023-01-01T00:06:23Z"
            }
         }
      },
      {
         "action":"CreateIssueComment",
         "event_id":"26163458136",
         "date":"2023-01-01T00:06:24Z",
         "details":{
            "issue":{
               "id":755698614,
               "number":78,
               "title":"r5",
               "state":"closed",
               "author":{
                  "id":15819577,
                  "login":"mem48"
               },
               "labels":[
                  {
                     "name":"enhancement",
                     "description":"New feature or request"
                  }
               ],
               "created_date":"2020-12-02T23:54:39Z",
               "updated_date":"2023-01-01T00:06:23Z",
               "closed_date":"2023-01-01T00:06:23Z"
            },
            "comment":{
               "id":1368298302,
               "position":1
            }
         }
      }
   ]
}
```

This step bridges the gap between granular operations and high-level task representations, enabling nuanced insights into contributor workflows.


---

## Citation

If you use this tool or dataset in your research, please cite:

### 📄 Paper

> **A Dataset of Contributor Activities in the NumFocus Open-Source Community**  
> Youness Hourri, Alexandre Decan, Tom Mens  
> _22nd International Conference on Mining Software Repositories (MSR)_  
> Ottawa (Ontario, Canada) on the 28th and 29th of April, 2025.

```bibtex
@inproceedings{hourri2025dataset,
  title={A Dataset of Contributor Activities in the NumFocus Open-Source Community},
  author={Hourri, Youness and Decan, Alexandre and Mens, Tom},
  booktitle={22nd International Conference on Mining Software Repositories},
  year={2025},
  organization={IEEE}
}
```

### 🛠️ Tool

> **ghmap: GitHub Event Mapping Tool**  
> Youness Hourri

```bibtex
@software{hourri2025ghmap,
  author       = {Hourri, Youness},
  title        = {ghmap: GitHub Event Mapping Tool},
  url          = {https://github.com/uhourri/ghmap},
  note         = {Accessed: 2025-03-21}
}
```

## Contributing

Contributions are welcome! If you identify issues or have suggestions for improvement, please submit an issue or pull request.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact [Youness Hourri](mailto:youness.hourri@umons.ac.be).

