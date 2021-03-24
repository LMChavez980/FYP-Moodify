package com.fypmood.moodify;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.fragment.app.Fragment;

import java.io.IOException;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class GenerateFrag extends Fragment {

    @Override
    public View onCreateView (LayoutInflater inflater, ViewGroup container,
                              Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.fragment_generate_grid, container, false);

        Button angryButton = rootView.findViewById(R.id.select_angry_btn);
        Button happyButton = rootView.findViewById(R.id.select_happy_btn);
        Button relaxedButton = rootView.findViewById(R.id.select_relaxed_btn);
        Button sadButton = rootView.findViewById(R.id.select_sad_btn);


        angryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                callAPI("angry");
            }
        });

        happyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                callAPI("happy");
            }
        });

        relaxedButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                callAPI("relaxed");
            }
        });

        sadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                callAPI("sad");
            }
        });

        return rootView;
    }

    public void callAPI(String mood){
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        httpClient.writeTimeout(5, TimeUnit.MINUTES);
        httpClient.readTimeout(5, TimeUnit.MINUTES);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.0.220:8000/api/v1/")
                .addConverterFactory(GsonConverterFactory.create())
                .client(httpClient.build())
                .build();

        MainActivity mainActivity = (MainActivity) getActivity();
        String user_id = mainActivity.mSharedPreferences.getString("USERID", "");
        String auth_token = mainActivity.mSharedPreferences.getString("TOKEN", "");

        ApiService service = retrofit.create(ApiService.class);
        MoodifyApiResponse apiRequest = new MoodifyApiResponse(user_id, auth_token, mood);

        Call<MoodifyApiResponse> apiResponseCall = service.GeneratePlaylist(apiRequest);
        apiResponseCall.enqueue(new Callback<MoodifyApiResponse>() {
            @Override
            public void onResponse(Call<MoodifyApiResponse> call, Response<MoodifyApiResponse> response) {
                if(response.isSuccessful()){
                    System.out.println(response.body().getMessage());
                }
                else
                {
                    try {
                        System.out.println(response.errorBody().string());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<MoodifyApiResponse> call, Throwable t) {
                System.out.println(t.toString());

            }
        });


    }

}
