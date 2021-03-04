import pandas as pd
import os
import joblib

bins = {"danceability": ['<= minimum', pd.Interval(0.0768, 0.384), pd.Interval(0.384, 0.506),
                         pd.Interval(0.506, 0.628), pd.Interval(0.628, 0.962), '> maximum'],
        "energy": ['<= minimum', pd.Interval(0.00302, 0.447), pd.Interval(0.447, 0.696),
                   pd.Interval(0.696, 0.879), pd.Interval(0.879, 0.999), '> maximum'],
        "loudness": ['<= minimum', pd.Interval(-34.317, -10.824), pd.Interval(-10.824, -7.541),
                     pd.Interval(-7.541, -5.296), pd.Interval(-5.296, -0.938), '> maximum'],
        "valence": ['<= minimum', pd.Interval(0.0314, 0.226), pd.Interval(0.226, 0.426),
                    pd.Interval(0.426, 0.664), pd.Interval(0.664, 0.982), '> maximum'],
        "tempo": ['<= minimum', pd.Interval(36.958000000000006, 99.387), pd.Interval(99.387, 119.737),
                  pd.Interval(119.737, 140.05), pd.Interval(140.05, 217.396), '> maximum']}


class MusicMood:
    def __init__(self):
        filepath = os.path.dirname(os.path.abspath(__file__))
        pipeline = os.path.join(filepath, "musicmood_bnb_pipeline.joblib")
        self.mood_clf = joblib.load(pipeline)

    def preprocess(self, feature, x):
        intervals = bins[feature]
        binned_feature = []
        for val in x:
            if val <= intervals[1].left:
                binned_feature.append(intervals[0])
            elif val > intervals[4].right:
                binned_feature.append(intervals[5])
            elif val <= intervals[1].right:
                binned_feature.append(str(intervals[1]))
            elif val <= intervals[2].right:
                binned_feature.append(str(intervals[2]))
            elif val <= intervals[3].right:
                binned_feature.append(str(intervals[3]))
            elif val <= intervals[4].right:
                binned_feature.append(str(intervals[4]))

        return binned_feature

    def mood(self, songs):
        songs = songs.T.to_dict().values()
        predictions = self.mood_clf.predict(songs)
        return predictions
