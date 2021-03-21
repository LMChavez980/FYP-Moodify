package com.fypmood.moodify;

import androidx.annotation.NonNull;

import com.fypmood.moodify.models.TestRes;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class IndexApiResponse {
    @SerializedName("error")
    @Expose
    String err_code;
    @SerializedName("message")
    @Expose
    String message;

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

    @NonNull
    @Override
    public String toString() {
        return "Index [error="+ err_code + ", "
                + "message=" + message + "]";
    }
}
