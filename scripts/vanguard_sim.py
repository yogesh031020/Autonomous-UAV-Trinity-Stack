import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from vanguard_interfaces.msg import HealthStatus, FailsafeAction
import time

class VanguardSim(Node):
    def __init__(self):
        super().__init__('vanguard_pro_sim')
        self.report_sub = self.create_subscription(HealthStatus, '/guardian/health_report', self.report_cb, 10)
        self.action_sub = self.create_subscription(FailsafeAction, '/guardian/action_request', self.action_cb, 10)
        
        self.batt_pub = self.create_publisher(BatteryState, '/ap/battery', 10)
        
        self.get_logger().info('VANGUARD PRO-Sim Engine Online: Testing IDL Pipelines...')
        self.run_mission_test()

    def report_cb(self, msg):
        # We can monitor the health report here to verify the brain is working
        pass

    def action_cb(self, msg):
        self.get_logger().info(f'>>> SYSTEM ACTION RECEIVED: {msg.action_code} | REASON: {msg.reason}')

    def run_mission_test(self):
        # 1. Simulate Normal Phase (Increased to 15 seconds for visual flight time)
        self.get_logger().info('--- STEP 1: NORMAL FLIGHT ---')
        self.pub_batt(12.4)
        time.sleep(15)

        # 2. Simulate Emergency Phase
        self.get_logger().info('--- STEP 2: CRITICAL BATTERY FAILURE ---')
        self.pub_batt(10.1)
        time.sleep(5)

    def pub_batt(self, v):
        msg = BatteryState()
        msg.voltage = v
        self.batt_pub.publish(msg)

def main():
    rclpy.init()
    sim = VanguardSim()
    sim.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
