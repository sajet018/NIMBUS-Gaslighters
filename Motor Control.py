import requests

ESP_IP = "10.49.144.120"
SNAPSHOT_URL = f"http://{ESP_IP}/snapshot"
MOTORS_URL = f"http://{ESP_IP}/motors"

motor_session = requests.Session()

motor_state = {
    "thrust": 0,
    "yaw": 0.0,
    "vertical": 0
}

def compute_motor_values():
    thrust = motor_state["thrust"]
    yaw = motor_state["yaw"]
    vertical = motor_state["vertical"]

    left = int(thrust * (1.0 - max(0, yaw)))
    right = int(thrust * (1.0 - max(0, -yaw)))

    left = max(0, min(255, left))
    right = max(0, min(255, right))
    vertical = max(-255, min(255, vertical))

    return left, right, vertical

def send_motor_command():
    left, right, vertical = compute_motor_values()

    try:
        motor_session.get(
            f"{MOTORS_URL}? m1 = {left} & m2 = {right} & m3 = {vertical}",
            timeout = (1, 2)
        )
    except Exception as e:
        print("Motor error: ", e)