from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
import random
import hashlib

app = FastAPI()

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

def generateCombinations():
    combinationsList = []

    while len(combinationsList) < 100:
        numbers = list(range(10))
        random.shuffle(numbers)

        valid_combinations = []
        i = 0

        while i < len(numbers) - 1:
            if abs(numbers[i] - numbers[i + 1]) > 1:  
                valid_combinations.append([numbers[i], numbers[i + 1]])
                i += 2 
            else:
                random.shuffle(numbers)  
                valid_combinations = []  
                i = 0

        if len(valid_combinations) == 5: 
            combinationsList.append(valid_combinations)

    return combinationsList

print(generateCombinations())

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

# print(colletionCombinations)

@app.get("/newCombination")
def randomCombination():
    total_combinations = collectionCombinations.count_documents({})
    
    if total_combinations == 0:
        raise HTTPException(status_code=404, detail="Nenhuma combinação encontrada no banco")

    random_index = random.randint(0, total_combinations - 1)
    combination = collectionCombinations.find().skip(random_index).limit(1)[0]

    return {"hash": combination["hash"], "combination": combination["combination"]}