from sklearn.naive_bayes import MultinomialNB
import numpy as np
from corpus import N4_test, N5_test
from analysed_text import AnalysedText

# Script for classifier adapted from the example given at https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html. Accessed 6th September 2023

# Below are feature vectors for each training text. It contains 17 values, 6 each for kanji, 6 for word and 5 for grammar points. Each 6 represents the ratio of unknown kanji, N5 kanji, N4 kanji, etc.
x_train = np.array([
    [1.9704433497536946, 16.25615763546798, 6.896551724137931, 34.97536945812808, 25.615763546798032, 14.285714285714285, 14.792899408284024, 20.118343195266274, 25.443786982248522, 15.384615384615385, 14.201183431952662, 10.059171597633137, 0, 0, 20.0, 0, 80.0],  # Feature vector for training Text 1, an N1 text. N1.1 Lower Advanced 2.05
    [2.8735632183908044, 12.643678160919542, 6.321839080459771, 32.758620689655174, 27.586206896551722, 17.81609195402299, 11.16751269035533, 5.0761421319796955, 22.33502538071066, 23.85786802030457, 18.781725888324875, 18.781725888324875, 0, 11.76470588235294, 29.411764705882355, 5.88235294117647, 52.94117647058824],  # Feature vector for training Text 2, an N1 text # N1.2 Lower Advanced 2.39 
    [2.7777777777777777, 10.185185185185185, 7.4074074074074066, 37.96296296296296, 21.296296296296298, 20.37037037037037, 7.4074074074074066, 4.62962962962963, 17.59259259259259, 26.851851851851855, 20.37037037037037, 23.14814814814815, 0, 0, 28.57142857142857, 7.142857142857142, 64.28571428571429],  # Feature vector for training Text 3, an N2 text: # N2.1 Upper Intermediate 2.89
    [1.977401129943503, 18.07909604519774, 11.016949152542372, 32.48587570621469, 23.163841807909606, 13.27683615819209, 20.52505966587112, 11.694510739856803, 25.29832935560859, 20.763723150357997, 11.455847255369928, 10.26252983293556, 0, 0, 42.857142857142854, 0, 57.14285714285714], # Feature vector for training Text 4, an N2 text: # N2b Upper Intermediate 3.1
    [2.272727272727273, 4.545454545454546, 0, 29.545454545454547, 31.818181818181817, 31.818181818181817, 16.049382716049383, 1.2345679012345678, 9.876543209876543, 19.753086419753085, 25.925925925925924, 27.160493827160494, 0, 0, 0, 12.5, 87.5], # Feature vector for training Text 5, an N3 text: # N3.1 Lower Intermediate 3.88
    [2.1052631578947367, 6.315789473684211, 6.315789473684211, 30.526315789473685, 30.526315789473685, 24.210526315789473, 6.422018348623854, 1.834862385321101, 12.844036697247708, 31.19266055045872, 28.440366972477065, 19.26605504587156, 0, 8.333333333333332, 16.666666666666664, 16.666666666666664, 58.333333333333336], # Feature vector for training Text 6, an N3 text:Lower Intermediate j read 3.8
    [0, 3.7037037037037033, 9.25925925925926, 18.51851851851852, 40.74074074074074, 27.77777777777778, 18.571428571428573, 2.857142857142857, 20.0, 10.0, 20.0, 28.57142857142857, 0, 0, 20.0, 0, 80.0], # Feature vector for training Text 7, an N4 text: N4.1 Aidoru yametai (Upper elementary 4.93)
    [2.941176470588235, 8.823529411764707, 14.705882352941178, 8.823529411764707, 35.294117647058826, 29.411764705882355, 8.333333333333332, 4.166666666666666, 6.25, 12.5, 29.166666666666668, 39.58333333333333, 0, 0, 0, 0, 100.0], # Feature vector for training Text 8, an N4 text: N4.2 Kisetsu A2 (Upper elementary j read 5.37)
    [6.25, 0, 0, 0, 25.0, 68.75, 4.166666666666666, 2.083333333333333, 4.166666666666666, 10.416666666666668, 33.33333333333333, 45.83333333333333, 0, 0, 10.0, 10.0, 80.0], # Feature vector for training Text 9, an N5 text: N5.1 (j read 6.25 lower elementary)
    [0, 0, 0, 0, 10.0, 90.0, 9.090909090909092, 6.0606060606060606, 3.0303030303030303, 15.151515151515152, 18.181818181818183, 48.484848484848484, 0, 0, 0, 12.5, 87.5] # Feature vector for training Text 10, an N5 text: N5b lower elementary j read 6.59


])

y_train = ["N1", "N1", "N2", "N2", "N3", "N3", "N4", "N4", "N5", "N5"]  # Corresponding JLPT levels for each training text

# Instantiate an instance of the Multinomial Naive Bayes classifier
model = MultinomialNB()

# Fit the model on training data
model.fit(x_train, y_train)

text = AnalysedText(N5_test)
text.full_analysis()

N5_text_vector = text.feature_vector

# The above feature vector must be reshaped into a 2D array. Adapted from https://stackoverflow.com/questions/51150153/valueerror-expected-2d-array-got-1d-array-instead. Accesssed 9th September 2023
new_text_vector = np.array(N5_text_vector).reshape(1, -1)

# Testing: Predict JLPT levels for example text that should be N5
JLPT_level_prediction = model.predict(new_text_vector)

print(f"\n\nStarting classfier\n\nOriginal text:\n {N5_test}")
print("Predicted JLPT Level:", JLPT_level_prediction[0])
