import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math

class ZenithAvoidanceNode(Node):
    """
    Project Zenith: Advanced Potential Field Avoidance [v2.0]
    Final 100% Build: Integrates AI Vision + Goal-Seeking.
    """
    def __init__(self):
        super().__init__('obstacle_avoidance')
        
        # Subscriptions
        self.vision_sub = self.create_subscription(String, '/perception/yolo_detections', self.vision_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)
        
        # Internal State
        self.repulsive_force = [0.0, 0.0]
        self.attractive_force = [1.0, 0.0] # Move forward by default
        self.get_logger().info('Zenith Potential Field Navigator Active.')

    def vision_callback(self, msg):
        """
        Calculates Repulsive Forces based on AI detections.
        Example: 'DETECTED: Tree | DIST: 1.5m | POS: Left'
        """
        data = msg.data
        try:
            # Parse distance and position
            dist = float(data.split('DIST: ')[1].split('m')[0])
            pos = data.split('POS: ')[1]
            
            # Reset repulsive force
            self.repulsive_force = [0.0, 0.0]
            
            if dist < 3.0: # Danger Zone
                force_mag = 1.0 / (dist ** 2) # Inverse square law for safety
                
                if pos == "Center":
                    self.repulsive_force = [-force_mag, 0.0]
                elif pos == "Left":
                    self.repulsive_force = [0.0, -force_mag]
                elif pos == "Right":
                    self.repulsive_force = [0.0, force_mag]
                    
                self.get_logger().warn(f'AVOIDING: {data} | Repulsion: {self.repulsive_force}')
                self.calculate_movement()
        except Exception as e:
            self.get_logger().error(f'Parsing Error: {e}')

    def calculate_movement(self):
        """
        Sums forces: Result = Attractive (Goal) + Repulsive (Obstacle)
        """
        twist = Twist()
        
        # Combine forces
        linear_x = self.attractive_force[0] + self.repulsive_force[0]
        angular_z = self.repulsive_force[1]
        
        # Safety Clamping
        twist.linear.x = max(0.2, min(linear_x, 1.5))
        twist.angular.z = max(-1.0, min(angular_z, 1.0))
        
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ZenithAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
