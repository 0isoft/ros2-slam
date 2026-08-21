import rclpy
from rclpy.node import Node
from std_msgs.msg import String 

#why import it from there? isnt it a default data type? 
#because this "String" is specific to ROS schema for messages
#a plain python string doesnt carry the ROS message metadata by itself

class TestPublisher(Node):
    def __init__(self):
        super().__init__("test_publisher") #this can't be empty
        #test_publusher is the ROS node name!!
        
        self.publisher=self.create_publisher(String,"/hello_world",10)
        #"10"=relates to a queue depth for the messages
        #(up to 10 messages will be buffered somewhere)

        #create_publisher() is inhereted from Node, and returns a
        #publisher object, which we then attach to TestPublisher


        self.timer=self.create_timer(1.0, self.publish_message)
        #this is kind of a callback, every 1s schedule publish_message 

    def publish_message(self):
            msg=String()
            msg.data="hello from test publisher node"
            self.publisher.publish(msg) 
            
            #self.get_logger().info("published", msg.data)
            #this sort of logging doesn't work,
            #it's not like Python's print()

            #we have to use
            self.get_logger().info(f"published:{msg.data}")
            #instead

def main():
    #before we can create ROS nodes, we need rclpy.init()
    rclpy.init()

    node=TestPublisher()#instance of our publisher node
    rclpy.spin(node)

if __name__=="__main__":
    main()

