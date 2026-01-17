def song_stats(df):
    songs = df[df['content_type'] == 'song']

    top_songs = (
        songs
        .groupby(['track_name', 'artist_name'])
        .agg(
            plays=('track_name', 'count'),
            hours=('hours_played', 'sum')
        )
        .reset_index()
        .sort_values(by='plays', ascending=False)
        .head(10)
    )
    
    top_genre = (
    songs
    .groupby('genre')['hours_played']
    .sum()
    .idxmax()
    if 'genre' in songs.columns else 'mixed'
)

    most_played_day = (
        songs
        .groupby('date')['hours_played']
        .sum()
        .idxmax()
    )

    total_hours = songs['hours_played'].sum()

    champion = None
    if not top_songs.empty:
        row = top_songs.iloc[0]
        champion = {
            'track_name': row['track_name'],
            'artist_name': row['artist_name'],
            'plays': int(row['plays']),
            'hours': round(row['hours'], 2)
        }
        
    top_songs = top_songs.to_dict(orient='records')

    return {
        'top_songs': top_songs,
        'most_played_day': most_played_day,
        'total_hours': round(total_hours, 2),
        'champion': champion,
        'top_genre': top_genre
    }
    
    
def artist_stats(df):
    songs = df[df['content_type'] == 'song']

    artists = (
        songs
        .groupby('artist_name')
        .agg(
            total_plays=('track_name', 'count'),
            unique_songs=('track_name', 'nunique'),
            hours=('hours_played', 'sum')
        )
        .reset_index()
        .sort_values(by='total_plays', ascending=False)
        .head(10)
    )

    champion = None
    if not artists.empty:
        row = artists.iloc[0]
        champion = {
            'artist_name': row['artist_name'],
            'total_plays': int(row['total_plays']),
            'unique_songs': int(row['unique_songs'])
        }

    return {
        'top_artists': artists.to_dict(orient='records'),
        'champion': champion
    }

   
def podcast_stats(df):
    podcasts = df[df['content_type'] == 'podcast']

    if podcasts.empty:
        return None

    top_podcasts = (
        podcasts
        .groupby('episode_show_name')
        .agg(
            plays=('episode_name', 'count'),
            hours=('hours_played', 'sum')
        )
        .reset_index()
        .sort_values(by='plays', ascending=False)
        .head(10)
    )

    most_played_day = (
        podcasts
        .groupby('date')['hours_played']
        .sum()
        .idxmax()
    )

    return {
        'top_podcasts': top_podcasts.to_dict(orient='records'),
        'most_played_day': most_played_day,
        'total_hours': round(podcasts['hours_played'].sum(), 2)
    }
    
def time_stats(df):
    first_play = df['ts'].min()
    last_play = df['ts'].max()

    yearly = (
        df
        .groupby('year')
        .agg(
            hours=('hours_played', 'sum'),
            plays=('ts', 'count')
        )
        .reset_index()
        .sort_values(by='year')
    )

    return {
        'first_play': first_play,
        'last_play': last_play,
        'yearly': yearly.to_dict(orient='records')
    }
    
def yearly_comparison(df):
    yearly = (
        df[df['content_type'] == 'song']
        .groupby('year')
        .agg(
            hours=('hours_played', 'sum'),
            plays=('ts', 'count'),
            unique_artists=('artist_name', 'nunique')
        )
        .reset_index()
        .sort_values('year')
    )

    return yearly.to_dict(orient='records')

def skipped_tracks(df):
    skipped = df[df['skipped'] == True]

    top_skipped = (
        skipped
        .groupby(['track_name', 'artist_name'])
        .size()
        .reset_index(name='skips')
        .sort_values('skips', ascending=False)
        .head(5)
    )

    return top_skipped.to_dict(orient='records')

def platform_stats(df):
    platforms = (
        df.groupby('platform')
        .size()
        .reset_index(name='plays')
        .sort_values('plays', ascending=False)
    )
    return platforms.to_dict(orient='records')

def country_stats(df):
    countries = (
        df.groupby('conn_country')
        .size()
        .reset_index(name='plays')
        .sort_values('plays', ascending=False)
    )
    return countries.to_dict(orient='records')

def audio_personality(df):
    avg_session = df['minutes_played'].mean()

    if avg_session > 8:
        return "Deep Listener 🥹🎧"
    elif avg_session > 3:
        return "Casual Groover 🎶"
    else:
        return "Skipper 🐧"