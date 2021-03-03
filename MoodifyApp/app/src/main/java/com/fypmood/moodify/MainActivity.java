package com.fypmood.moodify;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.util.Log;

import com.spotify.android.appremote.api.ConnectionParams;
import com.spotify.android.appremote.api.Connector;
import com.spotify.android.appremote.api.SpotifyAppRemote;

import com.spotify.protocol.types.Track;

import java.util.List;

import kaaes.spotify.webapi.android.SpotifyApi;
import kaaes.spotify.webapi.android.SpotifyService;
import kaaes.spotify.webapi.android.models.Pager;
import kaaes.spotify.webapi.android.models.PlaylistSimple;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class MainActivity extends AppCompatActivity {
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.moodify://callback";
    private static final int REQUEST_CODE = 1337;
    private SpotifyAppRemote mSpotifyAppRemote;


    private RecyclerView mExPlaylistRecyclerView;
    private ExPlaylistRecyclerAdapter mExPlaylistAdapter;
    private SpotifyApi api = new SpotifyApi();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String token = getIntent().getStringExtra("TOKEN");
        api.setAccessToken(token);

        mExPlaylistRecyclerView = findViewById(R.id.playlistRecyclerView);
        mExPlaylistRecyclerView.setLayoutManager(new LinearLayoutManager(this));

        SpotifyService spotify = api.getService();

        spotify.getMyPlaylists(new Callback<Pager<PlaylistSimple>>() {
            @Override
            public void success(Pager<PlaylistSimple> playlistSimplePager, Response response) {
                List<PlaylistSimple> myPlaylists = playlistSimplePager.items;
                Log.i("MainActivity", "My playlists allocated");
                mExPlaylistAdapter = new ExPlaylistRecyclerAdapter(MainActivity.this, myPlaylists);
                mExPlaylistRecyclerView.setAdapter(mExPlaylistAdapter);

                mExPlaylistAdapter.addActionCallback(new ExPlaylistRecyclerAdapter.ActionCallback() {
                    @Override
                    public void onClickListener(PlaylistSimple playlist) {
                        //Toast.makeText(MainActivity.this, playlist.id, Toast.LENGTH_LONG).show();
                        /*mSpotifyAppRemote.getPlayerApi().play("spotify:playlist:"+playlist.id);

                        mSpotifyAppRemote.getPlayerApi()
                                .subscribeToPlayerState()
                                .setEventCallback(playerState -> {
                                    final Track track = playerState.track;
                                    if (track != null) {
                                        Log.d("MainActivity", track.name + " by " + track.artist.name);
                                    }
                                });
                         */


                    }

                });
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("MainActivity", error.getMessage());
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
                Log.d("MainActivity", "Connected! WAHOO WAHOO!");
                //connected();
            }

            @Override
            public void onFailure(Throwable throwable) {
                Log.e("MainActivity", throwable.getMessage(), throwable);
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
                        Log.d("MainActivity", track.name + " by " + track.artist.name);
                    }
                });

    }

    @Override
    protected void onStop() {
        super.onStop();
        SpotifyAppRemote.disconnect(mSpotifyAppRemote);
    }


}