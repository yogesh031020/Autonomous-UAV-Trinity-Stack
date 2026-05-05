import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String, Float32
from nav_msgs.msg import Odometry
import time

class ChronosNavigator(Node):
    """
    Project CHRONOS: Resilient Navigator Node [v1.0]
    Handles autonomous switching between GPS and SLAM for inspection missions.
    """
    def __init__(self):
        super().__init__('navigator_node')
        
        # Subscriptions
        self.gps_sub = self.create_subscription(NavSatFix, '/gps/data', self.gps_callback, 10)
        self.slam_sub = self.create_subscription(Odometry, '/slam/odom', self.slam_callback, 10)
        
        # Publishers
        self.state_pub = self.create_publisher(String, '/chronos/nav_state', 10)
        self.health_pub = self.create_publisher(Float32, '/chronos/gps_health', 10)
        
        # Internal State
        self.current_state = "GPS_NAVIGATION" # Default
        self.gps_health = 100.0
        
        self.timer = self.create_timer(1.0, self.monitor_nav_health)
        self.get_logger().info('CHRONOS Navigator initialized. Mode: GPS_NAVIGATION')

    def gps_callback(self, msg):
        # In simulation, we check for 'NaN' or high variance to detect dead zones
        if msg.position_covariance[0] > 1.0: # High uncertainty
            self.gps_health = 0.0
        else:
            self.gps_health = 100.0

    def slam_callback(self, msg):
        # Store SLAM odometry for fallback
        pass

    def monitor_nav_health(self):
        msg = String()
        health_msg = Float32()
        health_msg.data = self.gps_health
        self.health_pub.publish(health_msg)
        
        if self.gps_health < 20.0 and self.current_state == "GPS_NAVIGATION":
            self.current_state = "SLAM_FALLBACK"
            msg.data = "NAV_ALERT: GPS SIGNAL LOST | SWITCHING TO SLAM"
            self.get_logger().error(msg.data)
        elif self.gps_health >= 20.0 and self.current_state == "SLAM_FALLBACK":
            self.current_state = "GPS_NAVIGATION"
            msg.data = "NAV_INFO: GPS SIGNAL RECOVERED | SWITCHING TO GPS"
            self.get_logger().warn(msg.data)
        else:
            msg.data = f"STATUS: {self.current_state} | GPS: {self.gps_health}%"
            
        self.state_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ChronosNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
