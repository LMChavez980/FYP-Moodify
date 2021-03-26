package com.fypmood.moodify.models;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.Map;

public class GeneratePlaylistRequest extends MoodifyApiRequest {
    @SerializedName("mood_selected")
    @Expose
    String mood_selected;

    @SerializedName("data")
    @Expose
    Map<String, String> data;

    public GeneratePlaylistRequest(String userid, String auth, String mood) {
        super(userid, auth);
        mood_selected = mood;
    }

    public String getMood_selected() {
        return mood_selected;
    }

    public void setMood_selected(String mood_selected) {
        this.mood_selected = mood_selected;
    }

    public Map<String, String> getData() {
        return data;
    }

    public void setData(Map<String, String> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public String toString() {
        return "Response [error="+ err_code + ", "
                + "message=" + message + ", data" + data + "]";
    }
}
