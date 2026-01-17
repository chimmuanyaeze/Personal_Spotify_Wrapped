import json
import pandas as pd


def load_spotify_files(file_paths):
    """
    Load and merge multiple Spotify Extended Streaming History JSON files.
    """

    all_records = []

    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_records.extend(data)

    df = pd.DataFrame(all_records)
    return df


def clean_spotify_data(df):
    """
    Clean and normalize Spotify streaming data for analytics.
    """

    # Convert timestamp
    df['ts'] = pd.to_datetime(df['ts'], utc=True)

    # Rename fields to consistent internal names
    df = df.rename(columns={
        'master_metadata_track_name': 'track_name',
        'master_metadata_album_artist_name': 'artist_name',
        'master_metadata_album_album_name': 'album_name'
    })

    # Convert milliseconds to hours
    df['hours_played'] = df['ms_played'] / (1000 * 60 * 60)
    df['minutes_played'] = df['ms_played'] / (1000 * 60)

    # Content type classification
    df['content_type'] = 'song'
    df.loc[df['episode_name'].notna(), 'content_type'] = 'podcast'
    df.loc[df['audiobook_title'].notna(), 'content_type'] = 'audiobook'

    # Remove zero-play records (Spotify logs skips)
    df = df[df['ms_played'] > 0]

    # Fill missing text values safely
    df['track_name'] = df['track_name'].fillna('Unknown Track')
    df['artist_name'] = df['artist_name'].fillna('Unknown Artist')
    df['album_name'] = df['album_name'].fillna('Unknown Album')
    df['episode_name'] = df['episode_name'].fillna('')
    df['audiobook_title'] = df['audiobook_title'].fillna('')

    # Extract date & year for grouping
    df['date'] = df['ts'].dt.date
    df['year'] = df['ts'].dt.year

    return df
