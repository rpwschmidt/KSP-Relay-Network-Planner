# 🚀 KSP Relay Network Planner
A visual planning tool for designing relay satellite networks in *Kerbal Space Program (KSP)*.

This **Python** application helps you determine satellite configurations around celestial bodies, taking into account communication range, signal strength, orbital mechanics, and antenna configurations.

## Project Goal

Designing relay networks in KSP can be tough and time-consuming, especially for beginners. This tool aims to:
* Simplify planning of relay constellations
* Provide accurate orbital calculations
* Visualize satellite placement and communication links


## Features

### 🛰️ Relay Network Design
* Configure a number of satellites (≥ 3)
* Set the number of antennas per satellite
* Choose relay and vessel antennas
* Visualize satellite spacing and interconnections

### 📡 Signal Strength & Communication
* Adjustable **minimum signal strength threshold**
* Computes maximum communication distance using KSP mechanics
* Automatically enforces communication constraints

### 🌍 Orbital Mechanics
* Calculates:
  * Minimum viable orbit (geometric + atmospheric)
  * Maximum orbit based on signal range
  * Ideal circular orbit for evenly spaced satellites
* Supports:
  * **Precision modes**:
    * Nearest second
    * Nearest minute
    * Nearest hour (for cleaner synchronization)
* Displays orbital period in **Kerbal time format**
  *(1 Kerbal day = 6 hours)*

### 🌐 Geostationary Orbit Support
* Automatically detects if a body supports a synchronous orbit
* If valid (and checked), uses geostationary orbit as the ideal orbit and displays the orbital period

### 🔄 Phasing Orbits
* Calculates and visualizes:
  * Lower phasing orbit
  * Higher phasing orbit
* Helps with **even satellite deployment**

### 📊 Visualization
* Rendering using [matplotlib](https://github.com/matplotlib/matplotlib)
* Shows:
  * Planet and atmosphere
  * Minimum / maximum / ideal orbit
  * Phasing orbits
  * Satellite positions
  * Inter-satellite links

### ⚠️ Validation & Feedback
* Built-in checks for:
  * Impossible orbits (inside planet / atmosphere)
  * Insufficient signal strength
  * Unsafe phasing orbits


## 🖥️ User Interface
Built with [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter) + **Matplotlib**:
* Dropdown menus for body and antennas
* Sliders for:
  * Number of satellites
  * Number of antennas
  * Signal strength threshold
* Period precision selector
* Live-updating visualization
* Message box for warnings and feedback


## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/rpwschmidt/KSP-Relay-Network-Planner.git
cd KSP-Relay-Network-Planner
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install customtkinter matplotlib numpy
```


## ▶️ Usage
Run the application:
```bash
python main.py
```
Or rename `main.py` :arrow_right: `main.pyw` and double-click the file.


## 🧭 How to Use
1. Select a celestial body

2. Choose:
   * Relay antenna
   * Vessel antenna

3. Adjust:
   * Number of satellites
   * Antennas per satellite
   * Minimum signal strength

4. Select **period precision** (seconds, minutes, or hours)

5. Observe:
   * Ideal orbit
   * Satellite positions
   * Phasing orbits

6. Check messages for warnings or constraints


### Ideal Orbit Strategy
Two modes:

#### 1. Coverage-Optimized
* Maximizes orbital radius within signal constraints
* Ensures evenly spaced satellites

#### 2. Geostationary (if available)
* Uses predefined synchronous orbit radius
* Validates against:
  * Signal strength
  * Minimum altitude

## ⚠️ Known Limitations
* Does not simulate:
  * Occlusion by terrain
  * Time-varying signal loss

* Assumes:
  * Perfect circular orbits
  * Even satellite spacing

## 🤝 Contributing
Contributions are welcome!
