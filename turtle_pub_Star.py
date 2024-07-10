#!/usr/bin/env python3
import rclpy  # Import ROS2 Python library
from rclpy.node import Node  # Import Node module
from std_msgs.msg import String  # Import String message type
from geometry_msgs.msg import Twist
# Class definition for our ROS2 publisher node
class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')  # Initialize the Node with the name 'my_publisher'
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # Create a publisher
       # self.publisher1_ = self.create_publisher(String, 'Mytopic', 10)  # Create a publisher
        self.timer = self.create_timer(1.0, self.timer_callback)  # Create a timer to call the callback every 0.5 seconds
        self.side_count = 0
        self.state = 'move'
        self.last_state = 'turn2'
    
    def timer_callback(self):
        msg = Twist()  # Create a new String message
        if self.state == 'move':
            msg.linear.x=1.0
            msg.angular.z=0.0
        elif self.state == 'turn1':
            msg.linear.x=0.0
            msg.angular.z=4.39823
        elif self.state == 'turn2':
            msg.linear.x=0.0
            msg.angular.z=0.628319

        self.publisher_.publish(msg)  # Publish the message
        
        if (self.state == 'move') and (self.last_state == 'turn2'):
            self.last_state = self.state
            self.state='turn1'
            self.side_count +=1

        elif (self.state == 'turn1') and (self.last_state == 'move'):
            self.last_state = self.state
            self.state='move'
            self.side_count +=1

        elif (self.state == 'move') and (self.last_state == 'turn1'):
            self.last_state = self.state
            self.state='turn2'
            self.side_count +=1

        elif (self.state == 'turn2') and (self.last_state == 'move'):
            self.last_state = self.state
            self.state='move'
            self.side_count +=1

            self.get_logger().info('Side_count: "%d"' %self.side_count)
        
        if self.side_count >=20:
            self.timer.cancel()
            self.get_logger().info('Done')

        

        
def main(args=None):
    rclpy.init(args=args)  # Initialize ROS2 Python communication
    my_publisher = MyPublisher()  # Create a MyPublisher object
    rclpy.spin(my_publisher)  # Keep the node alive to continue publishing

    my_publisher.destroy_node()  # Cleanup the node
    rclpy.shutdown()  # Shutdown ROS2 Python communication

if __name__ == '__main__':
    main()