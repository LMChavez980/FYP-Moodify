package com.fypmood.moodify.models;

import androidx.annotation.NonNull;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.Map;

public abstract class MoodifyApiRequest {
    @SerializedName("user_id")
    @Expose
    String user_id;
    @SerializedName("auth_token")
    @Expose
    String auth_token;

    // Response headers
    @SerializedName("error")
    @Expose
    String err_code;
    @SerializedName("message")
    @Expose
    String message;

    public MoodifyApiRequest(String userid, String auth){
        user_id = userid;
        auth_token = auth;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
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
}
