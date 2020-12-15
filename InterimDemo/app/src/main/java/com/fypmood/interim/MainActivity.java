package com.fypmood.interim;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;
import android.widget.Toolbar;

import com.fypmood.interim.models.Playlist;
import com.spotify.android.appremote.api.ConnectionParams;
import com.spotify.android.appremote.api.Connector;
import com.spotify.android.appremote.api.SpotifyAppRemote;

import com.spotify.protocol.client.Subscription;
import com.spotify.protocol.types.PlayerState;
import com.spotify.protocol.types.Track;
import com.spotify.sdk.android.auth.AuthorizationRequest;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.interim://callback";
    private static final int REQUEST_CODE = 1337;
    private SpotifyAppRemote mSpotifyAppRemote;


    private RecyclerView mExPlaylistRecyclerView;
    private ExPlaylistRecyclerAdapter mExPlaylistAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mExPlaylistRecyclerView = findViewById(R.id.playlistRecyclerView);

        mExPlaylistAdapter = new ExPlaylistRecyclerAdapter(this, new ArrayList< Playlist >());
        mExPlaylistRecyclerView.setAdapter(mExPlaylistAdapter);

        mExPlaylistRecyclerView.setLayoutManager(new LinearLayoutManager(this));

        mExPlaylistAdapter.addActionCallback(new ExPlaylistRecyclerAdapter.ActionCallback() {
            @Override
            public void onClickListener(Playlist playlist) {
                //Toast.makeText(MainActivity.this, playlist.getId(), Toast.LENGTH_LONG).show();
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