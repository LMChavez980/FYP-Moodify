package com.fypmood.moodify;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface ApiService {

    @GET(" ")
    public Call<IndexApiResponse> getIndex();

    @POST("analyze")
    public Call<MoodifyApiResponse> PlaylistAnalysis(@Body MoodifyApiResponse apiRequest);

    @POST("generate")
    public Call<MoodifyApiResponse> GeneratePlaylist(@Body MoodifyApiResponse apiRequest);



}
