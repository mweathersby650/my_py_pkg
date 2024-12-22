#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
 
from example_interfaces.msg import Int64


from example_interfaces.srv import SetBool
 
class NumberCounterNode(Node): 
    def __init__(self):
        super().__init__("number_counter")
        self.counter = 0
        self.publisher_ = self.create_publisher(Int64, "number_count",10)
        self.subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        self.get_logger().info("Number Counter has been started.")

        
        self.server_ = self.create_service(SetBool, "reset_counter",self.handler_service)
        self.get_logger().info("reset_counter service has been started.")

    def handler_service(self,request,response):

      self.get_logger().info('Incoming request: %s' % request.data)

      response.message = 'Boolean value set to %s' % request.data
      if request.data is True:
        self.counter = 0
        response.message = 'Boolean value set to %s' % request.data
      self.get_logger().info("counter at " + str(self.counter))
      response.success = True
      return response

    def callback_number(self,msg):
       self.get_logger().info("Incoming payload: " + str(msg.data))
       self.counter += msg.data

       self.get_logger().info("Counter incremented to " + str(self.counter))
       outMsg = Int64()
       outMsg.data = self.counter
       self.publisher_.publish(outMsg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()