FROM osrf/ros:jazzy-desktop-full

# Install development tools
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN rosdep init || true
RUN rosdep update

# Set working directory
WORKDIR /AUV

# Copy the ROS2 workspace
COPY ros2_ws ./ros2_ws

# Build the workspace
RUN /bin/bash -c "source /opt/ros/jazzy/setup.sh && colcon build --symlink-install && source install/setup.bash"