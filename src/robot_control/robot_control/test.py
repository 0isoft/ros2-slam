import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args) #initialize connection
    
    #new node
    node=Node('some_node_name')
    
    
    node.get_logger().info("hello world")
    
    rclpy.spin(node)

    node.destroy_node()#clean up node: but "spin" makes it such that this part of the code never runs
    rclpy.shutdown()#shut down ROS client library context

#to execute file as script:
if __name__=="__main__":
    main()

