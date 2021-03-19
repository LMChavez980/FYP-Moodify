package com.fypmood.moodify;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.spotify.android.appremote.api.SpotifyAppRemote;

import kaaes.spotify.webapi.android.SpotifyApi;

public class MainActivity extends AppCompatActivity {
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.moodify://callback";
    private static final int REQUEST_CODE = 1337;
    private SpotifyAppRemote mSpotifyAppRemote;
    SharedPreferences mSharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mSharedPreferences = getSharedPreferences("SPOTIFY", 0);

        String auth_token = mSharedPreferences.getString("TOKEN", "");
        String id = mSharedPreferences.getString("USERID", "");

        Log.i("MAIN", "Token: ".concat(auth_token));
        Log.i("MAIN", "User ID: ".concat(id));

        BottomNavigationView bottomNav = findViewById(R.id.bottomNav);
        bottomNav.setOnNavigationItemSelectedListener(navListener);

        // Set Default fragment
        getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,
                new GenerateFrag()).commit();

        /*Button toGen = findViewById(R.id.to_generate);
        Button toPool = findViewById(R.id.to_pool);
        Button toStats = findViewById(R.id.to_stats);

        toGen.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){

            }
        });

        toPool.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(v.getContext(), AddToPool.class);
                intent.putExtra("TOKEN", auth_token);
                startActivity(intent);
            }
        });

        toStats.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });*/


    }


    private BottomNavigationView.OnNavigationItemSelectedListener navListener =
            menuItem -> {
                Fragment selectedFragment = null;

                switch (menuItem.getItemId()) {
                    case R.id.nav_generate:
                        selectedFragment = new GenerateFrag();
                        getSupportActionBar().setTitle(R.string.select_mood_btn);
                        break;

                    case R.id.nav_add_to_pool:
                        selectedFragment = new AddToPoolFrag();
                        getSupportActionBar().setTitle(R.string.add_to_pool_btn);
                        break;

                    case R.id.nav_statistics:
                        selectedFragment = new StatisticsFrag();
                        getSupportActionBar().setTitle(R.string.mood_stats_btn);
                        break;
                }

                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,
                        selectedFragment).commit();

                return true;
            };
}
