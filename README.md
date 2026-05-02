# Journey Planner

## Contributors
**Group:** G18

| Name         | UID         |
|--------------|-------------|
| Peng Tsz Yiu | 3036666290  |
| Wang Yujin   | 3036481999  |
| Li Zhao Tian | 3033120221  |
| Han Jiale    | 3036390279  |
| Lu Xinqi     | 3036480696  |


A Python command-line journey planning application for exploring routes in a transport network.  
The project loads stop and route data from CSV files, builds an in-memory network model, and allows users to:

- list available stops
- query ranked journeys between two stops
- find the fastest path
- find the cheapest path
- switch between prepared test networks

## Features

- **Network modelling**
  - Represents stops, routes, transport modes, and the full network structure.
- **CSV-based data loading**
  - Loads stops and routes from files in `test_cases/`.
- **Journey generation**
  - Uses DFS to generate possible journeys between two stops.
  - Filter out journeys that are not pareto optimal.
- **Journey ranking**
  - Supports different preferences:
    - time
    - cost
    - transfers
    - balanced
- **Shortest path search**
  - Uses Dijkstra for fastest and cheapest path queries.
- **Interactive CLI**
  - Users interact through a menu and enter stop **names** instead of internal IDs.

## Project Structure

```text
COMP1110GP/
├── main.py
├── README.md
├── src/
│   ├── dijkstra.py
│   ├── file_loader.py
│   ├── journey_generator.py
│   ├── menu.py
│   ├── network.py
│   └── ranker.py
└── test_cases/
    ├── 1/
    └── 2/
```

## Requirements

- Python 3.10 or newer is recommended
- No third-party packages are required

This project currently uses only the Python standard library.

## How to Run

From the project root:

```bash
python main.py
```

On startup, the program tries to load the default dataset:

- `test_cases/1/stops.csv`
- `test_cases/1/routes.csv`

If loading fails, the program falls back to an empty network and still starts the menu.

## Menu Options

When the program starts, you will see a CLI menu with the following options:

1. **List all stops**
   - Displays all loaded stop names in alphabetical order.
2. **Query journeys (ranked)**
   - Generates candidate journeys between two stop names and ranks them by preference.
3. **Fastest path (Dijkstra)**
   - Finds the shortest path based on total duration.
4. **Cheapest path (Dijkstra)**
   - Finds the shortest path based on total cost.
5. **Load network from test cases**
   - Loads another prepared dataset, for example `1` or `2`.
6. **Exit**

## Input Format

- For journey queries, enter **stop names**, not stop IDs.
- Name matching is case-insensitive.
- If a stop name is not found, the program will ask again.
- If multiple stops share the same name, the program asks for a more specific input.

Example stop names from `test_cases/2`:

- `Central Station`
- `City Hall`
- `Tech Park`
- `Museum District`

## Data Format

### Stops CSV

Expected columns:

```csv
id,name
S001,Central Station
S002,City Hall
```

### Routes CSV

Expected columns:

```csv
start_id,end_id,duration,cost,mode
S001,S002,8,1.5,BUS
S002,S001,8,1.5,BUS
```

Supported transport modes are defined in `src/network.py`:

- `WALKING`
- `BUS`
- `SUBWAY`
- `TRAIN`
- `AIRPLANE`

## Core Modules

- `main.py`
  - Application entry point.
- `src/network.py`
  - Defines `Mode`, `Stop`, `Route`, and `Network`.
- `src/file_loader.py`
  - Loads CSV data and builds the network.
- `src/journey_generator.py`
  - Generates journeys and removes dominated or duplicate results.
- `src/ranker.py`
  - Scores and sorts journeys according to user preference.
- `src/dijkstra.py`
  - Computes the fastest or cheapest path.
- `src/menu.py`
  - Handles user interaction in the terminal.
