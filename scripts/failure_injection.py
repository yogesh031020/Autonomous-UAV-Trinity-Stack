import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from std_msgs.msg import String
import sys
import time

class FailureInjector(Node):
    """
    Failure Injection CLI
    A tool to simulate hardware/software failures for testing autonomy resilience.
    """
    def __init__(self):
        super().__init__('failure_injector')
        self.batt_pub = self.create_publisher(BatteryState, '/ap/battery', 10)
        self.ekf_pub = self.create_publisher(String, '/px4/ekf_status', 10)
        self.get_logger().info('Failure Injection CLI [Ready]')

    def inject_battery_failure(self, voltage):
        msg = BatteryState()
        msg.voltage = float(voltage)
        self.get_logger().warn(f'Injecting BATTERY FAILURE: {voltage}V')
        self.batt_pub.publish(msg)

    def inject_ekf_failure(self):
        msg = String()
        msg.data = "ERROR: HIGH_VARIANCE_DRIFT"
        self.get_logger().error('Injecting EKF FAILURE: High Variance')
        self.ekf_pub.publish(msg)

def main():
    rclpy.init()
    injector = FailureInjector()
    
    if len(sys.argv) < 2:
        print("Usage: python3 failure_injection.py [battery <val> | ekf]")
        return

    command = sys.argv[1]
    
    if command == "battery":
        val = sys.argv[2] if len(sys.argv) > 2 else 10.0
        injector.inject_battery_failure(val)
    elif command == "ekf":
        injector.inject_ekf_failure()
    else:
        print("Unknown command")

    # Give time for publication
    time.sleep(1)
    injector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
