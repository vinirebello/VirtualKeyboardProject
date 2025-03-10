from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
import random
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connectionString = 'mongodb+srv://viniadmin:54321@cluster0.u7owh.mongodb.net/'
client = MongoClient(connectionString)
dbConnection = client['ProjectDB']

collectionUsers = dbConnection.get_collection("Users")
collectionCombinations = dbConnection.get_collection("Combinations")

user = {
    "nome":"Usuarioteste",
    "senha": [1,2,3,4,5]
}

# collectionUsers.insert_one(user)

@app.get("/getCombination")
async def randomCombination():
    total_combinations = collectionCombinations.count_documents({})
    
    if total_combinations == 0:
        raise HTTPException(status_code=404, detail="Nenhuma combinação encontrada no banco")

    random_index = random.randint(0, total_combinations - 1)
    combination = collectionCombinations.find().skip(random_index).limit(1)[0]

    return {"hash": combination["hash"], "combination": combination["combination"]}

@app.get("/getUserPassword")
async def getPassword():
    user = collectionUsers.find_one()

    userPassword = user["senha"]
    print(userPassword)

    return userPassword

@app.post("/passwordValidation")
def validar_senha(payload: dict):

    user_id = payload.get("_id")
    senha_digitada = payload.get("senha")

    user = collectionUsers.find_one({"id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    userPassword = user["senha"]

    if senha_digitada == userPassword:
        return {"success": True, "message": "Senha correta!"}
    
    
    nova_combinacao = randomCombination()
    return {"success": False, "message": "Senha incorreta!", "nova_combinacao": nova_combinacao}


# def generateCombinations():
#     combinationsList = []

#     while len(combinationsList) < 100:
#         numbers = list(range(10))
#         random.shuffle(numbers)

#         valid_combinations = []
#         i = 0

#         while i < len(numbers) - 1:
#             if abs(numbers[i] - numbers[i + 1]) > 1:  
#                 valid_combinations.append([numbers[i], numbers[i + 1]])
#                 i += 2 
#             else:
#                 random.shuffle(numbers)  
#                 valid_combinations = []  
#                 i = 0

#         if len(valid_combinations) == 5: 
#             combinationsList.append(valid_combinations)

#     return combinationsList

# print(generateCombinations())

# def insert_db(combination):
#     combination_str = str(combination) 
#     combination_hash = hashlib.sha256(combination_str.encode()).hexdigest()

#     combination_map = {
#         "hash": combination_hash,
#         "combination": combination
#     }
    
#     collectionCombinations.insert_one(combination_map)
    
# combinations = generateCombinations()

# for combination in combinations:
#     insert_db(combination)