import os
import random
import json


class Bunker:
    directory:str = os.path.dirname(os.path.abspath(__file__) + "/cardFiles/")
    parametreList:list[str]
    cardType:str

    def CreateBunkerCards(self, Type:str) -> None:
        self.cardType = Type
        filepath:str = os.path.join(self.directory, f"Cards_{self.cardType}.txt")
        #print("\n"+filepath,end="... ")
        if os.path.exists(filepath):
            print(f"{self.cardType} Exist.\n")

            with open(filepath, "r") as file:
                self.parametreList = file.read().split("\n")
        else:
            print(f"{self.cardType} is not exist.")
            self.parametreList = ["Error"]
    
    def __init__(self,cardType:str):
        self.CreateBunkerCards(cardType)
    
    def __str__(self) -> str:
        print("empty string in file! " + self.cardType) if "" in self.parametreList else ...
        self.value = random.choice(self.parametreList)
        return self.value if self.value != '' else "emptyString while random choice. Сообщите разработчику об ошибке"

def letOrGod(year: int) -> str:
    if year == 1:
        return "год"
    elif 11 <= year <= 14 or year > 99:
        return "лет"
    else:
        last_digit = year % 10
        if last_digit == 1:
            return "год"
        elif last_digit in [2, 3, 4]:
            return "года"
        else:
            return "лет"
def AgeGenerator(firstAge:int=1, lastAge:int=99, decimalGeneration:bool=False) -> float:
    value = random.randint(firstAge,lastAge) #рандомное число в радиусе

    if decimalGeneration: #десятичное (и нуля)
        value -= random.choice([0.25,0.5,0.75,1]) if random.random() >= 0.5 else 0 #чуток уменьшаем

    return value

bunkerCharacterId = 0 #since starting site

def CreateRandomCharacter(isJson:bool=False) -> str:
    bunkerCharacterId += 1
    gender = "Мужчина" if random.random() <= 0.504 else "Женщина"
    age = AgeGenerator(14,99)

    profession_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    hobby_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    profession =     str(Bunker("Profession")).capitalize()
    fear =           str(Bunker("Fear")).capitalize()
    characteristic = str(Bunker("Characteristic")).capitalize()
    baggage =        str(Bunker("Baggage")).capitalize()
    personInfo =     str(Bunker("PersonInfo")).capitalize()
    hobby =          str(Bunker("Hobby")).capitalize()

    if isJson:
        ...
        filename = "content.json"
        json_file_value = f'''
        {{
            "id": "{bunkerCharacterId}",
            "gender": "{gender}",
            "age": "{age}",
            "profession": "{profession}",
            "fear": "{fear}"
        }}
            '''
        with open(filepath, "w") as file:
            # Write some text to the file
            json.dump(json_file_value,file)

    else:
        return f"""
""
Пол:             {gender},
Возраст:         {age},

Профессия:       {profession},
Опыт работы:     {profession_exp} {letOrGod(profession_exp)},

Хобби:           {hobby},
Опыт хобби:      {hobby_exp} {letOrGod(hobby_exp)},

Фобия:           {fear},

Черта характера: {characteristic},

Багаж:           {baggage},

Доп. инфа:       {personInfo}.

"id персонажа":  {bunkerCharacterId},

Создано Trofem (https://github.com/Trofem)
""
"""

def GetJsonValue():
    # Open the file in read mode
    with open(filepath, "r") as file:
        # Read the contents of the file
        fileValue = json.load(file)
    return fileValue
    
