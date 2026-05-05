import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import random

class ChronosSensorSim(Node):
    """
    Project CHRONOS: LiDAR Sensor Simulator [v1.0]
    Simulates a 360-degree LiDAR scanner for bridge girders.
    """
    def __init__(self):
        super().__init__('sensor_simulator')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(0.1, self.publish_scan) # 10Hz
        self.get_logger().info('CHRONOS LiDAR Simulator Active.')

    def publish_scan(self):
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'base_link'
        scan.angle_min = 0.0
        scan.angle_max = 2 * math.pi
        scan.angle_increment = math.pi / 180.0 # 1 degree
        scan.range_min = 0.1
        scan.range_max = 20.0
        
        # Simulate being inside a 4m wide girder
        # Distance to left/right wall is ~2m
        scan.ranges = []
        for i in range(360):
            # Add some "noise" to make SLAM work harder (realistic!)
            dist = 2.0 + random.uniform(-0.05, 0.05)
            scan.ranges.append(dist)
            
        self.publisher_.publish(scan)

def main(args=None):
    rclpy.init(args=args)
    node = ChronosSensorSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
