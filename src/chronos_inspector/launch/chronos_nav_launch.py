from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('chronos_inspector')
    
    # 1. Navigator Node (The Brain)
    navigator = Node(
        package='chronos_inspector',
        executable='navigator_node',
        name='navigator'
    )
    
    # 2. SLAM Toolbox (The Eyes)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py'
        )]),
        launch_arguments={
            'params_file': os.path.join(pkg_share, 'config', 'mapper_params_online_async.yaml'),
            'use_sim_time': 'true'
        }.items()
    )

    # 3. Sensor Simulator (The Hardware)
    sensors = Node(
        package='chronos_inspector',
        executable='sensor_simulator',
        name='sensors'
    )

    # 4. Static Transforms (The Connection)
    tf_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )
    
    tf_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link']
    )

    # 5. Inspection AI (The Eyes)
    detector = Node(
        package='chronos_inspector',
        executable='defect_detector',
        name='detector'
    )

    # 6. Camera Simulator (The Eyes)
    camera = Node(
        package='chronos_inspector',
        executable='camera_simulator',
        name='camera'
    )

    # 7. Mission Reporter (The Manager)
    reporter = Node(
        package='chronos_inspector',
        executable='report_generator',
        name='reporter'
    )

    return LaunchDescription([
        navigator,
        slam,
        sensors,
        tf_odom,
        tf_base,
        detector,
        camera,
        reporter
    ])
