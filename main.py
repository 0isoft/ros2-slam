#!/usr/bin/python3"""Launch and animate a fake UR5e using its ROS 2 trajectory controller."""
import math
import os
import signal
import subprocess
import sys
import time 
from pathlib import Path

# magic fix to solve dependenciesif os.environ.get("ROS_DISTRO") != "humble" or sys.version_info[:2] != (3, 10):    script = str(Path(__file__).resolve())    os.execvp(        "bash",        [            "bash",            "-c",            'source /opt/ros/humble/setup.bash && exec /usr/bin/python3 "$1"',            "bash",            script,        ],    )
import rclpy
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectoryPoint

JOINT_NAMES = [   
     "shoulder_pan_joint",   
     "shoulder_lift_joint",   
     "elbow_joint",    
     "wrist_1_joint",    
     "wrist_2_joint",    
     "wrist_3_joint",]

class SimpleUr5eMotion(Node):    
    def __init__(self) :        
        super().__init__("simple_ur5e_motion")        
        self.client = ActionClient(self,FollowJointTrajectory,"/joint_trajectory_controller/follow_joint_trajectory",)

    def run(self) :        
        print("Waiting for the UR5e controller...")        
        if not self.client.wait_for_server(timeout_sec=40.0):            
            raise RuntimeError("The joint trajectory controller did not start.")
        
        goal = FollowJointTrajectory.Goal()        
        goal.trajectory.joint_names = JOINT_NAMES

        poses = [            
            ([0.0, -math.pi / 2, math.pi / 2, -math.pi / 2, -math.pi / 2, 0.0], 4),
            ([0.6, -1.2, 1.3, -1.6, -math.pi / 2, 0.5], 8),            
            ([-0.6, -1.2, 1.3, -1.6, -math.pi / 2, -0.5], 12),            
            ([0.0, -math.pi / 2, math.pi / 2, -math.pi / 2, -math.pi / 2, 0.0], 16),        
            ]
        
        for positions, seconds in poses:            
            point = JointTrajectoryPoint()            
            point.positions = positions            
            point.time_from_start.sec = seconds            
            goal.trajectory.points.append(point)

        print("Controller ready. Sending the motion...")        
        send_future = self.client.send_goal_async(goal)        
        rclpy.spin_until_future_complete(self, send_future)        
        goal_handle = send_future.result()       

        if goal_handle is None or not goal_handle.accepted:            
            raise RuntimeError("The controller rejected the trajectory.")
        result_future = goal_handle.get_result_async()        
        rclpy.spin_until_future_complete(self, result_future)        
        result = result_future.result()        
        if result is None or result.result.error_code != 0:            
            error_code = "unknown" if result is None else result.result.error_code            
            raise RuntimeError(f"Motion failed with controller error {error_code}.")
        print("Motion complete.")

    def stop_launch(process: subprocess.Popen):    
        if process.poll() is None:        
            os.killpg(process.pid, signal.SIGINT)       
            try:            
                process.wait(timeout=8)        
            except subprocess.TimeoutExpired:            
                os.killpg(process.pid, signal.SIGTERM)            
            process.wait(timeout=3)

def main() -> int:    
    launch_command = [
               "ros2",        
               "launch",        
               "ur_robot_driver",        
               "ur_control.launch.py",        
               "ur_type:=ur5e",        
               "robot_ip:=0.0.0.0",        
               "use_fake_hardware:=true",        
               "fake_sensor_commands:=true",        
               "initial_joint_controller:=joint_trajectory_controller",        
               "launch_rviz:=true",    ]
    
    print("Starting a fake UR5e and RViz...")    
    launch_process = subprocess.Popen(launch_command, start_new_session=True)    
    node = None
    try:       
        time.sleep(2)        
        if launch_process.poll() is not None:            
            raise RuntimeError("The UR5e launch process exited early.")
        rclpy.init()        
        node = SimpleUr5eMotion()        
        node.run()        
        try:            
            input("RViz will stay open. Press Enter here to close everything... ")        
        except EOFError:            # Allows automated/headless runs to finish without reporting failure.            
            pass        
        return 0    
    except KeyboardInterrupt:        
        print("\nStopping...")        
        return 130    
    except Exception as error:        
        print(f"\nError: {error}", file=sys.stderr)        
        return 1    
    finally:        
        if node is not None:            
            node.destroy_node()        
        if rclpy.ok():            
            rclpy.shutdown()        
        stop_launch(launch_process)

if __name__ == "__main__":    
    raise SystemExit(main())
