import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# PX4 specific messages (The Industrial Standard)
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleStatus
from vanguard_interfaces.msg import FailsafeAction

class OffboardControl(Node):
    """
    VANGUARD Offboard Controller [Senior Edition]
    Responsible for high-level flight mode management and setpoint streaming.
    Directly interfaces with PX4 via Micro-XRCE-DDS.
    """
    def __init__(self):
        super().__init__('offboard_control_node')

        # 1. Setup Industrial QoS Profiles (Crucial for PX4)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # 2. PX4 Publishers
        self.offboard_ctrl_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.vehicle_cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos_profile)

        # 3. Guardian Subscriptions
        self.create_subscription(FailsafeAction, '/guardian/action_request', self.action_cb, 10)
        self.create_subscription(VehicleStatus, '/fmu/out/vehicle_status', self.status_cb, qos_profile)

        # 5. State Management & Counters
        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX
        self.armed = False
        self.emergency_mode = False
        self.offboard_setpoint_counter = 0

        # 6. Offboard Heartbeat Timer (20Hz - PX4 requires >2Hz)
        self.timer = self.create_timer(0.05, self.timer_callback)
        
        self.get_logger().info('VANGUARD Offboard Controller Initialized. Waiting for FMU Link...')

    def status_cb(self, msg):
        self.nav_state = msg.nav_state
        self.armed = msg.arming_state == VehicleStatus.ARMING_STATE_ARMED

    def action_cb(self, msg):
        """
        Reacts to the Guardian Node's Failsafe Requests
        """
        if msg.action_code == FailsafeAction.ACTION_RTL:
            self.get_logger().error(f"FAILSAFE TRIGGERED: {msg.reason} | Initiating Emergency RTL")
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_RETURN_TO_LAUNCH)
            self.emergency_mode = True
        elif msg.action_code == FailsafeAction.ACTION_LAND:
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)
            self.emergency_mode = True

    def timer_callback(self):
        # 1. Always publish OffboardControlMode (The Heartbeat)
        self.publish_offboard_control_mode()

        # 2. Check if we need to request Offboard mode and Arm
        if self.offboard_setpoint_counter < 11:
            self.offboard_setpoint_counter += 1
            if self.offboard_setpoint_counter == 10:
                # Command PX4 to switch to Offboard flight mode
                self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, param1=1.0, param2=6.0)
                # Command PX4 to Force-Arm motors (param2=21196.0 bypasses SITL preflight checks)
                self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, param1=1.0, param2=21196.0)
                self.get_logger().info("FMU Link Active: Switching to OFFBOARD Flight Mode & Force-Arming Motors...")

        # 3. Publish position target if not in emergency mode
        if not self.emergency_mode:
            # Fly to 5 meters altitude directly above home
            self.publish_trajectory_setpoint(0.0, 0.0, -5.0)
        
    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_ctrl_pub.publish(msg)

    def publish_trajectory_setpoint(self, x, y, z):
        msg = TrajectorySetpoint()
        msg.position = [x, y, z]
        msg.yaw = 0.0
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_pub.publish(msg)

    def publish_vehicle_command(self, command, **kwargs):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = kwargs.get("param1", float('nan'))
        msg.param2 = kwargs.get("param2", float('nan'))
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.vehicle_cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = OffboardControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
