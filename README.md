Test code to confirm ROS2 nodes working within docker container  
  
To run pull repo  
CD into repo  
Then do: docker build . -t auv/latest  
Then: docker run -it auv/latest  
Source the install/setup.bash file  
set the test_node.py file to be executable  
and the do ros2 run test_package test_node.py  
