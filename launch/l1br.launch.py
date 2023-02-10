import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition , UnlessCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_l1br_gazebo = get_package_share_path('l1br')
    
    model_arg = DeclareLaunchArgument(name="model", default_value=str(pkg_l1br_gazebo / "urdf/l1br.urdf.xacro"))
    rviz_arg = DeclareLaunchArgument(name="rvizconfig", default_value=str(pkg_l1br_gazebo / "config/rviz_config.rviz"))
    gui_arg = DeclareLaunchArgument(name="gui", default_value="false", choices=["true", "false"], description="Flag to enable joint_state_publisher_gui")

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

    joint_state_publisher_node = Node(
   		package="joint_state_publisher",
   		executable="joint_state_publisher",
   		condition=UnlessCondition(LaunchConfiguration("gui"))
    )

    joint_state_publisher_gui_node = Node(
    package="joint_state_publisher_gui",
    executable="joint_state_publisher_gui",
    condition=IfCondition(LaunchConfiguration("gui"))
    )
    
    # Gazebo launch
    gazebo = Node(
        package="gazebo_ros" ,
        executable="spawn_entity.py" ,
        name="spawn_l1br" ,
        output="screen" ,
        arguments= ["-topic", "/robot_description", "-entity", "l1br"] ,
    )
    
    #Rviz launch
    rviz = Node(
    	package="rviz2",
    	executable="rviz2",
    	name="rviz2",
    	output="screen",
    	arguments= ["-d", LaunchConfiguration("rvizconfig")],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )
    return LaunchDescription([
        model_arg ,
        rviz_arg ,
        gui_arg, 
        rviz ,
        gazebo ,
        diff_drive_spawner ,
        joint_broad_spawner ,
        robot_state_publisher_node ,
        joint_state_publisher_node ,
        joint_state_publisher_gui_node ,
    ])
