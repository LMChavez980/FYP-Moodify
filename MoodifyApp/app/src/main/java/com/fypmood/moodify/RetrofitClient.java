package com.fypmood.moodify;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private OkHttpClient.Builder httpClient;
    private Retrofit retrofit;
    private String DEV_BASE_URL = "http://192.168.0.220:8000/api/v1/";
    private String PROD_BASE_URL = "http://64.227.44.241:8000/api/v1/";
    private int timeout_time = 5;

    public RetrofitClient(){
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        httpClient.writeTimeout(timeout_time, TimeUnit.MINUTES);
        httpClient.readTimeout(timeout_time, TimeUnit.MINUTES);

        retrofit = new Retrofit.Builder()
                .baseUrl(PROD_BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .client(httpClient.build())
                .build();
    }

    public Retrofit getRetrofit() {
        return retrofit;
    }

    public void setRetrofit(Retrofit retrofit) {
        this.retrofit = retrofit;
    }

    public OkHttpClient.Builder getHttpClient() {
        return httpClient;
    }

    public void setHttpClient(OkHttpClient.Builder httpClient) {
        this.httpClient = httpClient;
    }

    public int getTimeout_time() {
        return timeout_time;
    }

    public void setTimeout_time(int timeout_time) {
        this.timeout_time = timeout_time;
    }
}
