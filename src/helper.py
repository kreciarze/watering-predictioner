def convert_soil_moisture_to_dataset_range(value) -> float:
    if value >= 19200: 
        return 90
    elif value <= 8864:
        return 0
    else:
        return (value - 8864) / (19200 - 8864) * 90

def convert_luminescence_to_dataset_range(value) -> float:
    if value >= 24000:
        return 100
    elif value <= 100:
        return 0
    else:
        return (value - 100) / (24000 - 100) * 100