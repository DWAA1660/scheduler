import motor.motor_asyncio, motor

global CLIENT
#CLIENT = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")
CLIENT = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://DWAA:Pinta123@schedulercluster.sfos0.mongodb.net/")
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]