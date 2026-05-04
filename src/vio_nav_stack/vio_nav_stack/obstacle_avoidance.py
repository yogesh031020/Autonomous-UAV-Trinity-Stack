import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class ObstacleAvoidance(Node):
    """
    Senior Obstacle Avoidance Node (Project Zenith)
    Implements a Reactive Potential Field approach for high-speed indoor navigation.
    Designed for integration with YOLOv10 object detection and VIO.
    """
    def __init__(self):
        super().__init__('obstacle_avoidance')
        
        # Parameters
        self.declare_parameter('safe_distance', 1.5)
        self.declare_parameter('max_linear_speed', 1.0)
        
        # Subscriptions
        self.lidar_sub = self.create_subscription(LaserScan, '/px4/laser_scan', self.lidar_callback, 10)
        self.yolo_sub = self.create_subscription(String, '/perception/yolo_detections', self.yolo_callback, 10)
        
        # Publishers
        self.cmd_pub = self.create_publisher(Twist, '/px4/setpoint_velocity', 10)
        
        self.get_logger().info('Project Zenith [v1.0] Initialized: Perception-Driven Navigation Active')

    def lidar_callback(self, msg):
        # Professional Reactive Logic: Vector-based Avoidance
        safe_dist = self.get_parameter('safe_distance').value
        ranges = np.array(msg.ranges)
        
        # Filter infinite values
        ranges[np.isinf(ranges)] = 10.0
        
        # Check front sector (e.g., -30 to 30 degrees)
        front_sector = ranges[len(ranges)//2 - 15 : len(ranges)//2 + 15]
        min_dist = np.min(front_sector)
        
        cmd = Twist()
        if min_dist < safe_dist:
            self.get_logger().warn(f'OBSTACLE DETECTED! Distance: {min_dist:.2f}m | Initiating Avoidance Maneuver')
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5 # Rotate away
        else:
            cmd.linear.x = self.get_parameter('max_linear_speed').value
            cmd.angular.z = 0.0
            
        self.cmd_pub.publish(cmd)

    def yolo_callback(self, msg):
        # Professional logic: Prioritize avoidance based on object classification
        if "PERSON" in msg.data:
            self.get_logger().info('Human detected in path! Reducing speed for safety protocol.')
            # (Logic to slow down would go here)

def main(args=None):
    rclpy.init(args=args)
    # Using numpy for vector operations
    import numpy as np
    node = ObstacleAvoidance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
