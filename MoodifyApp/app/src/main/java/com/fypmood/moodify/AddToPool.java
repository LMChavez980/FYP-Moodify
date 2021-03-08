package com.fypmood.moodify;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.util.SparseBooleanArray;
import android.view.View;
import android.widget.Toast;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.spotify.android.appremote.api.ConnectionParams;
import com.spotify.android.appremote.api.Connector;
import com.spotify.android.appremote.api.SpotifyAppRemote;

import com.spotify.protocol.types.Track;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import kaaes.spotify.webapi.android.SpotifyApi;
import kaaes.spotify.webapi.android.SpotifyService;
import kaaes.spotify.webapi.android.models.Pager;
import kaaes.spotify.webapi.android.models.PlaylistSimple;
import kaaes.spotify.webapi.android.models.UserPrivate;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class AddToPool extends AppCompatActivity {
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.moodify://callback";
    private static final int REQUEST_CODE = 1337;
    private SpotifyAppRemote mSpotifyAppRemote;
    //private SharedPreferences mSharedPreferences;


    private RecyclerView mExPlaylistRecyclerView;
    private ExPlaylistRecyclerAdapter mExPlaylistAdapter;
    private SpotifyApi api = new SpotifyApi();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pool);

        String token = getIntent().getStringExtra("TOKEN");
        api.setAccessToken(token);

        mExPlaylistRecyclerView = findViewById(R.id.playlistRecyclerView);
        mExPlaylistRecyclerView.setLayoutManager(new LinearLayoutManager(this));

        SpotifyService spotify = api.getService();

        //UserPrivate currentUser = new UserPrivate();

        String playlist_name = "Test Create 0";
        String des = "";

        Map<String, Object> create_body = new HashMap<String, Object>();
        create_body.put("name", playlist_name);
        create_body.put("description", des);
        create_body.put("public", false);

        /*spotify.createPlaylist("lmchavez980", create_body, new Callback<Playlist>() {
            @Override
            public void success(Playlist playlist, Response response) {
                Log.i("ATP", "Yeet");
            }

            @Override
            public void failure(RetrofitError error) {
                Log.i("ATP", "Noppers");

            }
        });*/

        spotify.getMyPlaylists(new Callback<Pager<PlaylistSimple>>() {
            @Override
            public void success(Pager<PlaylistSimple> playlistSimplePager, Response response) {
                List<PlaylistSimple> myPlaylists = playlistSimplePager.items;
                Log.i("ATP", "My playlists allocated");
                mExPlaylistAdapter = new ExPlaylistRecyclerAdapter(AddToPool.this, myPlaylists);
                mExPlaylistRecyclerView.setAdapter(mExPlaylistAdapter);

                FloatingActionButton analyzeFab = findViewById(R.id.sendToAnalyze);
                analyzeFab.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        ArrayList<String> mPlaylistsIds = new ArrayList<String>();
                        int len = mExPlaylistAdapter.getItemCount();
                        List<PlaylistSimple> mPlaylists = mExPlaylistAdapter.getmPlaylistList();
                        SparseBooleanArray chosen = mExPlaylistAdapter.getCheckBoxState();
                        String id = "";
                        for(int i = 1; i < len; i++)
                        {
                            if(chosen.get(i))
                            {
                                id = mPlaylists.get(i).id;
                                mPlaylistsIds.add(id);
                            }
                        }
                        Toast.makeText(getApplicationContext(), mPlaylistsIds.toString(), Toast.LENGTH_LONG).show();
                    }
                });
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("ATP", error.getMessage());
            }
        });

    }

    @Override
    protected  void onStart() {
        super.onStart();

        ConnectionParams connectionParams =
                new ConnectionParams.Builder(CLIENT_ID)
                        .setRedirectUri(REDIRECT_URI)
                        .showAuthView(true)
                        .build();

        SpotifyAppRemote.connect(this, connectionParams, new Connector.ConnectionListener() {
            @Override
            public void onConnected(SpotifyAppRemote spotifyAppRemote) {
                mSpotifyAppRemote = spotifyAppRemote;
                Log.d("ATP", "Connected! WAHOO WAHOO!");
                //connected();
            }

            @Override
            public void onFailure(Throwable throwable) {
                Log.e("ATP", throwable.getMessage(), throwable);
            }
        });
    }


    private void connected() {
        mSpotifyAppRemote.getPlayerApi().play("spotify:playlist:3cejj3mmTgiLrvNCr5qz83");

        mSpotifyAppRemote.getPlayerApi()
                .subscribeToPlayerState()
                .setEventCallback(playerState -> {
                    final Track track = playerState.track;
                    if (track != null) {
                        Log.d("ATP", track.name + " by " + track.artist.name);
                    }
                });

    }

    @Override
    protected void onStop() {
        super.onStop();
        SpotifyAppRemote.disconnect(mSpotifyAppRemote);
    }


}