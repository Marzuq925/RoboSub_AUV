Test code to confirm ROS2 nodes working within docker container  

prerequisites:
Docker

Makes sure to follow post install steps from docker page on linux  

To run follow the following steps  

Pull repo  
CD into repo  

sudo docker build . -t auv:latest
(optionally right click on file and click build image in vscode (need docker extension for this. This command constructs the container))  

sudo docker run -it \
  --device=/dev/ttyTHS1:/dev/ttyTHS1 \
  --device=/dev/gpiochip0:/dev/gpiochip0 \
  --device=/dev/gpiochip1:/dev/gpiochip1 \
  --group-add $(stat -c '%g' /dev/gpiochip0) \
  --privileged \
  -p 8765:8765 \
  auv:latest
    
  ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765

(this actually runs it and enters the container in the terminal, and passes the UART port into the docker environment so it can be accessed)  

you should see something like RoboSub@(hex string):/workspace/RoboSub#  
you can now run the ros node

ros2 run test_package test_node.py  
ros2 run test_package motor_uart_node.py
ros2 run test_package gpio_node.py

ros2 topic pub -r 10 /motor_commands test_package/msg/MotorCommands "{thruster0: 255, thruster1: 1, thruster2: 2, thruster3: 3, thruster4: 4, thruster5: 5, thruster6: 6, thruster7: 7}"