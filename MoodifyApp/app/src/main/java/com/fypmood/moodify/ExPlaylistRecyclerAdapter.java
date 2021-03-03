package com.fypmood.moodify;

import android.content.Context;
import android.util.Log;
import android.util.SparseBooleanArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckedTextView;

import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import kaaes.spotify.webapi.android.models.PlaylistSimple;

public class ExPlaylistRecyclerAdapter extends RecyclerView.Adapter<ExPlaylistRecyclerAdapter.ViewHolder>
{
    private List<PlaylistSimple> mPlaylistList;
    private Context context;
    private ActionCallback mActionCallback;
    private SparseBooleanArray checkBoxState = new SparseBooleanArray();


    interface ActionCallback
    {
        void onClickListener(PlaylistSimple playlist);
    }

    public ExPlaylistRecyclerAdapter(Context context, List<PlaylistSimple> mPlaylistList)
    {
        this.context = context;
        this.mPlaylistList = mPlaylistList;

    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType)
    {
        View view = LayoutInflater.from(context).inflate(R.layout.list_playlist, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position){ holder.bindData(position);}

    @Override
    public int getItemCount() { return mPlaylistList.size();}

    class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener{
        private CheckedTextView mExistingPlaylist;

        ViewHolder(View itemView){
            super(itemView);
            itemView.setOnClickListener(this);
            mExistingPlaylist = itemView.findViewById(R.id.list_item);
        }

        void bindData(int position)
        {
            PlaylistSimple playlist = mPlaylistList.get(position);

            String plName = playlist.name;
            mExistingPlaylist.setText(plName+" "+position);

            if(!checkBoxState.get(position, false))
            {
                Log.i("Adapter", "Empty"+position+" "+checkBoxState.toString());
                mExistingPlaylist.setChecked(false);
            }
            else
            {
                Log.i("Adapter", "Checked"+position+" "+checkBoxState.toString());
                mExistingPlaylist.setChecked(true);
            }
        }

        @Override
        public void onClick(View v)
        {
            if(mActionCallback != null)
            {
                mActionCallback.onClickListener(mPlaylistList.get(getAdapterPosition()));
            }

            if(!checkBoxState.get(getAdapterPosition(), false))
            {
                mExistingPlaylist.setChecked(true);
                checkBoxState.put(getAdapterPosition(),true);
            }
            else
            {
                mExistingPlaylist.setChecked(false);
                checkBoxState.put(getAdapterPosition(), false);
            }
            Log.i("CheckboxState", checkBoxState.toString());

        }
    }

    void addActionCallback(ActionCallback actionCallback) { mActionCallback = actionCallback; }

}
