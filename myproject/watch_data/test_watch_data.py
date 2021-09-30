import watch_data

def test_calculate_speed():
    result = watch_data.calculate_speed(5.0, .45)
    assert result==11.11111111111111
    
    result = watch_data.calculate_speed(5.0, .45, output_distance_unit='mi')
    assert result==6.904122222222222
    
    

def test_time_difference():
    result = watch_data.time_difference('1900-01-01 00:00:00 -0500', '1901-01-01 00:05:00 -0500')
    assert result==8760.083333333334
    
    result = watch_data.time_difference('1900-01-01 00:00:00 -0500', '1901-01-01 00:06:00 -0500')
    assert result==8760.1