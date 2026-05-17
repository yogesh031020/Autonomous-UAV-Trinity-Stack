import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from visualization_msgs.msg import Marker
from vanguard_interfaces.msg import HealthStatus, FailsafeAction
from std_msgs.msg import ColorRGBA
import math

class GuardianNode(Node):
    def __init__(self):
        super().__init__('guardian_node_viz')
        
        # State
        self.state = HealthStatus.STATE_NORMAL
        self.last_battery_v = 12.6
        self.current_dist = 0.0
        
        # Publishers
        self.health_pub = self.create_publisher(HealthStatus, '/guardian/health_report', 10)
        self.marker_pub = self.create_publisher(Marker, '/guardian/status_marker', 10)
        self.command_pub = self.create_publisher(FailsafeAction, '/guardian/action_request', 10)
        
        # Subscriptions
        self.create_subscription(BatteryState, '/ap/battery', self.battery_cb, 10)
        
        # 10Hz Loop
        self.create_timer(0.1, self.health_audit_loop)
        
        self.get_logger().info('VANGUARD Visualizer Online: Floating 3D HUD and Control Bridge Active.')

    def battery_cb(self, msg):
        self.last_battery_v = msg.voltage

    def health_audit_loop(self):
        # Decision Layer: Priority-Based State Machine
        prev_state = self.state

        if self.last_battery_v < 10.5:
            self.state = HealthStatus.STATE_FAILSAFE
        else:
            self.state = HealthStatus.STATE_NORMAL

        # Trigger Failsafe if state changed
        if self.state != prev_state:
            self.trigger_failsafe(prev_state)

        # Telemetry & Visuals
        self.publish_visual_marker()
        self.publish_report()

    def trigger_failsafe(self, old_state):
        cmd = FailsafeAction()
        if self.state == HealthStatus.STATE_FAILSAFE:
            cmd.action_code = FailsafeAction.ACTION_RTL
            cmd.reason = "CRITICAL_BATTERY_SHUTDOWN"
        else:
            cmd.action_code = FailsafeAction.ACTION_HOVER
            cmd.reason = "RECOVERY_TO_NORMAL"
        
        self.get_logger().warn(f"TRANSITION: {old_state} -> {self.state} | CAUSE: {cmd.reason}")
        self.command_pub.publish(cmd)

    def publish_report(self):
        report = HealthStatus()
        report.battery_voltage = self.last_battery_v
        report.gps_healthy = True
        report.vo_healthy = True
        report.sensor_divergence_dist = self.current_dist
        report.zenoh_link_active = True
        report.system_state = self.state
        self.health_pub.publish(report)

    def publish_visual_marker(self):
        marker = Marker()
        marker.header.frame_id = "base_link" # Attaches text to the drone
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.id = 0
        
        # Position label above the drone
        marker.pose.position.z = 1.0 
        marker.scale.z = 0.2 # Text size
        
        # Change appearance based on state
        if self.state == HealthStatus.STATE_FAILSAFE:
            marker.text = f"!!! FAILSAFE !!! [{self.last_battery_v:.1f}V]"
            marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0) # Red
        else:
            marker.text = f"SYSTEM: NORMAL [{self.last_battery_v:.1f}V]"
            marker.color = ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0) # Green

        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = GuardianNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
