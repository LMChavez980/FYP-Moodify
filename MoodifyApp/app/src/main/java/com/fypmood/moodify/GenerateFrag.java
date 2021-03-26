package com.fypmood.moodify;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.fypmood.moodify.models.GeneratePlaylistRequest;

import java.io.IOException;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

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
                GeneratePlaylistAPI("angry");
            }
        });

        happyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                GeneratePlaylistAPI("happy");
            }
        });

        relaxedButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                GeneratePlaylistAPI("relaxed");
            }
        });

        sadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                GeneratePlaylistAPI("sad");
            }
        });

        return rootView;
    }

    public void GeneratePlaylistAPI(String mood){
        RetrofitClient retrofitClient = new RetrofitClient();

        MainActivity mainActivity = (MainActivity) getActivity();
        String user_id = mainActivity.mSharedPreferences.getString("USERID", "");
        String auth_token = mainActivity.mSharedPreferences.getString("TOKEN", "");

        MoodifyApiEndpoints service = retrofitClient.getRetrofit().create(MoodifyApiEndpoints.class);
        GeneratePlaylistRequest apiRequest = new GeneratePlaylistRequest(user_id, auth_token, mood);

        Call<GeneratePlaylistRequest> generatePlaylistCall = service.GeneratePlaylist(apiRequest);
        generatePlaylistCall.enqueue(new Callback<GeneratePlaylistRequest>() {
            @Override
            public void onResponse(@NonNull Call<GeneratePlaylistRequest> call, @NonNull Response<GeneratePlaylistRequest> response) {
                if(response.isSuccessful()){
                    System.out.println(response.body().getMessage()+"\n"+response.body().getData());
                    Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_LONG).show();
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
            public void onFailure(Call<GeneratePlaylistRequest> call, Throwable t) {
                System.out.println(t.toString());

            }
        });


    }

}
