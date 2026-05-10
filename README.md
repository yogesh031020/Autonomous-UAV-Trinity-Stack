# Autonomous UAV Trinity Stack: AEGIS, Swarm & Zenith

[![ROS 2](https://img.shields.io/badge/ROS2-Jazzy-blue)](https://docs.ros.org/en/jazzy/index.html)
[![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)](https://gazebosim.org/home)
[![Level](https://img.shields.io/badge/Engineering-Senior-red)](https://github.com/)

A comprehensive, production-grade autonomous drone ecosystem. This repository integrates three core pillars of modern robotics: **Failure Resilience**, **Multi-Agent Coordination**, and **AI-Driven Perception.**


## 🌌 The Trinity Pillars
This repository integrates three core pillars of modern robotics: **Failure Resilience**, **Multi-Agent Coordination**, and **AI-Driven Perception.**

## 🛠️ Flagship Projects

### 🛡️ 1. Project AEGIS (Failure-Resilient Autonomy)
- **Status:** Operational ✅
- **Features:** Multi-state failsafe logic, high-frequency telemetry logging, and Chaos Engineering (Failure Injection) verification.

### 🐝 2. Project Swarm (Collaborative Intelligence)
- **Status:** Operational ✅
- **Features:** Decentralized discovery via Zenoh/DDS, multi-agent occupancy grid merging, and isolated namespace scaling.

### 🔭 3. Project Zenith (Perception & Navigation)
- **Status:** Operational ✅
- **Features:** Simulated YOLOv10 vision stream, reactive potential field obstacle avoidance, and VIO-ready navigation stack.

## 🚀 Getting Started
This entire stack is containerized using Docker for instant reproduction on any system.

```bash
# Clone and Build
cd Autonomous-UAV-Trinity-Stack
docker-compose up -d

# Launch the Full Trinity Stack
ros2 launch swarm_coordinator swarm_launch.py
```

---
*Architected and developed as a Senior Autonomous Systems Portfolio by Yogesh.*
