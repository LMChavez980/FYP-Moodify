package com.fypmood.moodify.models;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
    @SerializedName("auth_token")
    @Expose
    String auth_token;
    @SerializedName("mood_selected")
    @Expose
    String mood_selected;

    // Response headers
    @SerializedName("error")
    @Expose
    String err_code;
    @SerializedName("message")
    @Expose
    String message;
    @SerializedName("data")
    @Expose
    Map<String, Integer> data;

    // Constructor for Generate Playlists
    public MoodifyApiResponse(String userid, String auth, String mood){
        user_id = userid;
        auth_token = auth;
        mood_selected = mood;
    }

    // Constructor for Analyze Playlists
    public MoodifyApiResponse(String saved_tracks_status, ArrayList<String> playlist_ids, String userid, String auth){
        saved_tracks = saved_tracks_status;
        pl_ids = playlist_ids;
        user_id = userid;
        auth_token = auth;
    }

    public String getSaved_tracks() {
        return saved_tracks;
    }

    public void setSaved_tracks(String saved_tracks) {
        this.saved_tracks = saved_tracks;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public List<String> getPl_ids() {
        return pl_ids;
    }

    public void setPl_ids(List<String> pl_ids) {
        this.pl_ids = pl_ids;
    }

    public String getMood_selected() {
        return mood_selected;
    }

    public void setMood_selected(String mood_selected) {
        this.mood_selected = mood_selected;
    }

    public String getAuth_token() {
        return auth_token;
    }

    public void setAuth_token(String auth_token) {
        this.auth_token = auth_token;
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

    public Map<String, Integer> getData() {
        return data;
    }

    public void setData(Map<String, Integer> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public String toString() {
        return "Response [error="+ err_code + ", "
                + "message=" + message + ", data" + data + "]";
    }
}
