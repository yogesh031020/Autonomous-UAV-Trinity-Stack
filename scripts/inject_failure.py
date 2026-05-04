import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
import time

class FailureInjector(Node):
    """
    Utility to simulate hardware failures for testing the Guardian Stack.
    """
    def __init__(self):
        super().__init__('failure_injector')
        self.publisher_ = self.create_publisher(BatteryState, '/ap/battery', 10)
        self.get_logger().info('Failure Injector ready. Press Ctrl+C to stop.')

    def inject_critical_battery(self):
        self.get_logger().warn('!!! INJECTING CRITICAL BATTERY FAILURE (9.0V) !!!')
        msg = BatteryState()
        msg.voltage = 9.0  # Well below failsafe threshold
        msg.percentage = 0.05
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    injector = FailureInjector()
    
    # Wait for the system to settle
    time.sleep(2)
    
    try:
        # Inject the failure
        injector.inject_critical_battery()
        time.sleep(1)
    except KeyboardInterrupt:
        pass
        
    injector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
