# Connect-4-AI-Agent

## Overview
This project implements an AI agent to play **Connect 4** using advanced search algorithms and heuristics. The AI is designed to simulate competitive gameplay with efficient decision-making, utilizing minimax-based techniques enhanced by optimizations like alpha-beta pruning and caching.

---

## Algorithms Implemented

### 1. Minimax Without Pruning
- Explores all possible moves up to a specified depth.  
- Uses a caching mechanism to store and reuse heuristic calculations for efficiency.  

### 2. Minimax With Alpha-Beta Pruning
- Optimizes the standard Minimax algorithm by pruning irrelevant branches.  
- Alpha and Beta values help skip branches that do not influence the final decision.  
- Reduces computational complexity and enhances time efficiency.  

### 3. Expectiminimax
- Extends the Minimax algorithm to include **chance nodes** for probabilistic outcomes.  
- Incorporates weighted probabilities for possible random events, simulating realistic scenarios.  
- Balances deterministic strategy with randomness for a versatile AI performance.  

---

## Key Features

### Heuristic Function
The AI evaluates game states using a heuristic function that scores potential board configurations:  
- **Offensive Strategy**:
  - Rewards configurations such as 4-in-a-row (+100,000), 3-in-a-row (+5,000), or 2-in-a-row with free slots (+200 or +10).  
- **Defensive Strategy**:
  - Penalizes potential opponent wins (e.g., 4-in-a-row: -50,000) or strong threats like 3-in-a-row (-4,000).  
- **Positional Advantage**:
  - Encourages center column control (+150) for its strategic value.  

### Optimizations
1. **Caching**: Avoids redundant evaluations by storing heuristic values of previously computed board states.  
2. **Board Representation**: The board is represented as a string instead of a 2D array for space efficiency.  
3. **Move Reordering**: Prioritizes center moves during tree traversal, improving pruning efficiency.

---

## Data Structures
- **Node Class**: Represents each game state with attributes such as board state, depth, value, and child nodes.  
- **Memoization Dictionary**: Stores heuristic values for quick access to previously evaluated states.  
- **Queue for BFS**: Used in visualizing and debugging game trees by level-order traversal.  

---

## Performance Analysis 

### Minimax Without Pruning
| Depth | Nodes Expanded | Time Taken (sec) |
|-------|----------------|------------------|
| 1     | 7              | 0.001            |
| 4     | 2,401          | 0.103            |
| 8     | 5,747,322      | 54.0             |

### Minimax With Alpha-Beta Pruning
| Depth | Nodes Expanded | Time Taken (sec) |
|-------|----------------|------------------|
| 1     | 7              | 0.0008           |
| 4     | 269            | 0.016            |
| 8     | 39,976         | 1.282            |

### Expectiminimax
| Depth | Nodes Expanded | Time Taken (sec) |
|-------|----------------|------------------|
| 1     | 19             | 0.00099          |
| 4     | 361            | 0.0129           |
| 8     | 130,321        | 2.1829           |

---
