import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState, Imu
from std_msgs.msg import String
import sqlite3
import os
from datetime import datetime

class BlackBoxLogger(Node):
    """
    Senior Black Box Data Logger
    Maintains a persistent SQLite database for post-mission forensic analysis.
    Logs high-frequency telemetry and critical failure events.
    """
    def __init__(self):
        super().__init__('black_box_logger')
        
        # Path configuration
        self.db_path = os.path.join('/home/yogesh/project_aegis/logs', 'flight_telemetry.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Database Setup
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.setup_db()
        
        # Subscriptions
        self.battery_sub = self.create_subscription(BatteryState, '/ap/battery', self.log_battery, 10)
        self.health_sub = self.create_subscription(String, '/guardian/system_health', self.log_health, 10)
        self.imu_sub = self.create_subscription(Imu, '/px4/imu', self.log_imu, 10)
        self.failsafe_sub = self.create_subscription(String, '/guardian/failsafe_command', self.log_event, 10)
        
        self.get_logger().info(f'Black Box Logger [v2.0] Active: Saving to {self.db_path}')

    def setup_db(self):
        # Create tables for different telemetry types
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                topic TEXT,
                value TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

    def log_to_db(self, topic, value):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.cursor.execute('INSERT INTO telemetry (timestamp, topic, value) VALUES (?, ?, ?)',
                           (timestamp, topic, str(value)))
        self.conn.commit()

    def log_battery(self, msg):
        self.log_to_db('/ap/battery', f"V:{msg.voltage:.2f} | C:{msg.current:.2f}")

    def log_health(self, msg):
        self.log_to_db('/guardian/system_health', msg.data)

    def log_imu(self, msg):
        # Log high-frequency IMU data (simplified for db size)
        accel = f"acc:[{msg.linear_acceleration.x:.2f},{msg.linear_acceleration.y:.2f},{msg.linear_acceleration.z:.2f}]"
        self.log_to_db('/px4/imu', accel)

    def log_event(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.get_logger().warn(f'LOGGING CRITICAL EVENT: {msg.data}')
        self.cursor.execute('INSERT INTO events (timestamp, event_type, description) VALUES (?, ?, ?)',
                           (timestamp, "FAILSAFE_TRIGGER", msg.data))
        self.conn.commit()

def main(args=None):
    rclpy.init(args=args)
    node = BlackBoxLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
