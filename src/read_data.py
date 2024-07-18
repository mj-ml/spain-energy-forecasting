import pandas as pd


def read_load() -> pd.DataFrame:
    df = pd.read_csv('../data/energy_dataset.csv.zip', compression='zip')
    return df


def read_weather() -> pd.DataFrame:
    df = pd.read_csv('../data/weather_features.csv.zip', compression='zip')
    return df


def extract_load(df_load: pd.DataFrame) -> pd.DataFrame:
    columns = ['time', 'total load actual']
    return df_load[columns]


def extract_weather(df_weather: pd.DataFrame) -> pd.DataFrame:
    columns = ['dt_iso', 'temp']
    return df_weather[columns].groupby('dt_iso').mean()


def create_dataframe(df_weather: pd.DataFrame, df_load: pd.DataFrame, ) -> pd.DataFrame:
    return df_weather.merge(df_load, left_on='dt_iso', right_on='time')