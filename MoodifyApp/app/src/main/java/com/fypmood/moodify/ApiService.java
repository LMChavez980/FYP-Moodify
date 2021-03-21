package com.fypmood.moodify;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;

public interface ApiService {

    @GET(" ")
    public Call<IndexApiResponse> getIndex();

    @POST("analyze")
    public Call<AnalyzeApiResponse> PlaylistAnalysis(@Body AnalyzeApiResponse apiRequest);

}
