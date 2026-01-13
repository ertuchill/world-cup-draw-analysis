# 🏆 World Cup 2026 Draw Simulator & Probability Engine

<p align="left">
  <a href="https://two026-world-cup-draw-simulation.onrender.com" target="_blank">
    <img src="https://img.shields.io/badge/Render-Live_Demo-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://www.youtube.com/watch?v=pK6W1DT9OQM" target="_blank">
    <img src="https://img.shields.io/badge/YouTube-Project_Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Project Video">
  </a>
</p>

This project is a full-stack web application designed to simulate the official FIFA World Cup 2026 group stage draw. It implements complex FIFA-mandated constraints and analyzes the resulting matchup probabilities through large-scale simulations.

## 🎥 Project Presentation
Check out the video where I explain the technical details, algorithm logic, and show the simulation in action:

[![World Cup 2026 Simulation Walkthrough](https://img.youtube.com/vi/pK6W1DT9OQM/0.jpg)](https://www.youtube.com/watch?v=pK6W1DT9OQM)
> 💡 **Note:** Since the project is hosted on a free tier, the initial load may take around **30-40 seconds** as the server "wakes up." Thank you for your patience.

## 🎯 The Problem & Solution
FIFA's draw rules—such as geographical separation (except for UEFA) and group limits—significantly skew the probability of certain matchups. To address this, I developed:
* **A Draw Engine:** A validation-based system that ensures every generated draw follows 100% of the official tournament rules.
* **An Analysis Engine:** A Python-based Monte Carlo simulation that runs **10,000+ iterations** to calculate and visualize the likelihood of each country facing specific opponents.

## WebSite Deployment
https://two026-world-cup-draw-simulation.onrender.com

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** JavaScript (ES6+), HTML5, CSS3
* **Data Analysis:** Python Simulation Scripts

## 📦 How to Run
1. Clone the repository: `git clone https://github.com/ertuchill/world-cup-draw-analysis.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access the simulator via `http://localhost:5000`
