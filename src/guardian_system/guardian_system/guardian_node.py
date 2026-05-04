import rclpy
from rclpy.node import Node
from enum import Enum
from sensor_msgs.msg import BatteryState
from std_msgs.msg import String

class SystemState(Enum):
    NORMAL = 0
    WARNING = 1
    FAILSAFE = 2

class GuardianNode(Node):
    """
    Senior Autonomous Guardian Node
    Responsible for real-time health monitoring and autonomous failsafe triggering.
    Employs a multi-state machine to prevent catastrophic failure.
    """
    def __init__(self):
        super().__init__('guardian_node')
        
        # Parameters (Professional practice)
        self.declare_parameter('battery_warning_threshold', 11.1)
        self.declare_parameter('battery_critical_threshold', 10.5)
        
        # State Initialization
        self.state = SystemState.NORMAL
        self.last_battery_voltage = 12.6
        self.ekf_healthy = True
        
        # Subscriptions
        self.battery_sub = self.create_subscription(BatteryState, '/ap/battery', self.battery_callback, 10)
        self.ekf_sub = self.create_subscription(String, '/px4/ekf_status', self.ekf_callback, 10)
        
        # Publishers
        self.health_pub = self.create_publisher(String, '/guardian/system_health', 10)
        self.command_pub = self.create_publisher(String, '/guardian/failsafe_command', 10)
        
        # Monitoring Timer (10Hz)
        self.timer = self.create_timer(0.1, self.health_check_loop)
        
        self.get_logger().info('Guardian Node [v2.0] Initialized: Monitoring System Health...')

    def battery_callback(self, msg):
        self.last_battery_voltage = msg.voltage

    def ekf_callback(self, msg):
        if "ERROR" in msg.data:
            self.ekf_healthy = False
        else:
            self.ekf_healthy = True

    def health_check_loop(self):
        warn_v = self.get_parameter('battery_warning_threshold').value
        crit_v = self.get_parameter('battery_critical_threshold').value
        
        # State Machine Logic
        previous_state = self.state
        
        if self.last_battery_voltage < crit_v or not self.ekf_healthy:
            self.state = SystemState.FAILSAFE
        elif self.last_battery_voltage < warn_v:
            self.state = SystemState.WARNING
        else:
            self.state = SystemState.NORMAL
            
        # Action if state changed
        if self.state != previous_state:
            self.handle_state_transition(previous_state)
            
        # Continuous Health Heartbeat
        self.publish_health_heartbeat()

    def handle_state_transition(self, prev):
        msg = String()
        if self.state == SystemState.FAILSAFE:
            self.get_logger().error(f'!!! CRITICAL FAILURE !!! - Triggering Failsafe Action')
            msg.data = "ACTION: RETURN_TO_LAUNCH"
            self.command_pub.publish(msg)
        elif self.state == SystemState.WARNING:
            self.get_logger().warn(f'Low health detected: Switching to WARNING state')
            msg.data = "ACTION: HOVER_AND_WAIT"
            self.command_pub.publish(msg)
        elif self.state == SystemState.NORMAL and prev != SystemState.NORMAL:
            self.get_logger().info(f'System recovered: Back to NORMAL operations')

    def publish_health_heartbeat(self):
        msg = String()
        msg.data = f"STATUS: {self.state.name} | BATT: {self.last_battery_voltage:.2f}V | EKF: {'OK' if self.ekf_healthy else 'ERROR'}"
        self.health_pub.publish(msg)

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
