
import numpy as np


def maskQualityFlags(data, quality_flags, quality_flag_meanings, quality_flag_masks, mask_quality_flags):
    flag_masks = []
    for mask in mask_quality_flags:
        for i, meaning in enumerate(quality_flag_meanings):
            if meaning == mask:
                flag_masks.append(quality_flag_masks[i])

    output = np.ma.masked_where(quality_flags in flag_masks, data)
    return output

def maskWater(data, water_mask):
    output = np.ma.masked_where(water_mask != 1, data)
    return output
