from sudachipy import Dictionary, SplitMode
from readability import app, db
from readability.models import Kanji, Word, Grammar
from sqlalchemy.sql import exists, and_

class AnalysedText:
    def __init__(self, text):
        self.text = text
        self.feature_vector = []

        self.characters = [] # text split into individual characters
        self.kanji = []
        self.kanji_count = 0
        self.JLPT_kanji_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []} # found kanji in the text
        self.JLPT_kanji_ratio = {}

        self.words = [] # text split into individual words
        self.content_words = [] # content words (nouns, verbs, adjectives, adverbs) stored in their dictionary form
        self.word_count = 0
        self.JLPT_word_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []} # found words in the text
        self.JLPT_word_ratio = {}

        self.grammar = {1: [], 2: [], 3: [], 4: [], 5: []}  # grammar points currently in the database
        self.grammar_count = 0
        self.JLPT_grammar_dict = {1: [], 2: [], 3: [], 4: [], 5: []} # found grammar points in the text
        self.JLPT_grammar_ratio = {}

#region start GENERAL
    
    # To check whether the value (kanji, word or grammar point) has already been extracted from the text and saved in a dictionary, to avoid duplicates and unnecessary database queries
    def already_in_dict(self, dict:dict, variable):
        if any(variable in value for value in dict.values()):
            return True
    
    # To print out extracted values according to their JLPT level
    def get_dict(self, dict:dict, variable:str):
        for x, y in dict.items():
            print(f"N{x} {variable}:\n{y}\n")
    
    # To calculate the ratio of values according to JLPT level
    def calc_ratio(self, dict:dict, total_count:int):
        ratio_dict = {}
        for level, values in dict.items():
            values_in_level = len(values)
            if values_in_level > 0: # edge case for if there are no values for a particular JLPT level
                percentage_ratio = (values_in_level / total_count) * 100
                ratio_dict[level] = percentage_ratio
            else:
                ratio_dict[level] = 0
        return ratio_dict
    
    # To print out extracted values according to their JLPT level
    def get_ratio(self,dict:dict, variable:str):
        for level, ratio in dict.items():
            print(f"N{level} {variable}: {ratio:.0f}%")

    def set_feature_vector(self, dict:dict):
        for key, ratio in dict.items():
            if ratio:
                self.feature_vector.append(ratio)
            else:
                self.feature_vector.append(0)

    # To run all three analysis functions at once
    def full_analysis(self):
        self.get_kanji_info()
        self.get_word_info()
        self.get_grammar_info()
        print(f"\n\nThe feature vector for this text is 18 values, 6 for kanji, 6 for words, 6 for grammar points: \n\n Length: {len(self.feature_vector)}\n\n{self.feature_vector}")

#endregion GENERAL 

#region start KANJI analysis 
    
    # This function checks whether a character is a kanji character, as opposed to hiragana or katakana. Adapted from https://www.darrenlester.com/blog/recognising-japanese-characters-with-javascript from javascript into python, 19th July 2023
    def is_kanji(self, character):
        if ('\u4e00' <= character <= '\u9faf') or ('\u3400' <= character <= '\u4dbf'):
            self.kanji.append(character)
            return True

    # This function takes an extracted kanji from the text, and queries the database for it to pull its JLPT level. Adapted from https://stackoverflow.com/questions/7646173/sqlalchemy-exists-for-query, accessed 20th July 2023
    def __db_kanji_search(self, kanji):
        with app.app_context(): 
            if db.session.query(exists().where(Kanji.kanji == kanji)).scalar(): # Check if the kanji is in the database
                jlpt_level = db.session.query(Kanji.jlpt_level).filter_by(kanji=kanji).first()[0] # accessing the JLPT level of found kanji in the database
                self.JLPT_kanji_dict[jlpt_level].append(kanji) # Add to the dictionary of JLPT levels and extracted kanji
                print(f'{kanji} = an N{jlpt_level} kanji')
            else:
                self.JLPT_kanji_dict[0].append(kanji) # If the kanji is not in the database, add it to the unknown category 0
                print(f'{kanji} is a kanji character but not found in the database')
    
    def __set_kanji_ratio(self): # Calculate the ratio of kanji from each JLPT level in the text
        self.JLPT_kanji_ratio = self.calc_ratio(self.JLPT_kanji_dict, self.kanji_count)
        
    def kanji_analysis(self):
        for character in self.text: # Loop through each character in the text
            self.characters.append(character) # Save each character to a list
            if self.is_kanji(character): # Check if the character is a kanji
                kanji = character 
                if self.already_in_dict(self.JLPT_kanji_dict, kanji): # Check we haven't already extracted that same kanji from the text
                    print(f'{kanji} is a kanji character and has already been extracted from the text')
                    continue 
                else:
                    self.__db_kanji_search(kanji) # Query the database for the kanji
                    self.kanji_count += 1 
            else:
                print(f'{character} is not a kanji character')
                continue
        self.__set_kanji_ratio() # Calculate the ratio of kanji in each JLPT level
        self.set_feature_vector(self.JLPT_kanji_ratio) # Set the feature vector for kanji

    def get_kanji_info(self):
        print("Starting kanji analysis:\n")
        self.kanji_analysis()
        print(f"\nHere is the original text: \n\n{self.text}")
        print(f"\nHere is the text divided into individual characters: \n\n{self.characters}")
        print(f"\nHere are the extracted kanji: \n\n{self.kanji}\n\n")
        print (f"\nThere {self.kanji_count} unique kanji in the text (no repeats). Here they are organised into their JLPT levels, with 0 as unknown or not in the JLPT scope:\n\n")  # printing out JLPT: kanji dictionary for clarity
        self.get_dict(self.JLPT_kanji_dict, "kanji")
        self.get_ratio(self.JLPT_kanji_ratio, "kanji")
        print(f"\n\nThe kanji feature vector for this text : \n\n {self.JLPT_kanji_ratio}")

#endregion KANJI analysis

#region start WORD analysis

    def split_words(self):
        tokenizer = Dictionary().create()
        words = tokenizer.tokenize(self.text, SplitMode.C)
        self.words = words # Now the words are split into a list of SudachiPy Morpheme objects
    
    # A function that checks if a word is a content word (noun, verb, adjective or adverb) and saves it to a list.
    def is_content_word(self, word):

        pos_info = word.part_of_speech() # SudachiPy function that returns a 6 value tuple with part-of-speech information about a word
        if pos_info[0] in {"名詞", "動詞", "形容詞", "副詞"}: # If the first value of that tuple equates to noun, verb, adjective or adverb, the word is a content word
            self.content_words.append(word.dictionary_form()) # Add the word to self.content_words
            # print(f"{word.dictionary_form()} is a content word")
            return True
        else:
            # print(f"{word.dictionary_form()} is NOT a content word")
            return False

    def db_query(self, query:str, word):
        # Query the database to see if the word exists in the database, either in kanji form or pronunciation form. If it exists in the database, append the word to the JLPT word dictionary. Modified from https://stackoverflow.com/questions/7646173/sqlalchemy-exists-for-query 20th July 2023
        if query == 'kanji':
            condition = Word.kanji == word.dictionary_form() # Checking the db for the word for its kanji form, e.g. 見る miru

            query = db.session.query(
                    exists().where(
                        (
                            condition
                        )
                    )
                )

            if query.scalar():
                jlpt_level = db.session.query(Word.jlpt_level).filter_by(kanji=word.dictionary_form()).first()[0]# Pull the JLPT level of the word from the database
                # print(f'kanji form for {word.surface()}was searched but pronunciation not searched')    
                return jlpt_level        
            return None
            
        elif query == 'pronunciation':
            condition = Word.pronunciation == word.reading_form() # Checking the db word for its pronunication form spelled out in katakana　e.g. ミル miru

            for level in range(5, 0, -1): # The database will be queried 5 times, searching the table for a word with the filter of JLPT level
                query = db.session.query(
                        exists().where(
                            and_(
                                condition,
                                Word.jlpt_level == level
                            )
                        )
                    )

                if query.scalar():
                    # print(f'Database searched twice for {word}')    
                    return level # Pulling the JLPT level of the matched word from the database
            return None

    # This function queries the database for a word and saves information about its JLPT level. 
    def __db_word_search(self, word):
        with app.app_context(): 

            kanji_result = self.db_query('kanji', word)
            pronunciation_result = self.db_query('pronunciation', word)

            if kanji_result is not None: # If the kanji form of the word is in the database, save it to the JLPT word dictionary
                jlpt_level = kanji_result # JLPT level is pulled from the database
                self.JLPT_word_dict[jlpt_level].append(word.dictionary_form()) 
                print(f'{word.dictionary_form()} = N{jlpt_level} word')

            elif pronunciation_result is not None: # Else if the pronunciation form of the word is in the database, save it to the JLPT word dictionary
                jlpt_level = pronunciation_result
                self.JLPT_word_dict[jlpt_level].append(word.dictionary_form())
                print(f'{word.dictionary_form()} = N{jlpt_level} word')

            # If the word is not in the database, add it to the unknown category 0
            else:
                self.JLPT_word_dict[0].append(word.dictionary_form())
                print(f'{word.dictionary_form()} not found in the database')
        
    def word_analysis(self):
        self.split_words()
        for word in self.words:
            if word.surface().isnumeric(): # Skip the word if it is a number
                print(f'{word} is a number')
                continue
            else:
                word_dict_form = word.dictionary_form() # SudachiPy function to get the dictionary form of a word
                if self.already_in_dict(self.JLPT_word_dict, word_dict_form): # Check we haven't already extracted that same word from the text
                    print(f'{word_dict_form} has already been extracted from the text')
                    continue
                else:
                    if self.is_content_word(word):
                        self.__db_word_search(word) # Query the database for the word in its dictionary form and save word into JLPT word dictionary (0 for unknown)         
                    else:
                        continue # To the next word in the list
                word = word.surface()
        self.word_count = len(self.content_words)
        self.JLPT_word_ratio = self.calc_ratio(self.JLPT_word_dict, self.word_count) # Calculate the ratio of words from JLPT level in the text
        self.set_feature_vector(self.JLPT_word_ratio) # Set the feature vector for words


    def get_word_info(self):
        print("\nStarting word analysis:\n")
        self.word_analysis()
        print(f"\nHere is the original text: \n\n {self.text}")
        print(f"\n\nHere is the text divided into words using SudachiPy: \n\n {self.words}")
        print(f"\n\nFrom that, we discard particles and punctuation, and convert the remaining content words into their dictionary form: \n\n {self.content_words}\n\n")
        print (f"\nThere {self.word_count} unique content words in the text (no repeats). Here they are organised into their JLPT levels, with 0 as unknown or not in the JLPT scope:\n\n")
        self.get_dict(self.JLPT_word_dict, "words")
        self.get_ratio(self.JLPT_word_ratio, "words")
        print(f"\n\nThe word feature vector for this text : \n\n {self.JLPT_word_ratio}")


#endregion WORD
        
#region start GRAMMAR analysis

    # This function pulls all current known grammar points from the database and saves them in a dictionary with JLPT levels as keys. 
    def db_grammar_pull(self):
         with app.app_context(): 

            # Query the database for grammar points and corresponding JLPT levels
            db_grammar = db.session.query(Grammar.grammar_point, Grammar.jlpt_level).all()

            # Process the results and populate the dictionary
            for grammar_point, jlpt_level in db_grammar:
                self.grammar[jlpt_level].append(grammar_point)

    # This function iterates through the grammar dictionary pulled from the database and checks if any of the grammar points are in the text. If they are, they are saved to a new dictionary (also with JLPT levels as keys).
    def extract_grammar(self):  
        for level, values in self.grammar.items(): # self.grammar is the dictionary with grammar points pulled from the database
            for grammar_point in values:
                if grammar_point in self.text: # Checking if the grammar point is in the text
                    self.JLPT_grammar_dict[level].append(grammar_point) # If it is in the text, add it to the JLPT grammar dictionary
                    self.grammar_count += 1
                    print(f'{grammar_point} is N{level} grammar point')
                else:
                    continue
        
    def grammar_analysis(self):
        self.db_grammar_pull() # Pulling all the grammar points from the database
        self.extract_grammar() # Extracting matching grammar points (continuous strings) from the text
        self.JLPT_grammar_ratio = self.calc_ratio(self.JLPT_grammar_dict, self.grammar_count) # Calculate the ratio of grammar points by JLPT level in the text
        self.set_feature_vector(self.JLPT_grammar_ratio) # Set the feature vector for grammar

    def get_grammar_info(self):
      print("\nStarting grammar analysis:\n")
      self.grammar_analysis()
      print(f"\nHere is the original text: \n\n {self.text}")
      print (f"\nThere are {self.grammar_count} known grammar points in this text. Here they are organised into their JLPT levels, with 0 as unknown or not in the JLPT scope:\n\n")
      self.get_dict(self.JLPT_grammar_dict, "grammar")
      self.get_ratio(self.JLPT_grammar_ratio, "grammar")
      print(f"\n\nThe grammar feature vector for this text : \n\n {self.JLPT_grammar_ratio}")


#endregion GRAMMAR

