# A* Pathfinding Algorithm Visualization

This project visualizes the A* pathfinding algorithm using Pygame. The implementation demonstrates how the algorithm finds the shortest path between two points on a grid, considering obstacles and the optimal path. 

## Features

- Visualization of the A* pathfinding algorithm.
- Interactive grid where you can set start and end points, as well as barriers.
- Real-time pathfinding with visual feedback.
- Grid customization with different colors representing different states (e.g., open, closed, barriers, start, end).

## Getting Started

### Prerequisites

- Python 3.x
- Pygame

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/astar-pathfinding-visualization.git
    cd astar-pathfinding-visualization
    ```

2. Install the required Python packages:
    ```bash
    pip install pygame
    ```

### Running the Application

To run the visualization, execute the following command:

```bash
python ASTARPY.PY
```

### Usage

- **Left Click**: Place the start point, end point, or barriers on the grid.
- **Right Click**: Remove barriers or reset the grid.
- **Space Bar**: Start the pathfinding visualization.
- **`C` Key**: Clear the grid.

### Colors and Their Meanings

- **White**: Unvisited node.
- **Black**: Start node.
- **Red**: End node.
- **Green**: Open node (being considered).
- **Turquoise**: Closed node (already considered).
- **Orange**: Barrier.
- **Purple**: Path from start to end.

## Code Structure

- **`ASTARPY.PY`**: Main file containing the implementation of the A* algorithm and the Pygame visualization.

### Main Functions and Classes

- **`a_Star()`**: Initializes the Pygame window and sets up the visualization.
- **`Spot`**: Class representing each grid cell with methods to manage its state and interactions.

## Acknowledgments

- Inspiration for the project from various online tutorials and resources on pathfinding algorithms.
