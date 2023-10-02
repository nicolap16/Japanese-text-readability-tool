from readability import db
from sqlalchemy import Column, Integer, String

# Table to store kanji 
class Kanji(db.Model):
    __tablename__ = 'kanji'  

    kanji_id = Column(Integer, primary_key=True)
    kanji = Column(String(255))
    readings = Column(String(255), nullable=False)
    meanings = Column(String(255))
    jlpt_level = Column(Integer, nullable=False)

# Table to store words 
class Word(db.Model):
    __tablename__ = 'word'

    word_id = Column(Integer, primary_key=True)
    kanji = Column(String(255), nullable=True)
    pronunciation = Column(String(255), nullable=True)
    original_level = Column(String(255))
    POS1 = Column(String(255))
    POS_details = Column(String(255))
    word_origin = Column(String(255))
    jlpt_level = Column(Integer, nullable=False)

# Table to store grammar points 
class Grammar(db.Model):
    __tablename__ = 'grammar'  

    grammar_id = Column(Integer, primary_key=True)
    grammar_point = Column(String(255))
    jlpt_level = Column(Integer, nullable=False)

