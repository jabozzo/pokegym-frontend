# Pokegym

## Description

This repository contains a webpage frontend and a python backend for a pokemon arrival queue. Pokemon arrive in real time (simulated by files) and are displayed on a screen. If more pokemon that fit on a screen arrive at the same time, the list will shift once every second to remove a pokemon already displayed and add an enqueued pokemon for display.

For each batch of pokemon that arrive at the same time, they will be sorted by name before enqueuing the, to be displayed. Time of arrival have priority so the same sorting is performed only inside each pokemon batch.

## Requirements (python)

- flask (1.1.1)
- flask_cors (3.0.8)
- flask_restful (0.3.7)
- requests (2.22.0)
- parsec (3.5, optional)

## Installation

#### Make a virtual environment (optional, recommended)

With conda
```
conda create -n <env_name> python=3
```

Activate the enviroment
```
conda activate <env_name>
```

#### Install the required dependencies

```
pip install flask flask_cors flask_restful requests parsec
```

## Execution

#### Activate the virtual environment (if created)

```
conda activate <env_name>
```

#### Start the backend

```
backend/python/start_backend.py [FILES]
```

Optionally arrival time files can be included if parsec has been installed. Otherwise the backend will assume every pokemon have arrived at the same time at the gym when the server started.

#### Open the frontend

It is located in `frontend/index.html`.


## Arrival time file

An arrival time file is a set of rows. Each row starts with the arrival time (in seconds). The following components are separated by spaces and consists of either pokemon ids or pokemon id ranges.

A pokemon id range has the following format `<id-start>-<id_end>`. A file with a a wave of pokemon arriving at second 2 and then two pokemon arriving at second 100 would look like this:

```
2    34 12 43-90
100  3  4
```

Ids and times cannot start with 0.

## Additional notes

Additional notes can be found on `NOTES.md`
