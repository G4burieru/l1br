"""Launch Gazebo with a world that has rocket, as well as the follow node."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_rocket_gazebo = get_package_share_directory('rocket')

    model_arg = DeclareLaunchArgument(name="model", default_value="/home/renata_a/workspace/src/rocket/urdf/robozinho.urdf.xacro")

    robot_description = ParameterValue(
   	    Command(["xacro ", LaunchConfiguration("model")]) ,
      	value_type=str ,
    )
 
    robot_state_publisher_node = Node(
   	 	package= "robot_state_publisher" ,
   	 	executable= "robot_state_publisher" ,
   	 	name= "robot_state_publisher" ,
   	 	parameters= [{"robot_description" : robot_description}],
    )

    # Gazebo launch
    gazebo = Node(
        package="gazebo_ros" ,
        executable="spawn_entity.py" ,
        name="spawn_rocket" ,
        output="screen" ,
        arguments= ["-topic", "/robot_description", "-entity", "rocket"] ,
    )
    
    return LaunchDescription([
        model_arg ,
        gazebo ,
        robot_state_publisher_node ,
    ])
