package com.fypmood.moodify;

import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

public class AnalyzeService extends Service {
    public static final String CHANNEL_ID = "ForegroundServiceChannel";
    private int startAnalysisId = 1;
    private int endAnalysisId = 2;

    @Override
    public void onCreate(){
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startid) {
        String contentExtra = intent.getStringExtra("content");

        NotificationChannel serviceChannel = new NotificationChannel(
                CHANNEL_ID,
                "Analyze Foreground Service Channel",
                NotificationManager.IMPORTANCE_DEFAULT
        );

        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        manager.createNotificationChannel(serviceChannel);

        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this,
                0, notificationIntent, 0);


        Notification notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("Moodify Add To Pool")
                .setContentText(contentExtra)
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setContentIntent(pendingIntent)
                .build();

        startForeground(startAnalysisId, notification);

        callAPI(intent, manager);

        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public void callAPI(Intent intent, NotificationManager manager){
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        httpClient.writeTimeout(5, TimeUnit.MINUTES);
        httpClient.readTimeout(5, TimeUnit.MINUTES);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.0.220:8000/api/v1/")
                .addConverterFactory(GsonConverterFactory.create())
                .client(httpClient.build())
                .build();

        ApiService service = retrofit.create(ApiService.class);

        String save_tracks = intent.getStringExtra("saved_tracks");
        String user_id = intent.getStringExtra("user_id");
        String auth_token = intent.getStringExtra("auth_token");
        ArrayList<String> pl_ids = intent.getStringArrayListExtra("pl_ids");
        MoodifyApiResponse apiRequest = new MoodifyApiResponse(save_tracks, pl_ids, user_id, auth_token);

        Call<MoodifyApiResponse> apiResponseCall  = service.PlaylistAnalysis(apiRequest);
        apiResponseCall.enqueue(new Callback<MoodifyApiResponse>() {
            @Override
            public void onResponse(@NonNull Call<MoodifyApiResponse> call, @NonNull Response<MoodifyApiResponse> response) {
                Intent notificationIntent = new Intent(getApplicationContext(), MainActivity.class);
                PendingIntent pendingIntent = PendingIntent.getActivity(getApplicationContext(),
                        0, notificationIntent, 0);
                if (response.isSuccessful()){
                    System.out.println("Response: "+response.body());
                    Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                            .setContentTitle("Moodify Add To Pool")
                            .setContentText("Tracks Successfully added to pool")
                            .setSmallIcon(R.drawable.ic_launcher_foreground)
                            .setContentIntent(pendingIntent)
                            .build();
                    manager.notify(endAnalysisId, notification);
                }
                else
                {
                    System.out.println("Failed: "+response.errorBody());
                    Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                            .setContentTitle("Moodify Add To Pool")
                            .setContentText("An Error Occured - Please Try Again")
                            .setSmallIcon(R.drawable.ic_launcher_foreground)
                            .setContentIntent(pendingIntent)
                            .build();
                    manager.notify(endAnalysisId, notification);
                }

                stopForeground(true);

            }

            @Override
            public void onFailure(@NonNull Call<MoodifyApiResponse> call, @NonNull Throwable t) {
                System.out.println("Error:"+t.toString());
                Intent notificationIntent = new Intent(getApplicationContext(), MainActivity.class);
                PendingIntent pendingIntent = PendingIntent.getActivity(getApplicationContext(),
                        0, notificationIntent, 0);
                Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                        .setContentTitle("Moodify Add To Pool")
                        .setContentText("An Error Occured - Please Try Again")
                        .setSmallIcon(R.drawable.ic_launcher_foreground)
                        .setContentIntent(pendingIntent)
                        .build();
                manager.notify(endAnalysisId, notification);
                stopForeground(true);
            }
        });

    }

}
