import pandas as pd
from kivy import platform

if platform == 'android':
    from androidstorage4kivy import SharedStorage
    
def generate_xlsx(historical_frames, current_frame, T,  filename='report.xlsx', skip_frames = 1):
    # Create a DataFrame with the data
    df = pd.DataFrame(historical_frames, columns=current_frame.keys())
    
    # Add a timestamp index
    MAX_FRAMES = len(historical_frames)
    timestamp = range(0, T, skip_frames)[-MAX_FRAMES:]
    df.insert(0, "T (s)", timestamp)
    
    # Save the DataFrame to an Excel file
    report_path = './assets/report/' +  filename
    df.to_excel(report_path, index=False)
    if platform == 'android':
        ss = SharedStorage()
        # copy to private
        report_path = ss.copy_to_shared(report_path)

    print(f"write {report_path}")