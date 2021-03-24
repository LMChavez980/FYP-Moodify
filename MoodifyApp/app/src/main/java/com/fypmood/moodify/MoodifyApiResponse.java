package com.fypmood.moodify;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.List;

import retrofit2.http.Query;

public class MoodifyApiResponse {
    @SerializedName("saved_tracks")
    @Expose
    String saved_tracks;
    @SerializedName("playlist_ids")
    @Expose
    List<String> pl_ids;
    @SerializedName("user_id")
    @Expose
    String user_id;
    @SerializedName("error")
    @Expose
    String err_code;
    @SerializedName("message")
    @Expose
    String message;
    @SerializedName("data")
    @Expose
    List<List<String>> data;

    public MoodifyApiResponse(String saved_tracks_status, ArrayList<String> playlist_ids, String userid){
        saved_tracks = saved_tracks_status;
        pl_ids = playlist_ids;
        user_id = userid;
    }

    public String getErr_code() {
        return err_code;
    }

    public void setErr_code(String err_code) {
        this.err_code = err_code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<List<String>> getData() {
        return data;
    }

    public void setData(List<List<String>> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public String toString() {
        return "Response [error="+ err_code + ", "
                + "message=" + message + ", data" + data + "]";
    }
}
