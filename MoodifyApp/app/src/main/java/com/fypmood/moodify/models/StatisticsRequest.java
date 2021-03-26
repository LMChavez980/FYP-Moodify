package com.fypmood.moodify.models;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.HashMap;
import java.util.Map;

public class StatisticsRequest extends MoodifyApiRequest {
    // Response headers
    @SerializedName("data")
    @Expose
    HashMap<String, Integer> data;

    public StatisticsRequest(String userid, String auth) {
        super(userid, auth);
    }

    public HashMap<String, Integer> getData() {
        return data;
    }

    public void setData(HashMap<String, Integer> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public String toString() {
        return "Response [error="+ err_code + ", "
                + "message=" + message + ", data" + data + "]";
    }
}
