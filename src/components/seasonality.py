import pandas as pd



def data_preparation(weather: pd.DataFrame):

    weather.index = pd.to_datetime(weather.index, dayfirst=True)
    range = weather.index[
        (weather.index < pd.to_datetime('2018-09-01'))
        & (weather.index >= pd.to_datetime('2018-06-01'))
    ]

    winter_max = weather.loc[range, :].Max.tolist()
    winter_min = weather.loc[range, :].Min.tolist()
    winter_x = weather.loc[range, :].index.tolist()
    winter_temp = winter_max + winter_min[::-1]
    winter_x = winter_x + winter_x[::-1]
    return winter_x, winter_temp

