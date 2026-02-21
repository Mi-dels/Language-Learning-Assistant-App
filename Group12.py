import requests
import json

class Translator:
    def __init__(self,):
        self.langbly_key = "294rNFCUhg7ttXGo7hGizT"
        self.langbly_url = "https://api.langibly.com/v1/translate"

    def getLangaugeCode(self,languageName):
        language = {
            "english":"en",
            "french":"fr",
            "portuguese":"pt",
            "spanish":"es",
            "german":"de",
            "italian":"it",
            "korean":"ko",
            "chinese":"zh",
            "russian":"ru",
            "japanese":"ja",
            "arabic":"ar",
            "yoruba":"yo",
            "igbo":"ig",
            "hausa":"ha"
        }
        languageName = languageName.lower()
        return language.get(languageName)

    def translateWithLangbly(self,text,targetlanguage):
        headers = {
            "Authorization": f"Bearer{self.langbly_key}"
        }
        payload = {
            "q" : text,
            "target" : targetlanguage,
            "source":"auto"
        }

        response = requests.post(self.langbly_url, json=payload, headers=headers)
        if response.status_code != 200:
            return "Transaction Failed"
        data = response.json()
        return data.get("translatedText")
    
    def translateWithMyMemory(self,text,targetlanguage,sourceLanguage):
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q" : text,
            "langpair" : f"{sourceLanguage} | {targetlanguage}"
        }

        response = requests.get(url,params= params)
        data = response.json()

    def translate(self,text,targetLanguageName):
        targetlanguage = self.getLangaugeCode(targetLanguageName)
        if not targetlanguage:
            return "Language Not Supported"
        result = self.translateWithLangbly(text,targetlanguage)
        if result:
            return result
        else:
            sourceName = input("Langbly failed. Enter first language")
            sourceLanguage = self.getLangaugeCode(sourceName)

            if not sourceLanguage:
                return "First Language Not Supported"
            return self.translateWithMyMemory(text,sourceLanguage,targetlanguage)

            







class Phrasebook:
    def __init__(self,filename="phrasebook.json"):
        self.filename = filename
        self.phrases = self.loadPhrases()

    def loadPhrases(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def savePhrases(self):
        with open(self.filename, "w") as file:
            json.dump(self.phrases,file,indent=4)

    def addPhrases(self,original,translation):
        self.phrases[original] = translation
        self.savePhrases()

    def viewPhrases(self):
        if not self.phrases:
            print("Your Phrasebook is Empty ")   
        else:
            print("\n Your Personal Phrasebook:")
            for original,translation in self.phrases.items():
                print(f"{original} = {translation}")

    def deletePhrase(self)
        
class Dictionary:
    def __init__(self):
        pass
class Quiz:
    def __init__(self):
        pass
class Stats:
    def __init__(self):
        pass
class LanguageLearningApp:
    def __init__(self):
        pass








