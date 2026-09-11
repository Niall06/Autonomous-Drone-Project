import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

async def run():
    # 1. Initialize system object and open communication port
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    # 2. Monitor heartbeat stream until link is confirmed
    print("Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to PX4 SITL!")
            break

    # 3. Force-arm to bypass headless SITL sensor checks, then climb
    print("-- Force-arming vehicle...")
    await drone.action.arm_force()

    print("-- Taking off...")
    await drone.action.takeoff()
    # Allow 8 seconds to reach default hover altitude
    await asyncio.sleep(8)

    # 4. Offboard Handshake: Pre-stream a zero setpoint before starting
    print("-- Pre-streaming zero setpoint for handshake...")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )

    # 5. Engage Offboard Mode
    print("-- Starting Offboard mode...")
    try:
        await drone.offboard.start()
        print("-- Offboard mode active!")
    except OffboardError as error:
        print(f"Failed to enter offboard mode: {error._result.result}")
        await drone.action.land()
        return

    # 6. Stream yaw command at 20 Hz for 5 seconds (100 iterations)
    print("-- Streaming yaw rotation command (15 deg/s) for 5 seconds...")
    for _ in range(100):
        # VelocityBodyYawspeed(forward_m_s, right_m_s, down_m_s, yawspeed_deg_s)
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 15.0)
        )
        await asyncio.sleep(0.05)  # 20 Hz loop rate (50 ms)

    # 7. Neutralize setpoints, stop offboard, and land safely
    print("-- Stopping turn and neutralizing setpoints...")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )
    await asyncio.sleep(0.5)

    print("-- Stopping Offboard mode...")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Failed to stop offboard mode cleanly: {error._result.result}")

    print("-- Landing vehicle...")
    await drone.action.land()

if __name__ == "__main__":
    asyncio.run(run())