package com.fypmood.moodify;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import com.fypmood.moodify.models.AnalyzePlaylistRequest;

import java.util.ArrayList;

import static com.fypmood.moodify.MainActivity.dialog;

public class AnalyzePlaylistService extends Service {
    public static final String CHANNEL_ID = "ForegroundServiceChannel";
    private int startAnalysisId = 1;
    private int endAnalysisId = 2;

    @Override
    public void onCreate(){
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startid) {
        Log.i("APS", "In service");

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

        AnalyzeAPI(intent, manager);

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

    public void AnalyzeAPI(Intent intent, NotificationManager manager){
        RetrofitClient retroFitClient = new RetrofitClient();

        MoodifyApiEndpoints service = retroFitClient.getRetrofit().create(MoodifyApiEndpoints.class);

        String save_tracks = intent.getStringExtra("saved_tracks");
        String user_id = intent.getStringExtra("user_id");
        String auth_token = intent.getStringExtra("auth_token");
        ArrayList<String> pl_ids = intent.getStringArrayListExtra("pl_ids");
        AnalyzePlaylistRequest apiRequest = new AnalyzePlaylistRequest(save_tracks, pl_ids, user_id, auth_token);

        Call<AnalyzePlaylistRequest> apiResponseCall  = service.PlaylistAnalysis(apiRequest);
        apiResponseCall.enqueue(new Callback<AnalyzePlaylistRequest>() {
            @Override
            public void onResponse(@NonNull Call<AnalyzePlaylistRequest> call, @NonNull Response<AnalyzePlaylistRequest> response) {
                Intent notificationIntent = new Intent(getApplicationContext(), MainActivity.class);
                PendingIntent pendingIntent = PendingIntent.getActivity(getApplicationContext(),
                        0, notificationIntent, 0);
                if (response.isSuccessful()){
                    Log.i("APS", "Sucessful Response");
                    System.out.println("Response: "+response.body());
                    Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                            .setContentTitle("Moodify Add To Pool")
                            .setContentText(response.body().getMessage())
                            .setSmallIcon(R.drawable.ic_launcher_foreground)
                            .setContentIntent(pendingIntent)
                            .build();
                    manager.notify(endAnalysisId, notification);
                    dialog.setMessage(response.body().getMessage());
                    if(!dialog.isShowing()){
                        dialog.show();
                    }
                }
                else
                {
                    Log.e("APS", "ERROR: Unsucessful Response");
                    System.out.println("Failed: "+response.errorBody());
                    Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                            .setContentTitle("Moodify Add To Pool")
                            .setContentText("There was an error in analysing process - Please try again")
                            .setSmallIcon(R.drawable.ic_launcher_foreground)
                            .setContentIntent(pendingIntent)
                            .build();
                    manager.notify(endAnalysisId, notification);
                    dialog.setMessage("ERROR: There was an error in analysing process - Please try again");
                    if(!dialog.isShowing()){
                        dialog.show();
                    }
                }

                Log.i("APS", "Stopping Service on success");
                stopForeground(true);

            }

            @Override
            public void onFailure(@NonNull Call<AnalyzePlaylistRequest> call, @NonNull Throwable t) {
                System.out.println("Error:"+t.toString());
                Intent notificationIntent = new Intent(getApplicationContext(), MainActivity.class);
                PendingIntent pendingIntent = PendingIntent.getActivity(getApplicationContext(),
                        0, notificationIntent, 0);
                Notification notification = new NotificationCompat.Builder(getApplicationContext(), CHANNEL_ID)
                        .setContentTitle("Moodify Add To Pool")
                        .setContentText("There was an error in analysing process - Please try again")
                        .setSmallIcon(R.drawable.ic_launcher_foreground)
                        .setContentIntent(pendingIntent)
                        .build();
                manager.notify(endAnalysisId, notification);
                dialog.setMessage("There was an error in analysing process - Please try again");
                if(!dialog.isShowing()){
                    dialog.show();
                }
                Log.i("APS", "Stopping Service on Failure");
                stopForeground(true);
            }
        });

    }

}
