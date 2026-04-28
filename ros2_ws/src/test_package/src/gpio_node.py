#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import Jetson.GPIO as GPIO
import time


class GPIO_node(Node):
    """A ROS2 Node that manages GPIO pins on the Jetson."""

    def __init__(self):
        super().__init__('GPIO_node')

        print("Hello from GPIO")

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18, GPIO.OUT)

        while True:
            print("High!")
            GPIO.output(7, GPIO.HIGH)
            time.sleep(1)
            print("Low!")
            GPIO.output(7, GPIO.LOW)
            time.sleep(1)


def main(args=None):
    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)

        gpio_node = GPIO_node()
        rclpy.spin(gpio_node)
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

