# Tool to Classify Japanese Text According to JLPT Level

## Project Description

This project is the ongoing development of my MSc Computing dissertation. It is the prototype of a web application that students can use to input Japanese text and then have its predicted Japanese Language Proficieny Test (JLPT) level returned.

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
