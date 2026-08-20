# ros2-slam
the purpose of this document is to track my own understanding of ROS2 as i'm expanding an exploratory project
no AI has been used to write the code, nor this documentation.


## 20.08.2026: setting up first package and node

### ros nodes and topics
node = just a script that is running (somewhere on a jetson nano, for example). 

nodes can be publishers or subscribers, and communicate through topics, over which one transmits messages.
so basically a ros topic is like a kafka topic, except you don't get the replays/persistence associated with kafka

node has a responsibility and is executing code. topic is the communication channel. message is the actual content transmitted between nodes (in a given format, but think of it like a struct)

also worth noting that there is a master node which is the 'orchestrator'

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






