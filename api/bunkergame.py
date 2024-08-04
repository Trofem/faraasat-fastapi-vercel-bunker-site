from jinja2 import Environment, FileSystemLoader
import os
import random
import json


HTMLdirectory = os.path.abspath(os.getcwd()) + "/html/"

jinja_env = Environment(loader=FileSystemLoader(HTMLdirectory))



bunker_building_template = jinja_env.get_template('bunkerBuilding.html')

bunker_character_template = jinja_env.get_template('bunkerCharacter.html')

class Bunker:
    directory:str = os.path.abspath(os.getcwd()) + "/api/cardFiles/" #way to text files
    parametreList:list[str]
    cardType:str #temporary value of created card type
    
    def __init__(self,card:str,count:int=1):
        cards_count:int = count #count of cards needed to generate
        cardType = card
        self.CreateBunkerCard(cardType, cards_count)

    def __str__(self) -> str:
        global cardType
        print(f"мы возращаем {self.cards_count}")
        print("empty string in file! " + self.cardType) if "" in self.parametreList else ...
        self.value:list[str] = random.sample(self.parametreList, self.cards_count)
        return ", ".join(self.value) if self.value != '[]' else "emptyString while random choice. Сообщите разработчику об ошибке"
    
    def CreateBunkerCard(self, Type:str,count=1) -> None:
        self.cards_count = count
        self.cardType = Type
        filepath:str = os.path.join(self.directory, f"Cards_{self.cardType}.txt")
        
        if os.path.exists(filepath):
            print(f"{self.cardType} Exist.\n")

            #в текстовых файлах не должно быть двойных кавычек, где либо, важно
            with open(filepath, "r") as file:
                self.parametreList = file.read().split("\n")
        else:
            print(f"{self.cardType} is not exist.")
            self.parametreList = ["Error (не смогли выдать карту (сообщите разработчику))"]


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

bunkerId = 0 #since starting site

def CreateRandomCharacter(isJson:bool=False) -> str:
    global bunkerId
    bunkerId += 1
    gender = "Мужчина" if random.random() <= 0.504 else "Женщина"
    age = AgeGenerator(14,99)

    profession_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    hobby_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    profession =     Bunker("Profession")
    fear =           Bunker("Fear")
    hobby =          Bunker("Hobby")
    characteristic = Bunker("Characteristic")
    baggage =        Bunker("Baggage")
    personInfo =     Bunker("PersonInfo")

    if isJson:
        json_file_value = f'''
        {{
            "id": {bunkerId},
            "gender": "{gender}",
            "age": {age},
            "profession": "{profession}",
            "profession_exp": {profession_exp},
            "hobby": "{hobby}",
            "hobby_exp": {hobby_exp},
            "fear": "{fear}",
            "characteristic": "{characteristic}",
            "baggage": "{baggage}",
            "personInfo": "{personInfo}"
        }}
        '''
        return json.loads(json_file_value)
        
    
    else:
        return bunker_character_template.render(
            bunkerId=bunkerId, gender=gender, age=age, profession=profession,
            profession_exp=profession_exp, hobby=hobby, hobby_exp=hobby_exp,
            fear=fear, characteristic=characteristic, baggage=baggage, personInfo=personInfo,
            letOrGod=letOrGod
            )

    
def CreateRandomBunker(isJson:bool=False) -> str:
    size = random.choice([space for space in range(100) if space % 10 == 0 and space > 20])
    #размер в кв. метров
    stocks = Bunker("Stock", 2)
    room_count = random.randint(2,3)
    rooms = Bunker("Rooms",room_count)

    if isJson:
        json_file_value = f"""{{ 
            "size": {size},
            "stocks": "{stocks}",
            "room_count": {room_count},
            "rooms": "{rooms}"
        }}"""
        
        return json.loads(json_file_value)
    else:
        return bunker_building_template.render(
            size=size, stocks=stocks, room_count=room_count, rooms=rooms)


#print( CreateRandomCharacter(isJson=False) )
#print( CreateRandomBunker(isJson=False) )

