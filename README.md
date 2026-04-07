Test code to confirm ROS2 nodes working within docker container  

Disclaimer: should work on windows but ran into permission issues so I cant verify that yet.    

Use of devcontainers to write code is recommended but not nescessary  

If Ros is installed locally vscode should be able to see the imports, if not then youre kinda working blind in the ide    


prerequisites:
Docker

Makes sure to follow post install steps from docker page on linux  

To run follow the following steps
Pull repo  
CD into repo  
docker build . -t auv:latest or optionally right click on file and click build image in vscode (need docker extension for this. This command constructs the container)  
docker run -it auv:latest(this actually runs it and enters the container in the terminal)  
you should see something like root@(hex string):/workspace/RoboSub#  
you can now run the ros node
ros2 run test_package test_node.py  
