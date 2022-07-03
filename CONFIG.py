import motor.motor_asyncio, motor

global CLIENT
CLIENT = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")