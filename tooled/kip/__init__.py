import os
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

def open_file(path:str) -> pd.DataFrame:
    """
    Open a .csv results file from KNIME.
    :param path: Path to the .csv results file.
    :return: Pandas DataFrame.
    """
    print(f"Opening file {os.path.basename(path)}")
    try:
        df = pd.read_csv(path, sep=',').drop(['row ID'], axis='columns')
    except:
        df = pd.read_csv(path, sep=',')

    return df

def write_file(dataframe:pd.DataFrame, file_name:str):
    """
    Write DataFrame to file.
    :param dataframe: Pandas DataFrame to be saved to file.
    :param file_name: Name of file to be saved.
    """
    if '.csv' in file_name:
        name = file_name
    else:
        name = file_name + '.csv'
    
    print(f"Saving file {name}.")
    dataframe.to_csv(name)

    return

def display_track_sum(dataframe:pd.DataFrame, channel_name:str, style='scatter'):
    """
    Sums individual tracks over time and displays x/y scatter graph.
    """
    # check for valid channel name
    try:
        if _check_valid_channel(dataframe, channel_name):
            print("Suming tracks...")
            df_track_sum = dataframe.groupby('track').sum().reset_index()
            sns.relplot(x='track', y=channel_name, data=df_track_sum)
            plt.show()
    except:
        pass

    return

def display_shade_line_graph(dataframe:pd.DataFrame, channel_name:str):
    """
    Things
    """
    sns.relplot(x='time', y=channel_name, hue='loc', style='loc', kind='line', data=dataframe)
    plt.show()

    return

def delete_track(dataframe:pd.DataFrame, track_name:str) -> pd.DataFrame:
    """
    Delete the specified track from the DataFrame.
    :param dataframe: Input DataFrame.
    :param track_name: Name of track to delete.
    """

    # get empty DataFrame
    df_trim = _create_empty_dataframe(dataframe)
    print(f"Deletinging: {track_name}")
    delete_row = dataframe[dataframe['track'] == track_name].index
    df_trim = dataframe.drop(delete_row)
    print(f"{len(delete_row)} elements deleted.")
    print(f"Old DataFrame size: {len(dataframe)}\nNew DataFrame size: {len(df_trim)}")

    return df_trim

def filter_track(dataframe:pd.DataFrame, channel_name:str, threshold:float, position:str) -> pd.DataFrame:
    """
    Filter tracks from a DataFrame.
    :param dataframe: Input DataFrame to be filtered.
    :param channel_name: Channel to filter.
    :param threshold: Threshold signal value.
    :param position: Filter positional argument.
    :return: Filtered DataFrame.
    """
    dataframe_track_sum = dataframe.groupby('track').sum().reset_index()
    sorted_tracks = []

    if position == 'above':
        sort_value = threshold
        for index, row in dataframe_track_sum.iterrows():
            if row[channel_name] <= sort_value:
                sorted_tracks.append(row['track'])
    elif position == 'below':
        sort_value = threshold
        for index, row in dataframe_track_sum.iterrows():
            if row[channel_name] >= sort_value:
                sorted_tracks.append(row['track'])
    else:
        print(f"position={position} is invalid. Valid string values are \"above\" and \"below\".")
        
        return

    # create unique track list and empty DataFrame for filtered values
    sorted_tracks_unique = set(sorted_tracks)
    df_filtered = _create_empty_dataframe(dataframe)

    # create new DataFrame with matched traks
    for index, row in dataframe.iterrows():
        if row['track'] in sorted_tracks_unique:
            df_filtered = df_filtered.append(row)
        else:
            pass

    return df_filtered

def _create_empty_dataframe(dataframe:pd.DataFrame) -> pd.DataFrame:
    """
    Create an empty Pandas DataFrame from an existing DataFrame.
    :param dataframe: Input DataFrame.
    """
    df_col_names = list(dataframe.columns.values)
    empty_df = pd.DataFrame(columns=df_col_names)

    return empty_df

def _check_valid_channel(dataframe:pd.DataFrame, channel_name:str) -> bool:
    data_status = False
    df_col_names = list(dataframe.columns.values)
    for name in df_col_names:
        if channel_name in df_col_names:
            data_status = True
        else:
            print(f"Channel: {channel_name} was not found in the DataFrame.")
    
    return data_status