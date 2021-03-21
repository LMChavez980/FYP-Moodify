package com.fypmood.moodify;

import android.app.IntentService;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AnalyzeIntentService extends IntentService {
    public static final String CHANNEL_ID = "ForegroundServiceChannel";

    public AnalyzeIntentService() {
        super("Playlist Analyze Service");
    }

    @Override
    protected void onHandleIntent(@Nullable Intent intent) {
        String input = intent.getStringExtra("inputExtra");
        createNotificationChannel();
        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this,
                0, notificationIntent, 0);

        Notification notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("Analyze Service")
                .setContentText(input)
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setContentIntent(pendingIntent)
                .build();

        startForeground(1, notification);

        callAPI(intent);
    }

    private void createNotificationChannel() {
        NotificationChannel serviceChannel = new NotificationChannel(
                CHANNEL_ID,
                "Foreground Service Channel",
                NotificationManager.IMPORTANCE_DEFAULT
        );

        NotificationManager manager = getSystemService(NotificationManager.class);
        manager.createNotificationChannel(serviceChannel);
    }

    public void callAPI(Intent intent){
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        httpClient.writeTimeout(5, TimeUnit.MINUTES);
        httpClient.readTimeout(5, TimeUnit.MINUTES);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.0.220:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .client(httpClient.build())
                .build();

        ApiService service = retrofit.create(ApiService.class);

        String save_tracks = intent.getStringExtra("saved_tracks");
        String user_id = intent.getStringExtra("user_id");
        ArrayList<String> pl_ids = intent.getStringArrayListExtra("pl_ids");
        AnalyzeApiResponse apiRequest = new AnalyzeApiResponse(save_tracks, pl_ids, user_id);

        Call<AnalyzeApiResponse> apiResponseCall  = service.PlaylistAnalysis(apiRequest);
        apiResponseCall.enqueue(new Callback<AnalyzeApiResponse>() {
            @Override
            public void onResponse(Call<AnalyzeApiResponse> call, Response<AnalyzeApiResponse> response) {
                if (response.isSuccessful()){
                    System.out.println("Response:"+response.body());
                }
                else
                {
                    System.out.println("Failed:"+response.errorBody());
                }

            }

            @Override
            public void onFailure(Call<AnalyzeApiResponse> call, Throwable t) {
                System.out.println("Error:"+t.toString());
            }
        });

    }
}
