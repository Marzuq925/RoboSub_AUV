Test code to confirm ROS2 nodes working within docker container  

prerequisites:
Docker

Makes sure to follow post install steps from docker page on linux  

To run follow the following steps  

Pull repo  
CD into repo  

sudo docker build . -t auv:latest
(optionally right click on file and click build image in vscode (need docker extension for this. This command constructs the container))  

sudo docker run -it --device=/dev/ttyTHS1:/dev/ttyTHS1 auv:latest
(this actually runs it and enters the container in the terminal, and passes the UART port into the docker environment so it can be accessed)  

you should see something like RoboSub@(hex string):/workspace/RoboSub#  
you can now run the ros node

ros2 run test_package test_node.py  
ros2 run test_package motor_output_node.py
