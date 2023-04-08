import pandas as pd
from kivy import platform
import os

if platform == 'android':
    from androidstorage4kivy import SharedStorage
    
def generate_xlsx(historical_frames, current_frame, T,  filename='report.xlsx', skip_frames = 1):
    # Create a DataFrame with the data
    print('generate_xlsx: ')
    df = pd.DataFrame(historical_frames, columns=current_frame.keys())
    
    # Add a timestamp index
    MAX_FRAMES = len(historical_frames)
    timestamp = range(0, T, skip_frames)[-MAX_FRAMES:]
    df.insert(0, "T (s)", timestamp)

    report_dir = './assets/report/'

    # check if the report_dir exists
    if not os.path.exists(report_dir):
        # create a directory
        os.mkdir(report_dir)
    report_path = report_dir +  filename
    # Save the DataFrame to an Excel file
    df.to_excel(report_path, index=False)

    if platform == 'android':
        ss = SharedStorage()
        # copy to private
        report_path = ss.copy_to_shared(report_path)

    print(f"write {report_path}")