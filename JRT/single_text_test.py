# This is a test for analysing an individual text.

from analysed_text import AnalysedText
from corpus import N4a

text = AnalysedText(N4a)

# Either run the functions separately or run the full analysis:

# text.get_kanji_info()
# text.get_word_info()
# text.get_grammar_info()

text.full_analysis()









