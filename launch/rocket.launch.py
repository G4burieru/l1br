"""Launch Gazebo with a world that has rocket, as well as the follow node."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_rocket_gazebo = get_package_share_directory('rocket')

    # Gazebo launch
    gazebo = Node(
        package="gazebo_ros" ,
        executable="spawn_entity.py" ,
        name="spawn_rocket" ,
        output="screen" ,
        arguments= ["-file", "urdf/robozinho.urdf", "-entity", "rocket", "-z", "0.03"] ,
    )
    
    return LaunchDescription([
        gazebo ,
    ])
