import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args) #initialize connection
    
    #new node
    node=Node('some_node_name')
    node.get_logger().info("hello world")
    
    node.destroy_node()#clean up node
    rclpy.shutdown()#shut down ROS client library context

#to execute file as script:
if __name__=="__main__":
    main()

