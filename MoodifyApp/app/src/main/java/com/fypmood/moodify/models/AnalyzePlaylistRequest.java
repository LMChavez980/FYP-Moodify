package com.fypmood.moodify.models;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class AnalyzePlaylistRequest extends MoodifyApiRequest {
    @SerializedName("saved_tracks")
    @Expose
    String saved_tracks;
    @SerializedName("playlist_ids")
    @Expose
    List<String> pl_ids;

    public AnalyzePlaylistRequest(String saved_tracks_status, ArrayList<String> playlist_ids, String userid, String auth)
    {
        super(userid, auth);
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

    public List<String> getPl_ids() {
        return pl_ids;
    }

    public void setPl_ids(List<String> pl_ids) {
        this.pl_ids = pl_ids;
    }

    @NonNull
    @Override
    public String toString() {
        return "Response [error="+ err_code + ", "
                + "message=" + message + "]";
    }
}
