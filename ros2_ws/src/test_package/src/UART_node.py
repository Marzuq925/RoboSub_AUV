#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import time


class UART_node(Node):
   """A ROS2 Node that manages UART comms between Jetson and Pico."""


   def __init__(self):
       super().__init__('UART_node')


       #Initialize an unique ID for this pico boot cycle
       self.id_file = "UART_pico_id.txt"
       self.pico_id = 0


       #Open the serial port
       self.serial_port = serial.Serial(
           port="/dev/ttyTHS1",
           baudrate=38400,
           bytesize=serial.EIGHTBITS,
           parity=serial.PARITY_ODD,
           stopbits=serial.STOPBITS_ONE,
       )
       self.serial_port.reset_input_buffer()


       #Define Variables
       self.time_last_sent_command = time.time()
       self.time_last_recv_command = time.time()


       self.time_last_pair_attempted = time.time()
       self.pairing_cooldown_s = 1


       self.msg_buffer = ""
       self.end_of_packet = 0
       self.prev_ack_index = 0


       self.commanded_vel = 1 #TODO: Make this be based on a topic


       #Periodic Timer
       self.timer_period: float = 0.005
       self.command_period: float = 0.02
       self.timer = self.create_timer(self.timer_period, self.timer_callback)




   def timer_callback(self):
       """Method that is periodically called by the timer."""
       self.process_msg()

       if (time.time() - self.time_last_sent_command >= self.command_period):
           self.send_command()
           self.time_last_sent_command = time.time()   


       if (time.time() - self.time_last_recv_command > self.command_period*3):
           self.time_last_recv_command = time.time()
           print("SELF>DID_NOT_RECV_PACKET")


   #ID/File Ops
   def write_number(self, number: int) -> None:
       with open(self.id_file, 'w') as f:
           f.write(str(number))


   def read_number(self) -> int:
       with open(self.id_file, 'r') as f:
           return int(f.read().strip())


   def increment_number(self) -> int:
       number = read_number() + 1
       write_number(number)
       return number


   #Transmitting
   def send_command(self):
       for i in range(8):
           self.serial_port.write(self.commanded_vel.to_bytes(1, byteorder='big'))
       self.serial_port.write(self.end_of_packet.to_bytes(1, byteorder='big'))

       self.commanded_vel += 1
       if (self.commanded_vel > 255):
           self.commanded_vel = 1


   def send_paring_ack(self):
       if (time.time() - self.time_last_pair_attempted > self.pairing_cooldown_s):
        #    self.pico_id = increment_number()
           self.pico_id = 0
           self.serial_port.write(b'ACK:ID')
           self.serial_port.write(self.end_of_packet.to_bytes(1, byteorder='big'))
           print("Pico Reboot Detected, assigning new ID")
           self.time_last_pair_attempted = time.time()


   #Receiving
   def process_msg(self):
       while (self.serial_port.in_waiting > 0):
           data = self.serial_port.read()
           if(data == b'\x00'):
               if (len(self.msg_buffer) > 0): print(str(self.pico_id) + '>' + self.msg_buffer)
               self.msg_buffer = ""
               self.time_last_recv_command = time.time()
           else:
               if "ACK:" in self.msg_buffer:
                   index = int.from_bytes(data, "big")
                   if (index != self.prev_ack_index+1 and self.prev_ack_index != 255): print("SELF>NONSEQUENTIAL_ACK")
                   self.prev_ack_index = index
                   self.msg_buffer += str(index)
               else:
                   self.msg_buffer += data.decode("utf-8", errors="replace")


               if "REQ:ID" in self.msg_buffer:
                   self.send_paring_ack()


def main(args=None):
   """
   The main function.
   :param args: Not used directly by the user, but used by ROS2 to configure
   certain aspects of the Node.
   """
   try:
       rclpy.init(args=args)


       uart_manager_node = UART_node()


       rclpy.spin(uart_manager_node)
   except KeyboardInterrupt:
       pass
   except Exception as e:
       print(e)


if __name__ == '__main__':
   main()

