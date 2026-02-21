# Civilization Simulation 🏛️

A high-fidelity Agent-Based Model (ABM) simulating the complex dynamics, evolution, and collapse of civilizations. This project leverages Object-Oriented Programming (OOP) and advanced numerical methods to model population growth and resource competition among different nations.

---

## 🔭 The Vision

> **"To decode the chaotic laws of history using the precision of computational physics."**

---

## 📋 Overview

This project provides a comprehensive simulation of civilization life cycles, tracking the following variables:
- **Population Growth**: Precise simulation using the Logistic equation solved via the **4th-order Runge-Kutta (RK4)** method.
- **Resource Management**: A dynamic system for food production and consumption and its impact on state survival.
- **Conflicts and Warfare**: Modeling stochastic military interactions and their demographic consequences.
- **Civilization Collapse**: Tracking extinction events resulting from recurring famines or devastating wars.

---

## ✨ Key Features

- **Stable Mathematical Modeling**: Implementation of the RK4 algorithm to ensure numerical precision and stability in population dynamics.
- **Multi-Agent Interaction**: Simultaneous simulation of multiple nations (e.g., Nation_A, Nation_B, Nation_C) competing in a shared environment.
- **Dynamic Feedback Loops**: Interdependent relationship between population size, weather-impacted food production, and consumption.
- **Professional Data Visualization**: Integrated charts illustrating population trends and food stocks for each nation over time.

---

## 🏗️ Project Structure

```text
civilization_sim/
├── notebooks/
│   └── visualization.ipynb    # Main file for running the simulation and viewing results
├── src/
│   ├── __init__.py
│   ├── world.py               # Core simulation engine (WorldModel)
│   └── nation.py              # Logic for nations and agents (NationAgent)
└── README.md                  # Project documentation
```

---

## 🔧 Requirements and Setup

### Requirements:
- Python 3.8+
- [Mesa](https://mesa.readthedocs.io/) (ABM framework)
- Matplotlib (Data visualization)
- Jupyter Notebook

### How to Run:
1. **Install the necessary libraries**:
   ```bash
   pip install mesa matplotlib jupyter
   ```
2. **Open the Jupyter Notebook**:
   ```bash
   jupyter notebook notebooks/visualization.ipynb
   ```
3. **Execute the cells**: Run the cells in order to initialize the `WorldModel`, run the simulation for the desired number of years, and generate the plots.

---

## 🔬 Technical Principles

### 1. Population Growth
The simulation relies on the Logistic Growth Equation to represent environmental carrying capacity:
`dP/dt = r * P * (1 - P/K)`
Population counts are updated at each time step using the **RK4 solver** to ensure smooth and accurate transitions.

### 2. Food Management
Food production is calculated based on base production modified by a random weather factor. Food shortages lead to:
- Increased mortality rates (Famine).
- Cessation of natural population growth.

### 3. Warfare System
Wars occur probabilistically between nations. If a nation is stronger (larger population) than a randomly selected neighbor, it may launch an attack. This results in percentage-based population losses for both parties, which can lead to the sudden collapse of civilizations.

---

## 📈 Output Analysis

Upon completion of the simulation (e.g., after 3000 years), the project provides:
1. **Statistical Summary**: Displays final population, status (Alive/Extinct), famine count, and war count.
2. **Visual Charts**:
   - **Solid Line (Blue)**: Represents population change.
   - **Dashed Line (Green)**: Represents food stock.

---

## 📝 Development Notes

- **Modular Design**: Logic (in the `src` folder) is strictly separated from Visualization (in the `notebooks` folder).
- **Auto-Reload**: The notebook utilizes the `autoreload` extension to ensure changes in Python files are detected automatically without restarting the kernel.

---
**Developed as part of a complex systems simulation project.**

Copyright © 2026 Ahmed. All rights reserved.