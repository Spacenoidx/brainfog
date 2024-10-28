import statsapi
import pandas as pd
from datetime import datetime
import time

def get_pitch_data_for_season(year):
    """
    Fetches pitch-by-pitch data for an entire MLB season.
    
    Args:
        year (int): The season year to fetch data for
    
    Returns:
        DataFrame: Pitch-by-pitch data for the season
    """
    # Get all games for the season
    schedule = statsapi.schedule(start_date=f'{year}-01-01', 
                               end_date=f'{year}-12-31',
                               sportId=1,
                               )  # 1 is MLB
    
    all_pitches = []
    
    for game in schedule:
        game_id = game['game_id']
        try:
            # Get play-by-play data
            plays = statsapi.get('game_playByPlay', {'gamePk': game_id})
            
            # Extract pitch data from each play
            for play in plays['allPlays']:
                for pitch_index, pitch in enumerate(play.get('playEvents', [])):
                    if pitch['type'] == 'pitch':
                        pitch_data = {
                            'game_id': game_id,
                            'game_date': game['game_date'],
                            'game_Type': game['game_type'],
                            'inning': play['about']['inning'],
                            'top_inning': play['about']['isTopInning'],
                            'pitch_number': pitch_index + 1,
                            'pitcher_id': play['matchup']['pitcher']['id'],
                            'pitcher_name': play['matchup']['pitcher']['fullName'],
                            'batter_id': play['matchup']['batter']['id'],
                            'batter_name': play['matchup']['batter']['fullName'],
                            'pitch_type': pitch['details'].get('type', {}).get('description'),
                            'pitch_speed': pitch['pitchData'].get('startSpeed'),
                            'pitch_result': pitch['details'].get('description'),
                            'balls': pitch['count']['balls'],
                            'strikes': pitch['count']['strikes']
                        }
                        all_pitches.append(pitch_data)
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing game {game_id}: {str(e)}")
            continue
    
    # Convert to DataFrame
    df = pd.DataFrame(all_pitches)
    
    # Add some derived statistics
    df['is_strike'] = df['pitch_result'].str.contains('Strike|Foul|In play', case=False, na=False)
    df['is_swing'] = df['pitch_result'].str.contains('Swinging|Foul|In play', case=False, na=False)
    
    return df

def save_pitch_data(df, year):
    """
    Saves pitch data to CSV with basic error handling
    """
    try:
        filename = f'mlb_pitches_{year}.csv'
        df.to_csv(filename, index=False)
        print(f"Successfully saved data to {filename}")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

# Example usage:
year = 2024
pitch_data = get_pitch_data_for_season(year)
save_pitch_data(pitch_data, year)