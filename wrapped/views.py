from django.shortcuts import render, redirect
import json
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .spotify_processor import load_spotify_files, clean_spotify_data
from .stats_engine import (
    song_stats,
    artist_stats,
    podcast_stats,
    time_stats,
    yearly_comparison,
    skipped_tracks,
    platform_stats,
    country_stats,
    audio_personality
)
import uuid
from django.core.cache import cache

# Create your views here.
def home(request):
    return render(request, 'wrapped/home.html')

def how_it_works(request):
    return render(request, 'wrapped/how_it_works.html')

def upload_data(request):
    if request.method == 'POST':
        files = request.FILES.getlist('spotify_files')

        if not files:
            return render(request, 'wrapped/upload.html', {
                'error': 'Please upload at least one JSON file.'
            })

        fs = FileSystemStorage()
        uploaded_files = []

        for file in files:
            if not file.name.endswith('.json'):
                return render(request, 'wrapped/upload.html', {
                    'error': 'Only JSON files are allowed.'
                })

            filename = fs.save(file.name, file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Basic JSON validation
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                os.remove(file_path)
                return render(request, 'wrapped/upload.html', {
                    'error': f'{file.name} is not a valid JSON file.'
                })

            uploaded_files.append(file_path)

        df = load_spotify_files(uploaded_files)
        df = clean_spotify_data(df)
        
        yearly_data = yearly_comparison(df)
        song_data = song_stats(df)
        artist_data = artist_stats(df)
        podcast_data = podcast_stats(df)
        time_data = time_stats(df)
        skipped_data = skipped_tracks(df)
        platform_data = platform_stats(df)
        country_data = country_stats(df)
        personality = audio_personality(df)
        
        token = str(uuid.uuid4())[:8]

        cache.set(token, {
            'file_count': len(df),
            'total_hours': round(df['hours_played'].sum(), 2),
            'total_days': round((df['hours_played'].sum()) / 24, 2),
            'total_minutes': round(df['minutes_played'].sum(), 2),
            'total_plays': len(df),
            'song_data': song_data,
            'artist_data': artist_data,
            'podcast_data': podcast_data,
            'time_data': time_data,
            'yearly_data': yearly_data,
            'skipped_data': skipped_data,
            'platform_data': platform_data,
            'country_data': country_data,
            'personality': personality,
        }, timeout=86400)
                

        # Deleting files immediately for my customers privacy
        for path in uploaded_files:
            os.remove(path)

        # TEMP: show basic confirmation
        return redirect("wrapped:wrapped_result", token=token)
        
        

    return render(request, 'wrapped/upload.html')

def wrapped_result(request, token):
    data = cache.get(token)

    if not data:
        return render(request, 'wrapped/expired.html')

    return render(request, 'wrapped/results.html', data)