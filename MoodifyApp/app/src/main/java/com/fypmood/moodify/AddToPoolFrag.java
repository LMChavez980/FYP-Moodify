package com.fypmood.moodify;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.util.SparseBooleanArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.ArrayList;
import java.util.List;

import kaaes.spotify.webapi.android.SpotifyApi;
import kaaes.spotify.webapi.android.SpotifyService;
import kaaes.spotify.webapi.android.models.Pager;
import kaaes.spotify.webapi.android.models.PlaylistSimple;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class AddToPoolFrag extends Fragment {

    private ExPlaylistRecyclerAdapter mExPlaylistAdapter;
    private SpotifyApi api = new SpotifyApi();

    public AddToPoolFrag(){}

    @Override
    public View onCreateView (LayoutInflater inflater, ViewGroup container,
                              Bundle savedInstanceState){

        View rootView = inflater.inflate(R.layout.fragment_pool, container, false);

        MainActivity mainActivity = (MainActivity) getActivity();

        String auth_token = mainActivity.mSharedPreferences.getString("TOKEN", "");

        RecyclerView mExPlaylistRecyclerView = rootView.findViewById(R.id.playlistRecyclerView);
        mExPlaylistRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        api.setAccessToken(auth_token);
        SpotifyService spotify = api.getService();

        spotify.getMyPlaylists(new Callback<Pager<PlaylistSimple>>() {
            @Override
            public void success(Pager<PlaylistSimple> playlistSimplePager, Response response) {
                List<PlaylistSimple> myPlaylists = playlistSimplePager.items;
                Log.i("ATP", "My playlists allocated");
                mExPlaylistAdapter = new ExPlaylistRecyclerAdapter(getContext(), myPlaylists);
                mExPlaylistRecyclerView.setAdapter(mExPlaylistAdapter);

                FloatingActionButton analyzeFab = rootView.findViewById(R.id.sendToAnalyze);
                analyzeFab.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        ArrayList<String> mPlaylistsIds = new ArrayList<String>();
                        int len = mExPlaylistAdapter.getItemCount();
                        List<PlaylistSimple> mPlaylists = mExPlaylistAdapter.getmPlaylistList();
                        SparseBooleanArray chosen = mExPlaylistAdapter.getCheckBoxState();
                        String id = "";
                        for(int i = 1; i < len; i++) {
                            if (chosen.get(i)) {
                                id = mPlaylists.get(i).id;
                                mPlaylistsIds.add(id);
                            }
                        }
                        Toast.makeText(getContext(), mPlaylistsIds.toString(), Toast.LENGTH_LONG).show();
                        Intent serviceIntent = new Intent(mainActivity, AnalyzePlaylistService.class);
                        if(chosen.get(0)){
                            serviceIntent.putExtra("saved_tracks", "1");
                        }
                        else
                        {
                            serviceIntent.putExtra("saved_tracks", "0");
                        }
                        serviceIntent.putStringArrayListExtra("pl_ids", mPlaylistsIds);
                        serviceIntent.putExtra("content", "Analyzing Your Playlists");
                        serviceIntent.putExtra("user_id", mainActivity.mSharedPreferences.getString("USERID", ""));
                        serviceIntent.putExtra("auth_token", mainActivity.mSharedPreferences.getString("TOKEN", ""));
                        mainActivity.startForegroundService(serviceIntent);
                        Toast.makeText(getContext(), "Service Started", Toast.LENGTH_LONG).show();
                        Log.i("ATP", "Service Started");
                    }

                });

            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("ATP", "Error:"+error.getMessage());
            }
        });

        return rootView;
    }

}
