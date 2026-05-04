from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    The Trinity Launch [v1.0]
    Final 100% Portfolio Milestone: Starts all 3 major drone projects.
    """
    
    # 1. Project AEGIS (Safety)
    guardian = Node(
        package='guardian_system',
        executable='guardian_node',
        name='guardian'
    )
    
    # 2. Project Swarm (Coordination)
    coordinator = Node(
        package='swarm_coordinator',
        executable='swarm_coordinator',
        name='coordinator'
    )
    
    # 3. Project Zenith (Perception)
    perception = Node(
        package='vio_nav_stack',
        executable='perception_simulator',
        name='perception'
    )
    
    avoidance = Node(
        package='vio_nav_stack',
        executable='obstacle_avoidance',
        name='avoidance'
    )

    return LaunchDescription([
        guardian,
        coordinator,
        perception,
        avoidance
    ])
