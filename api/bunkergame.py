import os
import random
import json


class Bunker:
    directory:str = os.path.abspath(os.getcwd()) + "/api/cardFiles/"
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
    global bunkerCharacterId
    bunkerCharacterId += 1
    gender = "Мужчина" if random.random() <= 0.504 else "Женщина"
    age = AgeGenerator(14,99)

    profession_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    hobby_exp = AgeGenerator(1, round(age/3), decimalGeneration=True)

    profession =     str(Bunker("Profession")).capitalize()
    fear =           str(Bunker("Fear")).capitalize()
    hobby =          str(Bunker("Hobby")).capitalize()
    characteristic = str(Bunker("Characteristic")).capitalize()
    baggage =        str(Bunker("Baggage")).capitalize()
    personInfo =     str(Bunker("PersonInfo")).capitalize()

    if isJson:
        json_file_value = f'''
        {{
            "way": "{Bunker("Profession").directory}",
            "id": "{bunkerCharacterId}",
            "gender": "{gender}",
            "age": "{age}",
            "profession": "{profession}",
            "profession_exp": "{profession_exp}",
            "hobby": "{hobby}",
            "hobby_exp": "{hobby_exp}",
            "fear": "{fear}",
            "characteristic": "{characteristic}",
            "baggage": "{baggage}",
            "personInfo": {personInfo},

        }}
            '''
        return json.loads(json_file_value)
        

    else:
        return f"""
<html>
    <body>
    <ul>
        <li><p>Пол:             {gender},</p></li>
        <li><p>Возраст:         {age},</p></li>

        <li><p>Профессия:       {profession},</p></li>
        <li><p>Опыт работы:     {profession_exp} {letOrGod(profession_exp)},</p></li>

        <li><p>Хобби:           {hobby},</p></li>
        <li><p>Опыт хобби:      {hobby_exp} {letOrGod(hobby_exp)},</p></li>

        <li><p>Фобия:           {fear},</p></li>

        <li><p>Черта характера: {characteristic},</p></li>

        <li><p>Багаж:           {baggage},</p></li>

        <li><p>Доп. инфа:       {personInfo}.</p></li>

        <li><p>"id персонажа":  {bunkerCharacterId},</p></li>
	</ul>  
    <body>
        <body><h3>Создатель:</h3></body>
                <h4><a href="https://github.com/Trofem/">Trofem</a></h4> 
<html>

"""
    
