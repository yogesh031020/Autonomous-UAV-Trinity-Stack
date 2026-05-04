from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    """
    Project 2: Swarm Launch System [v1.0]
    Spawns multiple agents in isolated namespaces for decentralized coordination.
    """
    
    # 1. Drone 1 Stack
    drone_1_guardian = Node(
        package='guardian_system',
        executable='guardian_node',
        namespace='drone_1',
        name='guardian',
        parameters=[{'battery_critical_threshold': 10.5}]
    )
    
    drone_1_logger = Node(
        package='guardian_system',
        executable='black_box_logger',
        namespace='drone_1',
        name='logger'
    )

    # 2. Drone 2 Stack
    drone_2_guardian = Node(
        package='guardian_system',
        executable='guardian_node',
        namespace='drone_2',
        name='guardian',
        parameters=[{'battery_critical_threshold': 10.8}] # Different threshold for testing
    )
    
    drone_2_logger = Node(
        package='guardian_system',
        executable='black_box_logger',
        namespace='drone_2',
        name='logger'
    )

    # 3. Global Swarm Coordinator
    coordinator = Node(
        package='swarm_coordinator',
        executable='swarm_coordinator',
        name='coordinator'
    )

    # 4. Map Merger
    map_merger = Node(
        package='swarm_coordinator',
        executable='map_merger',
        name='map_merger'
    )

    return LaunchDescription([
        drone_1_guardian,
        drone_1_logger,
        drone_2_guardian,
        drone_2_logger,
        coordinator,
        map_merger
    ])
