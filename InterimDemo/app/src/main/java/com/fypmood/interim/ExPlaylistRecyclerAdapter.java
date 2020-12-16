package com.fypmood.interim;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.fypmood.interim.models.Playlist;

import java.util.List;

import kaaes.spotify.webapi.android.models.PlaylistSimple;

public class ExPlaylistRecyclerAdapter extends RecyclerView.Adapter<ExPlaylistRecyclerAdapter.ViewHolder>
{
    private List<PlaylistSimple> mPlaylistList;
    private Context context;
    private ActionCallback mActionCallback;


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
        private TextView mExPlaylistName;

        ViewHolder(View itemView){
            super(itemView);
            itemView.setOnClickListener(this);
            mExPlaylistName = itemView.findViewById(R.id.list_item);
        }

        void bindData(int position)
        {
            PlaylistSimple playlist = mPlaylistList.get(position);

            String plName = playlist.name;
            mExPlaylistName.setText(plName);

        }

        @Override
        public void onClick(View v)
        {
            if(mActionCallback != null)
            {
                mActionCallback.onClickListener(mPlaylistList.get(getAdapterPosition()));
            }
        }
    }

    void addActionCallback(ActionCallback actionCallback) { mActionCallback = actionCallback; }

}
