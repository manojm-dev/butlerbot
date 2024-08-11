import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare, FindPackagePrefix


def generate_launch_description():

    world_name = 'cafe'
    ros_base_path = '/opt/ros/' + os.environ['ROS_DISTRO']

    pkg_share = FindPackageShare('butlerbot_rmf_gazebo').find('butlerbot_rmf_gazebo')
    pkg_butlerbot_gazebo = FindPackageShare('butlerbot_gazebo').find('butlerbot_gazebo')

    # openrmf classic gazebo plugins
    rmf_robot_sim_gz_classic_plugins = os.path.join(ros_base_path, 'lib', 'rmf_robot_sim_gz_classic_plugins')
    rmf_building_sim_gz_classic_plugins = os.path.join(ros_base_path, 'lib', 'rmf_building_sim_gz_classic_plugins')

    # openrmf gazebo sim plugins
    # rmf_robot_sim_gz_plugins = FindPackagePrefix('rmf_robot_sim_gz_plugins').find('rmf_robot_sim_gz_plugins')
    # rmf_building_sim_gz_plugins = FindPackagePrefix('rmf_building_sim_gz_plugins').find('rmf_building_sim_gz_plugins')

    # File paths
    world_path = os.path.join(pkg_share, 'maps', world_name, f'{world_name}.world')
    world_models_path = os.path.join(pkg_share, 'maps', world_name, 'models')
    models_path = os.path.join(pkg_share, 'models')
    print(models_path)

    # Launch configuration variables with default values 
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')

    declare_arguments = [
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use gazebo clock'
        ),
        DeclareLaunchArgument(
            name='world',
            default_value=world_path, 
            description='Absolute path of gazebo WORLD file'
        ),
    ]

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + ':' + world_models_path + ':' + models_path 
    else:
        os.environ['GAZEBO_MODEL_PATH'] = world_models_path + ':' + models_path 

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + rmf_robot_sim_gz_classic_plugins + ':' + rmf_building_sim_gz_classic_plugins
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = rmf_robot_sim_gz_classic_plugins + ':' + rmf_building_sim_gz_classic_plugins

    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))


    # Open simulation environment
    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_butlerbot_gazebo, 'launch', 'gazebo.launch.py'))
    )


    return LaunchDescription(
        declare_arguments + [
            start_gazebo
            ]
    )
