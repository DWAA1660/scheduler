import motor.motor_asyncio, motor, os
from dotenv import load_dotenv

load_dotenv()

global CLIENT
#CLIENT = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")
CSTR = os.environ.get("CLIENT")
print(CSTR)
CLIENT = motor.motor_asyncio.AsyncIOMotorClient(str(CSTR))
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]