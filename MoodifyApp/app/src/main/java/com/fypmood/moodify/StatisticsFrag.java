package com.fypmood.moodify;

import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.appcompat.app.AlertDialog;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import com.fypmood.moodify.models.StatisticsRequest;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.formatter.PercentFormatter;
import com.github.mikephil.charting.highlight.Highlight;
import com.github.mikephil.charting.listener.OnChartValueSelectedListener;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.fypmood.moodify.MainActivity.dialog;

public class StatisticsFrag extends Fragment {
    PieChart pieChart;
    Map<String, Integer> moodSongCounts;

    @Override
    public View onCreateView (LayoutInflater inflater, ViewGroup container,
                              Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.fragment_statistics, container, false);

        pieChart = rootView.findViewById(R.id.piechart);
        pieChart.setNoDataText("Getting your library mood statistics....");
        pieChart.setNoDataTextColor(ContextCompat.getColor(getActivity(), R.color.SpotifyWhite));

        moodSongCounts = null;

        // Get statistics from server
        StatisticsAPI();

        return rootView;
    }

    private void StatisticsAPI(){
        RetrofitClient retrofitClient = new RetrofitClient();

        MainActivity mainActivity = (MainActivity) getActivity();
        String user_id = mainActivity.mSharedPreferences.getString("USERID", "");
        String auth_token = mainActivity.mSharedPreferences.getString("TOKEN", "");

        MoodifyApiEndpoints service = retrofitClient.getRetrofit().create(MoodifyApiEndpoints.class);
        StatisticsRequest apiRequest = new StatisticsRequest(user_id, auth_token);

        Call<StatisticsRequest> statisticsRequestCall = service.MoodStatistics(apiRequest);
        statisticsRequestCall.enqueue(new Callback<StatisticsRequest>() {
            @Override
            public void onResponse(Call<StatisticsRequest> call, Response<StatisticsRequest> response) {
                if(response.isSuccessful()){
                    System.out.println(response.body().getMessage());
                    System.out.println(response.body().getData());
                    moodSongCounts = response.body().getData();
                    System.out.println(moodSongCounts);
                    getPieChart();

                }
                else
                {
                    Log.e("STATS", "Call Unsuccessful - Couldn't get statistics");
                    try {
                        pieChart.setNoDataText("Library mood data unavailable");
                        pieChart.invalidate();
                        System.out.println(response.errorBody().string());
                        dialog = getStatisticsDialog();
                        dialog.show();
                    } catch (IOException e) {
                        e.printStackTrace();
                        pieChart.setNoDataText("Library mood data unavailable");
                        pieChart.invalidate();
                        dialog = getStatisticsDialog();
                        dialog.show();
                    }
                }

            }

            @Override
            public void onFailure(Call<StatisticsRequest> call, Throwable t) {
                Log.e("STATS", "Call Failed - Couldn't get statistics");
                pieChart.setNoDataText("Library mood data unavailable");
                pieChart.invalidate();
                System.out.println(t.toString());
                System.out.println(t.getMessage());
                dialog = getStatisticsDialog();
                dialog.show();

            }
        });



    }

    private void getPieChart(){
        // Return if no data
        if(moodSongCounts == null)
        {
            Log.i("STAT", "Data returned empty");
            pieChart.setNoDataText("Library mood data unavailable");
            pieChart.invalidate();
            return;
        }

        ArrayList<PieEntry> entries = new ArrayList<>();

        ArrayList<Integer> color = new ArrayList<>();

        // Prepare entries with corresponding colors
        for(String mood: moodSongCounts.keySet()){
            entries.add(new PieEntry(Objects.requireNonNull(moodSongCounts.get(mood)), mood));
            if(mood.equals("angry")) {
                color.add(ContextCompat.getColor(getActivity(), R.color.angryColor));
            }
            else if(mood.equals("happy"))
            {
                color.add(ContextCompat.getColor(getActivity(), R.color.happyColor));
            }
            else if(mood.equals("relaxed"))
            {
                color.add(ContextCompat.getColor(getActivity(), R.color.relaxedColor));
            }
            else if(mood.equals("sad"))
            {
                color.add(ContextCompat.getColor(getActivity(), R.color.sadColor));
            }
        }

        // Initialize the dataset for the pie-chart
        PieDataSet pieDataSet = new PieDataSet(entries, "");

        // Text size
        pieDataSet.setValueTextSize(18f);
        pieChart.setEntryLabelTextSize(18f);

        // Set the colors for the pie-chart
        pieDataSet.setColors(color);

        PieData pieData = new PieData(pieDataSet);

        // Set legend text white
        pieChart.getLegend().setTextColor(Color.WHITE);

        // Put Legend on the top right of screen
        pieChart.getLegend().setVerticalAlignment(Legend.LegendVerticalAlignment.TOP);
        pieChart.getLegend().setHorizontalAlignment(Legend.LegendHorizontalAlignment.RIGHT);
        pieChart.getLegend().setOrientation(Legend.LegendOrientation.VERTICAL);
        pieChart.getLegend().setTextSize(15f);

        // Set Hole & Transparent hole colour and size
        pieChart.setHoleColor(ContextCompat.getColor(getActivity(), R.color.SpotifyBlack));
        pieChart.setTransparentCircleRadius(50f);
        pieChart.setHoleRadius(35f);

        // Don't let pie-chart rotate
        pieChart.setRotationEnabled(false);

        // Hide description
        pieChart.getDescription().setEnabled(false);

        // Show percentage instead of count
        pieChart.setUsePercentValues(true);

        // Show percentage symbol beside values
        pieData.setValueFormatter(new PercentFormatter(pieChart));

        // Attach the dataset
        pieChart.setData(pieData);

        // Update pie-chart
        pieChart.invalidate();
    }

    // Alert dialog for Statistics process
    private AlertDialog getStatisticsDialog(){
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());

        builder.setMessage("Could not load your statistics. Please try again")
                .setNeutralButton("Close", (dialog, which) -> Log.i("STAT", "Closing STAT dialog"))
                .setTitle(R.string.app_name);

        return builder.create();
    }

}
