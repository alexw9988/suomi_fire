
import numpy as np


def maskFlags(data, flag_array, flag_meanings, flag_values, flag_selection, mode='binary_and'):
    for flag_name in flag_selection:
        for i, meaning in enumerate(flag_meanings):
            if meaning == flag_name:
                value = flag_values[i]
                if mode == 'binary_and': 
                    data = np.where(flag_array & value, np.nan, data)
                elif mode == 'equal':
                    data = np.where(flag_array == value, np.nan, data)

    return data
