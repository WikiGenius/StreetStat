import pandas as pd

def generate_xlsx(historical_frames, current_frame, T,  filename='report.xlsx', skip_frames = 1):
    # Create a DataFrame with the data
    df = pd.DataFrame(historical_frames, columns=current_frame.keys())
    
    # Add a timestamp index
    MAX_FRAMES = len(historical_frames)
    timestamp = range(0, T, skip_frames)[-MAX_FRAMES:]
    df.insert(0, "T (s)", timestamp)
    
    # Save the DataFrame to an Excel file
    df.to_excel('./assets/report/' +  filename, index=False)
    print(f"write {filename}")