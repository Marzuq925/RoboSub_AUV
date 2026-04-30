FROM ros:jazzy-ros-core
ARG USERNAME=RoboSub
ARG USER_UID=1001
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y \
    sudo \
    dos2unix \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    build-essential \
    python3-pip \
    python3-dev \
    ros-jazzy-pcl-conversions \
    ros-jazzy-pcl-ros \
    && rm -rf /var/lib/apt/lists/* \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Add user to required groups for GPIO access
RUN usermod -aG dialout $USERNAME \
    && groupadd -f -r gpio \
    && usermod -aG gpio $USERNAME

# Install python libs
RUN apt-get update && apt-get install -y python3-serial && sudo apt install -y ros-$ROS_DISTRO-foxglove-bridge && rm -rf /var/lib/apt/lists/*

# Install Jetson.GPIO
RUN pip3 install Jetson.GPIO --break-system-packages
RUN pip3 install simple-pid --break-system-packages

# Set up GPIO udev rules (needed for non-root GPIO access)
RUN echo 'SUBSYSTEM=="gpio", KERNEL=="gpiochip*", ACTION=="add", PROGRAM="/bin/sh -c '\''chown root:gpio /sys/class/gpio/export /sys/class/gpio/unexport ; chmod 220 /sys/class/gpio/export /sys/class/gpio/unexport'\''"' > /etc/udev/rules.d/99-gpio.rules \
    && echo 'SUBSYSTEM=="gpio", KERNEL=="gpio*", ACTION=="add", PROGRAM="/bin/sh -c '\''chown root:gpio /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value ; chmod 660 /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value'\''"' >> /etc/udev/rules.d/99-gpio.rules

USER $USERNAME

RUN sudo rosdep init || true
RUN rosdep update

WORKDIR /workspaces/RoboSub_AUV
COPY ros2_ws ./ros2_ws

RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && cd /workspaces/RoboSub_AUV && colcon build --symlink-install"

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc \
    && echo "source /workspaces/RoboSub_AUV/install/setup.bash" >> ~/.bashrc

RUN find /workspaces/RoboSub_AUV/ros2_ws/src -name "*.py" -exec sudo chmod +x {} \;