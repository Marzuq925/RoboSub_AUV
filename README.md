Test code to confirm ROS2 nodes working within docker container  

prerequisites:
docker

To run pull repo  
CD into repo  
Then do: docker build . -t auv:latest or optionally right click on file and click build image in vscode (need docker extension for this)
Then: docker run -it auv:latest  
Source the install/setup.bash file to make the package recognizable   
set the test_node.py file to be executable  
and the do ros2 run test_package test_node.py  
