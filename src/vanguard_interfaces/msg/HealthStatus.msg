float32 battery_voltage
bool gps_healthy
bool vo_healthy
float32 sensor_divergence_dist
bool zenoh_link_active
uint8 system_state

# State constants
uint8 STATE_NORMAL = 0
uint8 STATE_WARNING = 1
uint8 STATE_FAILSAFE = 2
uint8 STATE_SENSOR_CONFLICT = 3
uint8 STATE_COMMS_LOST = 4
