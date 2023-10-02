# Tool to Classify Japanese Text According to JLPT Level

## Project Description

This project is the ongoing development of my MSc Computing dissertation. It is the prototype of a web application that students can use to input Japanese text and then have its predicted Japanese Language Proficieny Test (JLPT) level returned.

After creating a mini-corpus of texts labelled according to JLPT level, I created some algorithms to pre-process the text for machine learning (a particular challenge in Japanese). With the resulting feature extracted for each text in my corpus, I trained a language classification model using the Multinomial Naïve Bayes algorithm. I was then able to conduct basic testing to see that in theory the classification model works, though it requires a much larger set of training data in order to increase its accuracy. As it is, the prototype is as a command line tool, but I intend to develop it into a web application.

## Project Aims

- To parse Japanese text and extract Chinese kanji characters, words and grammar points
- To cross reference those features with a database storing information about JLPT level of those features
- To train a classification model to recognise the distribution of features in a text of a given level
- To have the classification model predict the JLPT level of a text


## Technologies Used

- Programming Language: Python
- Frameworks and Libraries: Flask, SQLAlchemy, Numpy, ScikitLearn, SudachiPy, Selenium

## Project Structure

- `analysed_text.py` - Class containing methods to extract kanji, vocabulary and grammar from a given Japanese text.
- `corpus.py` - Script to analyse all texts according to the variables above.
- `JLPT_classifier.py` - Script that stores the classifier. Change test input here.
- `j-readability_web_driver.py` - A web driver to validate classifier results against results from website j-Readability


## Usage

Install requirements.txt and run a flask server. Then insert desired text into JLPT_classifier.py and run.

## License
Apache 2.0
