import requests
import json
import random

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

    def translateWithLangbly(self, text, targetlanguage):
        headers = {
            "Authorization": f"Bearer {self.langbly_key}"
        }
        payload = {
            "q": text,
            "target": targetlanguage,
            "source": "auto"
        }

        try:
            response = requests.post(self.langbly_url, json=payload, headers=headers, timeout=5)
            if response.status_code != 200:
                return None  # Return None so the translate() method moves to the fallback
            data = response.json()
            return data.get("translatedText")
        except requests.exceptions.RequestException:
            # This catches DNS errors, timeouts, and no internet
            print("Network error: Could not reach Langibly.")
            return None
        except Exception as e:
            # Catch-all to prevent uncaught exceptions from crashing the app
            print(f"Unexpected error contacting Langibly: {e}")
            return None

    def translateWithMyMemory(self,text,targetlanguage,sourceLanguage):
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            # MyMemory expects langpair as "source|target" (no spaces)
            "langpair": f"{sourceLanguage}|{targetlanguage}"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            response_data = data.get("responseData", {}) if isinstance(data, dict) else {}
            return response_data.get("translatedText")
        except requests.exceptions.RequestException:
            print("Network error: Could not reach MyMemory.")
            return None
        except Exception as e:
            print(f"Unexpected error contacting MyMemory: {e}")
            return None 

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
            # translateWithMyMemory expects (text, targetlanguage, sourceLanguage)
            return self.translateWithMyMemory(text, targetlanguage, sourceLanguage)

            







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

    def deletePhrase(self,original):
        if original in self.phrases:
            del self.phrases[original]
            self.savePhrases()
        else:
            print("Phrase not found.")
        
class Dictionary:
    def __init__(self,):
        self.cache = {}
        self.history = []

    def getDictionry(self,word):
        word = word.lower()

        if word in self.cache:
            return self.cache[word]
        
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        try:
            response = requests.get(url)

            if response.status_code != 200:
                return {
                    "word": word,
                    "definitions":"Not available",
                    "syllables":"Not available",
                    "pronounciation":"Not available",
                    "part_of_speech":"Not available"
                }

            
            data = response.json()
            entry = data[0]
            word = entry.get("word",word)
            pronounciation = entry.get("phonetic","Not available")
            definition = entry["meanings"][0]["definitions"][0]["definition"]
            part_of_speech = entry["meanings"][0]["partOfSpeech"]
            syllables = entry.get("syllables", {}).get("list","Not available")

            details = {
                "word" : word,
                "definition" : definition,
                "pronounciation" : pronounciation,
                "syllables":syllables,
                "part_of_speech": part_of_speech

            }
            self.cache[word] = details
            return details
        except:
            return{
                "word": word,
                "defiinition": "Error loading file.......",
                "pronounciation":"Not available",
                "syllables":"Not available",
                "part_of_speech":"Not availaable"

            }


        

       
class Quiz:
    def __init__(self,phrasebook,stats_file="quiz.stats.json"):
        self.phrasebook = phrasebook
        self.stats_file = stats_file
        self.stats = self.loadStats()  

    def loadStats(self):
        try:
            with open(self.stats_file, "r") as file :
                return json.load(file)
        except FileNotFoundError:
            return {"Correct" : 0, "Wrong" : 0}
        
    def saveStats(self):
        with open(self.stats_file, "w") as file:
            return json.dump(self.stats,file, indent=4)
        
    def takeQuiz(self):
        if not self.phrasebook.phrases:
            print("No phrases availble for quiz. Add some first.")
            return
        
        original, translation = random.choice(list(self.phrasebook.phrases.items()))

        print()
class Stats:
    def __init__(self):
        pass
class LanguageLearningApp:
    def __init__(self):
        pass



class LanguageLearningApp:
    def __init__(self):
        self.translator = Translator()
        self.phrasebook = Phrasebook()
        self.dictionary = Dictionary()
        # self.quiz = Quiz(self.phrasebook) # Uncomment when Quiz is ready

    def menu(self):
        print("\n Language Learning Assistant")
        print("1. Translate Text")
        print("2. Search Dictionary")
        print("3. View Phrasebook")
        return input("Choose an option: ")

    def run(self):
        while True:
            choice = self.menu()

            if choice == "1":
                text = input("Enter text to translate: ")
                target = input("Enter target language (e.g., French, Yoruba): ")
                result = self.translator.translate(text, target)
                print(f"\nResult: {result}")

            elif choice == "2":
                word = input("Enter word to look up: ")
                data = self.dictionary.getDictionry(word)
                print(f"\n--- {data['word'].upper()} ---")
                print(f"Definition: {data.get('definition', 'N/A')}")
                print(f"Part of Speech: {data['part_of_speech']}")

            elif choice == "3":
                self.phrasebook.viewPhrases()

# This starts the app
if __name__ == "__main__":
    app = LanguageLearningApp()
    app.run()




