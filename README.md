# ros2-slam
the purpose of this document is to track my own understanding of ROS2 as i'm expanding an exploratory project
no AI has been used to write the code, nor this documentation.


## 20.08.2026: setting up first package and node

### ros nodes and topics
node = just a script that is running (somewhere on a jetson nano, for example). 

nodes can be publishers or subscribers, and communicate through topics, over which one transmits messages.
so basically a ros topic is like a kafka topic, except you don't get the replays/persistence associated with kafka

node has a responsibility and is executing code. topic is the communication channel. message is the actual content transmitted between nodes (in a given format, but think of it like a struct)

also worth noting that there was a master node which was the 'orchestrator' in ros1, but ros2 is decentralized

nodes can publish or subscribe to a topic.


```
import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args) #initialize connection
    
    #new node
    node=Node('some_node_name')
    node.get_logger().info('hello world')
    node.destroy_node()
    rclpy.shutdown()

#to execute file as script:
if __name__=="__main__":
    main()
```
 here: octavian@octavian-VMware20-1:~/ros2_ws/robot-stack/src/robot_control/robot_control$ nano test.py.
 
 ive also changed setup.py to include entry point=main function that ive written, in **setup.py**
```
...
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='octavian',
    maintainer_email='octavian@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': 'test_node_executable=robot_control.test:main',
    },
)
```

this was my hello world script.

this references rclpy=ROS Client Library for Python = make ROS aware of the python script ("build ros graph")

this is then 'compiled' with colcon (python code is not compiled, but the workspace containing the python scripts is assembled by colcon)

```bash

octavian@octavian-VMware20-1:~/ros2_ws/robot-stack$ colcon build --symlink-install
Starting >>> robot_control
Finished <<< robot_control [1.24s]          

Summary: 1 package finished [1.43s]

```

symlink = use symbolic links (pointers) s.t. you don't have to rebuild everything when making changes to existing python files
(note: this wont work with cpp files, those need to actually be re-compiled).
colcon produces a binary executable


## 21.08.2026 - creating publishers and subscribers

spin = keep node alive

every time you open a new terminal to run ros2, you need to run
```bash
source install/setup.bash
```

but this can be avoided if you you add it "to bashrc"

```bash
nano ~/.bashrc
```

and add

```bash
source /home/octavian/ros2_ws/install/setup.bash
```

### creating a publisher
a new script was created,
```py
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
```

what this does, is that it instantiates a TestPublisher instance. what is a TestPublisher instance? is just a Node,
called "test_publisher" by ROS, to which we set the attribute 'publisher' as the object returned when we call .create_publisher() method (which is a method all Nodes have).
at this time, we also defined this publisher as writing to a topic called "hello world", and up to 10 messages from this publisher
can be buffered on it. 
can the "10" stack depth argument be avoided? apparently not.

the test_publisher node will use a timer such that every 1s it calls publish_message, which publishes a ROS String message and then logs that op.


one can see the activity on a topic with
```bash
ros2 topic info /name_of_topic
```
(will show publisher count and subscriber count)


here, I also added the subscriber, for completeness
```py
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
            #msg=String() #no longer needed
            
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
```

<img width="877" height="647" alt="Capture d’écran 2026-08-21 à 21 43 05" src="https://github.com/user-attachments/assets/5ec2c5f5-1173-46f1-928e-cbf674bd56d6" />


<img width="1277" height="717" alt="Capture d’écran 2026-08-21 à 21 42 49" src="https://github.com/user-attachments/assets/4b5a2516-e5b5-45c3-af31-6c782f8f8342" />

## 22.08.2026 - ros2 services and actions
topics-stream of data continuously published/subscribed
services-no stream of data. but a server and client relationship (like REST API).

topics are one-to-many and make sense whenever there's a continuous action (like camera frames / sensor data)
services are there for whenever we want to make individual calls to a node. example: reset map, get a config.

we also have "actions", which is like a service, but after the call to the server node is done,
the server keeps a continuous stream of updates going back to the client (time during which the client can make other requests like 'cancel'), good for whenever something can take a longer time to complete (example: move arm, navigate to point)

in all cases, it's event driven in the sense that there is this "executor" which acknowledges that packets have arrived, then dispatches that message and injects the data into the callback methods. this is handled by ros middleware first, then by rclpy/rclcpp

(TODO) provide examples of service/action scripts






