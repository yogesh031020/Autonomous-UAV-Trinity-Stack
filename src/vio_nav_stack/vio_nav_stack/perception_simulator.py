import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class PerceptionSimulator(Node):
    """
    Project Zenith: AI Perception Simulator [v1.0]
    Simulates YOLOv10 object detections for autonomous obstacle avoidance.
    """
    def __init__(self):
        super().__init__('perception_simulator')
        self.publisher_ = self.create_publisher(String, '/perception/yolo_detections', 10)
        self.timer = self.create_timer(1.0, self.publish_detection)
        self.get_logger().info('Zenith AI Perception Simulator Started...')

    def publish_detection(self):
        objects = ["Person", "Wall", "Tree", "Building", "Drone"]
        distances = [1.5, 3.2, 5.0, 10.0, 0.8]
        angles = ["Center", "Left", "Right"]
        
        obj = random.choice(objects)
        dist = random.choice(distances)
        ang = random.choice(angles)
        
        msg = String()
        msg.data = f"DETECTED: {obj} | DIST: {dist}m | POS: {ang}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Simulated Vision: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
