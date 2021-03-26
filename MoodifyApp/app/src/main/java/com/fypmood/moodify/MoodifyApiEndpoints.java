package com.fypmood.moodify;

import com.fypmood.moodify.models.AnalyzePlaylistRequest;
import com.fypmood.moodify.models.GeneratePlaylistRequest;
import com.fypmood.moodify.models.IndexApiResponse;
import com.fypmood.moodify.models.StatisticsRequest;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface MoodifyApiEndpoints {

    @GET(" ")
    public Call<IndexApiResponse> getIndex();

    @POST("analyze")
    public Call<AnalyzePlaylistRequest> PlaylistAnalysis(@Body AnalyzePlaylistRequest apiRequest);

    @POST("generate")
    public Call<GeneratePlaylistRequest> GeneratePlaylist(@Body GeneratePlaylistRequest apiRequest);

    @POST("statistics")
    public Call<StatisticsRequest> MoodStatistics(@Body StatisticsRequest apiRequest);



}
