#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from test_package.msg import MotorCommands
from simple_pid import PID


class TwistConvNode(Node):
    """A ROS2 Node that converts local frame twists into motor commands."""

    def __init__(self):
        super().__init__('Twist_Conv_Node')

        #Publish to motor commands topic
        self.motor_commands_publisher = self.create_publisher(
            msg_type=MotorCommands,
            topic='/motor_commands',
            qos_profile=1)
        
        #Subscribe to desired twist topic
        self.desired_twist_subscriber = self.create_subscription(
            msg_type=Twist,
            topic='/desired_twist',
            callback=self.desired_twist_subscriber_callback,
            qos_profile=1)
        
        #Variables
        self.MAX_LINEAR_SPEED_X = 1
        self.MAX_LINEAR_SPEED_Y = 1
        self.MAX_LINEAR_SPEED_Z = 1
        self.MAX_ANGULAR_SPEED_X = 1
        self.MAX_ANGULAR_SPEED_Y = 1
        self.MAX_ANGULAR_SPEED_Z = 1

        self.target_linear_vels = Vector3()
        self.target_angular_vels = Vector3()

        yaw_pid = PID(1, 0.1, 0.05, setpoint=0)

        #Periodic Timer
        self.command_period: float = 0.02
        self.timer = self.create_timer(self.command_period, self.timer_callback)


    #Callbacks
    def timer_callback(self):
        """Method that is periodically called by the timer."""
        #TODO: RUN PIDS


    def desired_twist_subscriber_callback(self, msg: Twist):
        """Method that is called when a new msg is received by the node."""
        new_linear_vels = msg.linear
        new_angular_vels = msg.angular
        
        new_linear_vels.x = self.clamp(new_linear_vels.x, self.MAX_LINEAR_SPEED_X)
        new_linear_vels.y = self.clamp(new_linear_vels.y, self.MAX_LINEAR_SPEED_Y)
        new_linear_vels.z = self.clamp(new_linear_vels.z, self.MAX_LINEAR_SPEED_Z)

        new_angular_vels.x = self.clamp(new_angular_vels.x, self.MAX_ANGULAR_SPEED_X)
        new_angular_vels.y = self.clamp(new_angular_vels.y, self.MAX_ANGULAR_SPEED_Y)
        new_angular_vels.z = self.clamp(new_angular_vels.z, self.MAX_ANGULAR_SPEED_Z)

        self.target_linear_vels = new_linear_vels
        self.target_angular_vels = new_angular_vels


        motor_commands = MotorCommands()
        amazing_quote.id = self.incremental_id
        amazing_quote.quote = 'Use the force, Pikachu!'
        amazing_quote.philosopher_name = 'Uncle Ben'

        self.amazing_quote_publisher.publish(amazing_quote)
        

    #Util Function
    def clamp(self, n, max_abs_val):
        return max(-max_abs_val, min(n, max_abs_val))
    

    #Motor Conversions
    def get_linear_thrusts(self, desired_linear_vel_mps: Vector3):
        linear_thrusts = Vector3()

        linear_thrusts.x = desired_linear_vel_mps.x/self.MAX_LINEAR_SPEED_X
        linear_thrusts.y = desired_linear_vel_mps.y/self.MAX_LINEAR_SPEED_Y
        linear_thrusts.z = desired_linear_vel_mps.z/self.MAX_LINEAR_SPEED_Z

    def get_motor_speed(thrust_kg, batt_v):
        x = thrust_kg
        y = batt_v
        if (thrust_kg == 0):
            return 0
        elif (thrust_kg > 0):
            a,b,c,d,e,f = 0.80159994,0.4042657,-0.09132469,-0.01855475,0.00281378,-0.00812859
        else:
            a,b,c,d,e,f = -0.78689061,0.51407952,0.08920133,0.02886842,-0.00272574,-0.01048958
        return a + b*x + c*y + d*x**2 + e*y**2 + f*x*y


def main(args=None):
    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)

        twist_conv_node = TwistConvNode()
        rclpy.spin(twist_conv_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

