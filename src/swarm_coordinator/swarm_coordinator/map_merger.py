import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import numpy as np

class MapMerger(Node):
    """
    Senior Map Merger Node
    Subscribes to multiple drone occupancy grids and merges them into a global swarm map.
    Demonstrates decentralized SLAM coordination.
    """
    def __init__(self):
        super().__init__('map_merger')
        
        self.drone_maps = {}
        self.merged_map_pub = self.create_publisher(OccupancyGrid, '/swarm/global_map', 10)
        
        # Subscriptions for 2 drones as a demo
        self.create_subscription(OccupancyGrid, '/drone_1/map', lambda msg: self.map_callback(msg, 'drone_1'), 10)
        self.create_subscription(OccupancyGrid, '/drone_2/map', lambda msg: self.map_callback(msg, 'drone_2'), 10)
        
        self.timer = self.create_timer(2.0, self.merge_and_publish)
        self.get_logger().info('Map Merger [v1.0] Active: Listening for multi-agent occupancy grids...')

    def map_callback(self, msg, drone_id):
        self.drone_maps[drone_id] = msg

    def merge_and_publish(self):
        if not self.drone_maps:
            return
            
        # Professional Logic: Assume all maps share the same resolution and origin for this demo
        # In a real system, we would perform coordinate transformation (TF2)
        
        base_map = list(self.drone_maps.values())[0]
        merged_data = np.array(base_map.data, dtype=np.int8)
        
        for drone_id, m_map in self.drone_maps.items():
            incoming_data = np.array(m_map.data, dtype=np.int8)
            # Merge logic: Take the maximum certainty (max value) between maps
            merged_data = np.maximum(merged_data, incoming_data)
            
        # Construct merged message
        merged_msg = OccupancyGrid()
        merged_msg.header = base_map.header
        merged_msg.header.frame_id = 'map'
        merged_msg.info = base_map.info
        merged_msg.data = merged_data.tolist()
        
        self.merged_map_pub.publish(merged_msg)
        self.get_logger().info(f'Published merged global map from {len(self.drone_maps)} agents')

def main(args=None):
    rclpy.init(args=args)
    node = MapMerger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
