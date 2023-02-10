from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition , UnlessCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_l1br_gazebo = get_package_share_path('l1br')
    
    teleop_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        arguments=["--ros-args-r", "/cmd_vel:=/diff_cont/cmd_vel_unstamped"],
    )

    return LaunchDescription([
        teleop_node ,
    ])

    

