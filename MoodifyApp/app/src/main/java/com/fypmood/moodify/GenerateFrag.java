package com.fypmood.moodify;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.icu.text.SymbolTable;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;

import com.fypmood.moodify.models.GeneratePlaylistRequest;

import java.io.IOException;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.fypmood.moodify.MainActivity.dialog;

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

        dialog = getGenerateLoadingDialog(mood);
        dialog.show();


        MainActivity mainActivity = (MainActivity) getActivity();
        String user_id = mainActivity.mSharedPreferences.getString("USERID", "");
        String auth_token = mainActivity.mSharedPreferences.getString("TOKEN", "");

        MoodifyApiEndpoints service = retrofitClient.getRetrofit().create(MoodifyApiEndpoints.class);
        GeneratePlaylistRequest apiRequest = new GeneratePlaylistRequest(user_id, auth_token, mood);

        Call<GeneratePlaylistRequest> generatePlaylistCall = service.GeneratePlaylist(apiRequest);
        generatePlaylistCall.enqueue(new Callback<GeneratePlaylistRequest>() {
            @Override
            public void onResponse(@NonNull Call<GeneratePlaylistRequest> call, @NonNull Response<GeneratePlaylistRequest> response) {
                dialog.dismiss(); // close spinner dialog
                if(response.isSuccessful()){
                    System.out.println(response.body().getMessage()+"\n"+response.body().getData());
                    String resp_msg = response.body().getMessage();
                    if(response.body().getData() != null) {
                        String new_pl_id = response.body().getData().get("new_playlist_id");
                        dialog = getGenerateResultDialog(resp_msg, new_pl_id, true);
                        dialog.show();
                    }
                    else{
                        System.out.println(response.body().getErr_code()+": "+response.body().getMessage());
                        resp_msg = response.body().getErr_code()+": "+response.body().getMessage();
                        dialog = getGenerateResultDialog(resp_msg, null, false);
                        dialog.show();
                    }
                }
                else
                {
                    try {
                        System.out.println(response.errorBody().string());
                        String resp_msg = response.body().getErr_code()+": "+response.body().getMessage();
                        dialog = getGenerateResultDialog(resp_msg, null, false);
                        dialog.show();

                    } catch (IOException e) {
                        e.printStackTrace();
                        dialog = getGenerateResultDialog("An Error Occured - Please Try Again", null, false);
                        dialog.show();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneratePlaylistRequest> call, Throwable t) {
                dialog.dismiss(); // close spinner dialog
                System.out.println(t.toString());
                dialog = getGenerateResultDialog("An Error Occured - Please Try Again", null, false);
                dialog.show();

            }
        });


    }

    // Alert dialog for loading spinner
    private AlertDialog getGenerateLoadingDialog(String chosen){
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View spinnerView = inflater.inflate(R.layout.loading_spinner, null);

        builder.setMessage("Generating "+chosen+" playlist....")
                .setView(spinnerView)
                .setTitle(R.string.app_name);

        return builder.create();
    }

    // Alert dialog for results from API call
    private AlertDialog getGenerateResultDialog(String message, String new_id, boolean success){
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());

        // If successful response prompt user to open new playlist on Spotify
        // Else inform user of failure
        if(success){
            builder.setMessage(message)
                    .setPositiveButton("Open Spotify", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.i("GEN", "Open Playlist Spotify");
                            if(checkSpotifyInstall()){
                                Intent openSpotApp = new Intent(Intent.ACTION_VIEW);
                                openSpotApp.setData(Uri.parse("spotify:playlist:"+new_id));
                                openSpotApp.putExtra(Intent.EXTRA_REFERRER,
                                        Uri.parse("android-app://" + getActivity().getPackageName()));
                                startActivity(openSpotApp);
                            }
                            else{
                                Log.i("GEN", "Spotify Not Installed");
                                Intent openSpotWeb = new Intent(Intent.ACTION_VIEW, Uri.parse("https://open.spotify.com/playlist/"+new_id));
                                startActivity(openSpotWeb);
                            }

                        }
                    })
                    .setNegativeButton("Close", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            System.out.println("Close");
                        }
                    })
                    .setTitle(R.string.app_name);


        }
        else{
            builder.setMessage(message)
                    .setNegativeButton("Close", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            System.out.println("Close");
                        }
                    })
                    .setTitle(R.string.app_name);
        }

        return builder.create();
    }

    // Function to check if Spotify is installed
    private boolean checkSpotifyInstall(){
        PackageManager pm = getActivity().getPackageManager();
        try {
            pm.getPackageInfo("com.spotify.music", 0);
            return true;
        } catch (PackageManager.NameNotFoundException e) {
            return false;
        }
    }

}
