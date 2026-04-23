# A list of 8 (one for each thruster) 1 byte unsigned ints to represent motor throttles, 1 for full revese, 128 for stop, and 255 for full forward
# ros2 topic pub -r 10 /motor_commands test_package/msg/MotorCommands "{thruster0: 0, thruster1: 1, thruster2: 2, thruster3: 3, thruster4: 4, thruster5: 5, thruster6: 6, thruster7: 7}"
# ros2 topic pub --once /motor_commands test_package/msg/MotorCommands "{thruster0: 1, thruster1: 1, thruster2: 2, thruster3: 3, thruster4: 4, thruster5: 5, thruster6: 6, thruster7: 7}"
uint8 thruster0
uint8 thruster1
uint8 thruster2
uint8 thruster3
uint8 thruster4
uint8 thruster5
uint8 thruster6
uint8 thruster7

