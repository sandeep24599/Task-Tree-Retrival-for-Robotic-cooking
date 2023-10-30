# FOON (Functional Object-Oriented Network) Task Planner
# Project Overview
The FOON Task Planner is a Python-based tool designed to facilitate task planning in a functional object-oriented network (FOON) environment. The FOON network consists of functional units (FUs) and objects, representing tasks and the objects involved in those tasks, respectively. This project's primary goal is to find an optimal sequence of FUs to achieve a specific task using various heuristic search methods.

# Features
Search Heuristics: 
The project offers three different heuristic search methods to find optimal task sequences.

Heuristic 1 (Search Heuristic 1): This method prioritizes FUs with the highest success probabilities for motion. It aims to find the most likely path to accomplish a task efficiently.
Heuristic 2 (Search Heuristic 2): This heuristic focuses on minimizing the number of input nodes and considering ingredients when selecting FUs. It aims to reduce the complexity of the task sequence.
IDDFS (Iterative Deepening Depth-First Search): This approach incrementally explores FUs at increasing depth levels, looking for the optimal task sequence.
Leaf Node Detection: The project includes a mechanism to detect leaf nodes in the FOON network, which are the objects at the lowest depth levels that exist in the kitchen.

**# Kitchen Simulation: **
The tool allows you to specify the objects present in the "kitchen," and it helps determine the optimal task sequence to achieve a specific task using objects available in the kitchen.

# Getting Started
Clone this repository to your local machine.
Install the required dependencies.
Update the FOON data files with your own FOON network and object data.
Run the Python script to explore different heuristic search methods and find optimal task sequences.
Usage
Define the FOON network and objects by providing appropriate data files.
Specify the objects present in the kitchen.
Choose a specific goal node, which represents the desired task to accomplish.
Run the Python script to find the optimal task sequence using the provided search heuristics.
Example Data Files
Sample data files for the FOON network, objects, motion probabilities, and utensils are provided as references.
