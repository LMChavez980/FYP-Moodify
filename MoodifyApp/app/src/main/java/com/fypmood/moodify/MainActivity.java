package com.fypmood.moodify;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    SharedPreferences mSharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_main);

        mSharedPreferences = getSharedPreferences("SPOTIFY", 0);

        String auth_token = mSharedPreferences.getString("TOKEN", "");
        String id = mSharedPreferences.getString("USERID", "");

        Log.i("MAIN", "Token: ".concat(auth_token));
        Log.i("MAIN", "User ID: ".concat(id));

        Button toGen = findViewById(R.id.to_generate);
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
        });


    }

}
