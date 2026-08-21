import rclpy
from rclpy.node import Node
from std_msgs.msg import String 


class TestSubscriber(Node):
    def __init__(self):
        super().__init__("test_subscriber") #this can't be empty
        #test_publusher is the ROS node name!!
        
        self.subscriber=self.create_subscription(String,"/hello_world", self.listen_to_message,10)
        #subscriber listens to the same topic as the publisher (hello_world).
        
        #but according to documentation, we need to specify the callback function instead
        #so it seems that when a message is received, it triggers an event that leads to "listen_to_message"
        #being called
        #instead of using a timer to catch messages received within x seconds or sth


        #self.timer=self.create_timer(1.0, self.listen_to_message) 

    def listen_to_message(self,msg):
            #msg=String() #still needed?
            
            #received_msg=self.subscriber.get(msg) #? how will the message get here?

            # msg is passed as argument to the callback function!!
            # ROS handles passing it from the topic, to the listener, through a "ros executor"
            # ROS invokes the callbacks whenever events occur, and it also prepares the payloads and injects them
        
            self.get_logger().info(f"published:{msg}")

def main():
    #before we can create ROS nodes, we need rclpy.init()
    rclpy.init()

    node=TestSubscriber()#instance of our publisher node
    rclpy.spin(node)

if __name__=="__main__":
    main()

