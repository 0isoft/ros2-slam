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







