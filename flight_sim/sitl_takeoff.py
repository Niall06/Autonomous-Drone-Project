

import asyncio
from mavsdk import System

async def run():
    drone = System()
    # Updated connection URL format for newer MAVSDK releases
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Drone Connected successfully!")
            break

    print("Arming motors...")
    await drone.action.arm()

    print("Taking off...")
    await drone.action.takeoff()

    await asyncio.sleep(8)

    print("Landing...")
    await drone.action.land()

if __name__ == "__main__":
    asyncio.run(run())