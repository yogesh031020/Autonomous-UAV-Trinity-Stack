import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge

class ChronosCameraSim(Node):
    """
    Project CHRONOS: Camera Stream Simulator [v1.0]
    Simulates a high-definition camera feed of an industrial bridge girder.
    """
    def __init__(self):
        super().__init__('camera_simulator')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.publish_image) # 10Hz
        self.bridge = CvBridge()
        self.get_logger().info('CHRONOS Camera Simulator Active.')

    def publish_image(self):
        # Create a simple 640x480 gray image to simulate a concrete wall
        image = np.full((480, 640, 3), 128, dtype=np.uint8)
        
        # Convert and publish
        msg = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_link"
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ChronosCameraSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
