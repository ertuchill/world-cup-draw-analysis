# 🏆 World Cup 2026 Draw Simulator & Probability Engine

This project is a full-stack web application designed to simulate the official FIFA World Cup 2026 group stage draw. It implements complex FIFA-mandated constraints and analyzes the resulting matchup probabilities through large-scale simulations.

## 🎯 The Problem & Solution
FIFA's draw rules—such as geographical separation (except for UEFA) and group limits—significantly skew the probability of certain matchups. To address this, I developed:
* **A Draw Engine:** A validation-based system that ensures every generated draw follows 100% of the official tournament rules.
* **An Analysis Engine:** A Python-based Monte Carlo simulation that runs **10,000+ iterations** to calculate and visualize the likelihood of each country facing specific opponents.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=render)https://two026-world-cup-draw-simulation.onrender.com

## 🎥 Project Presentation
Check out the video where I explain the technical details and show the simulation in action:
[**Watch the Project Walkthrough on YouTube**]https://youtube.com/watch/pK6W1DT9OQM?si=YM-QSC0MCAl4pXs_

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** JavaScript (ES6+), HTML5, CSS3
* **Data Analysis:** Python Simulation Scripts

## 📦 How to Run
1. Clone the repository: `git clone https://github.com/ertuchill/world-cup-draw-analysis.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access the simulator via `http://localhost:5000`
