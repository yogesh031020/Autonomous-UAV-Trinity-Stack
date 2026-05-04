# Project AEGIS: Senior Robotics Environment
# Base Image: Ubuntu 24.04 (Noble Numbat)
FROM ubuntu:24.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install core dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    wget \
    software-properties-common \
    git \
    python3-pip \
    python3-venv \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 1. Setup ROS 2 Jazzy
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && apt-get install -y \
    ros-jazzy-desktop \
    ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Gazebo Harmonic
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    apt-get update && apt-get install -y \
    gz-harmonic \
    && rm -rf /var/lib/apt/lists/*

# 3. Setup micro-XRCE-DDS Agent
RUN git clone --recursive https://github.com/eProsima/Micro-XRCE-DDS-Agent.git /opt/Micro-XRCE-DDS-Agent && \
    cd /opt/Micro-XRCE-DDS-Agent && \
    mkdir build && cd build && \
    cmake .. && make && make install && \
    ldconfig /usr/local/lib/

# 4. Setup PX4 Autopilot SITL
RUN git clone --recursive https://github.com/PX4/PX4-Autopilot.git /opt/PX4-Autopilot && \
    bash /opt/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx --no-sim-tools

# Setup User & Workspace
ARG USERNAME=yogesh
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Fix: Check if group/user exists before creating
RUN if ! getent group $USER_GID; then groupadd --gid $USER_GID $USERNAME; fi \
    && if ! getent passwd $USER_UID; then useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; else usermod -l $USERNAME $(getent passwd $USER_UID | cut -d: -f1); fi \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/project_aegis

# Source ROS 2 by default
RUN echo "source /opt/ros/jazzy/setup.bash" >> /home/$USERNAME/.bashrc

CMD ["bash"]
