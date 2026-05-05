import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import datetime
import os

class ChronosReportGenerator(Node):
    """
    Project CHRONOS: Mission Report Generator [v1.0]
    Compiles AI detections into a professional inspection report.
    """
    def __init__(self):
        super().__init__('report_generator')
        
        # Subscriptions
        self.defect_sub = self.create_subscription(String, '/chronos/defects', self.callback, 10)
        
        # Internal State
        self.findings = []
        self.report_path = "/tmp/CHRONOS_Mission_Report.txt"
        
        self.get_logger().info('CHRONOS Mission Reporter Active.')
        self.get_logger().info(f'Reports will be saved to: {self.report_path}')

    def callback(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {msg.data}"
        
        if entry not in self.findings:
            self.findings.append(entry)
            self.get_logger().info(f'RECORDED: {msg.data}')
            self.write_report()

    def write_report(self):
        """
        Writes the compiled findings to a file.
        In a real scenario, this would be a PDF or Database entry.
        """
        try:
            with open(self.report_path, "w") as f:
                f.write("=== PROJECT CHRONOS: INSPECTION SUMMARY ===\n")
                f.write(f"DATE: {datetime.date.today()}\n")
                f.write(f"TOTAL DEFECTS FOUND: {len(self.findings)}\n")
                f.write("-------------------------------------------\n")
                for item in self.findings:
                    f.write(item + "\n")
                f.write("-------------------------------------------\n")
                f.write("STATUS: MISSION IN PROGRESS\n")
        except Exception as e:
            self.get_logger().error(f'Failed to write report: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ChronosReportGenerator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
