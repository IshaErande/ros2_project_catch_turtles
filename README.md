
# ROS2 Catch Them All Project

This project demonstrates a **turtle-catching mechanism** in ROS2 using `turtlesim`. The system simulates a scenario where a main turtle follows target turtles. Upon catching a target, new turtles are spawned dynamically, continuing the loop.

Custom **messages (msg)** and **services (srv)** are used to manage turtle states and catching events between nodes.

---

## Repository Structure

```
├── catch_them_all_interfaces              
│   ├── msg
│   │   ├── TurtleArray.msg               
│   │   └── TurtleCoordinates.msg          
│   ├── srv
│   │   └── CatchTurtle.srv                
│   ├── CMakeLists.txt
│   └── package.xml
│
└── turtle_catch_them_all_pkg             
    ├── resource
    ├── test
    ├── turtle_catch_them_all_pkg
    │   ├── __init__.py
    │   ├── spawn_turtle.py                 
    │   └── turtle_controller.py           
    ├── package.xml
    ├── setup.cfg
    ├── setup.py
    └── README.md
```

---

## Interface Definitions

### Messages

1. **TurtleCoordinates.msg**
    ```plaintext
    float64 x
    float64 y
    float64 theta
    string name
    ```

2. **TurtleArray.msg**
    ```plaintext
    TurtleCoordinates[] turtles
    ```

### Services

1. **CatchTurtle.srv**
    ```plaintext
    string name
    ---
    bool success
    ```

---

## Package Breakdown

### 1. **catch_them_all_interfaces/**
- Defines custom message and service types to structure communication between nodes.
- **Used by**: Both `spawn_turtle.py` and `turtle_controller.py` for publishing turtle states and service calls.

### 2. **turtle_catch_them_all_pkg/**
- **spawn_turtle.py**:
  - Spawns initial target turtles after the simulation starts.
  - Publishes active turtle positions on `/turtle_array` topic.
  - Implements `/catch_turtle` service server to handle catch requests and spawn new turtles upon successful catch.
- **turtle_controller.py**:
  - Subscribes to `/turtle_array` to obtain live turtle positions.
  - Computes velocity commands for the main turtle to follow the current target turtle.
  - Calls `/catch_turtle` service to report when a turtle is caught.

---

## ROS2 Communication Overview

| Communication Type | Name                | Interface                 | Publisher / Server            | Subscriber / Client           |
|--------------------|--------------------|---------------------------|-------------------------------|-------------------------------|
| Topic               | `/turtle_array`    | `TurtleArray.msg`          | Publisher: `spawn_turtle.py`  | Subscriber: `turtle_controller.py` |
| Service             | `/catch_turtle`    | `CatchTurtle.srv`          | Server: `spawn_turtle.py`     | Client: `turtle_controller.py` |

---

## Execution Flow

1. Launch `turtlesim_node` to start the turtlesim simulation.
2. Run `spawn_turtle.py` to spawn a target turtle and start publishing their positions.
3. Run `turtle_controller.py` to control the main turtle which follows the current target.
4. When the main turtle gets close enough to a target, `turtle_controller.py` will call the `/catch_turtle` service.
5. On successful catch, `spawn_turtle.py` will delete the caught turtle and spawn a new target turtle.
6. The cycle continues indefinitely.

---

## Build & Run Instructions

### Prerequisites
- Ubuntu 22.04
- ROS2 Humble
- turtlesim package
- colcon 

### Build after cloning the remository
 Navigate to the repository
# Build packages using
~~~
colcon build
~~~

# Source the overlay
~~~
source install/setup.bash
~~~
### Run Simulation

# 1. Launch turtlesim
~~~bash
ros2 run turtlesim turtlesim_node
~~~
# 2. Run spawn_turtle node
~~~
ros2 run turtle_catch_them_all_pkg spawn_turtle
~~~
# 3. Run turtle_controller node
~~~
ros2 run turtle_catch_them_all_pkg turtle_controller
~~~

