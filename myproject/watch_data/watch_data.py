"""
This is a module that does fun things with Apple Watch / Apple Health data dumps. 
This module is intended to be used and developed on by students in Purdue Universities The Data Mine.
"""

import datetime
from typing import Callable
from pathlib import Path
from collections import defaultdict

import lxml
import lxml.etree
import plotly.express as px
import pandas as pd


def example_filter(element: lxml.etree._Element) -> bool:
    """
    An example of a filter to be used with the `WatchData` class. Any
    filter should accept a single `lxml.etree._Element` and return True
    if it meets a given, generic criteria, and False otherwise. 
    
    Any data will be returned where the filter returns True. In this example
    this filter returns only "Workout" elements representing runs that last 
    more than 30 minutes.
    """
    if element.get('workoutActivityType') == 'HKWorkoutActivityTypeRunning':
        if duration := float(element.get('duration')):
            return duration >= 30.0

        
def calculate_speed(distance: float, time: float, distance_unit: str = 'km', time_unit: str = 'hours', output_distance_unit: str = '', output_time_unit: str = ''):
    """
    Given the distance and time, calculate the speed. The distance unit and time unit can be specified.
    If not specified, the default unit is km and hour respectively.
    
    Additionally, the output unit can be specified. If not specified, the default units will match the 
    `distance_unit` and be presented using `hours` for the `output_time_unit`.

    >>> calculate_speed(5.0, .55, output_distance_unit='mi')
    5.648827272727272
    
    >>> calculate_speed(5.0, .55, output_distance_unit='km')
    9.09090909090909
    
    >>> calculate_speed(5.0, 1)
    5.0

    >>> calculate_speed(5.0, .55, output_distance_unit = 'm')
    Traceback (most recent call last):
        ...
    ValueError: output_distance_unit must be 'mi' or 'km'

    Args:
        distance (float): The distance, in `distance_unit` units.
        time (float): The time taken to travel `distance` in `time_unit` units.
        distance_unit (str, optional): The distance unit representing `distance`. Defaults to 'km'.
            Valid units are:
                - 'km'
                - 'mi'
        time_unit (str, optional): The time unit representing `time_unit`. Defaults to 'hours'.
            Valid units are:
                - 'seconds'
                - 'minutes'
                - 'hours'
    """
    
    def _convert_time(time: float, time_unit: str, output_time_unit: str) -> float:
        """
        Convert the time to the output time unit.
        
        Args:
            time (float): The time to convert.
            time_unit (str): The time unit of the input time.
            output_time_unit (str): The time unit of the output time.
            
        Raises:
            ValueError: If the input time unit is not valid.
            
        Returns:
            float: The converted time.
        """
        if time_unit == 'seconds':
            if output_time_unit == 'minutes':
                return time / 60
            elif output_time_unit == 'hours':
                return time / 3600
        elif time_unit == 'minutes':
            if output_time_unit == 'seconds':
                return time * 60
            elif output_time_unit == 'hours':
                return time / 60
        elif time_unit == 'hours':
            if output_time_unit == 'seconds':
                return time * 3600
            elif output_time_unit == 'minutes':
                return time * 60
        else:
            raise ValueError(f'Invalid time unit: {time_unit}')
    
    def _convert_distance(distance: float, distance_unit: str, output_distance_unit: str) -> float:
        """
        Given a distance value, distance unit and output distance unit, convert the distance to the output distance unit.
        
        Args:
            distance (float): The distance to convert.
            distance_unit (str): The distance unit of the distance.
            output_distance_unit (str): The output distance unit.
            
        Raises:
            ValueError: If the distance unit is not valid.
            
        Returns:
            float: The converted distance.
        """
        if distance_unit == 'km':
            if output_distance_unit == 'mi':
                return distance * 0.621371
            elif output_distance_unit == 'km':
                return distance
            else:
                raise ValueError("output_distance_unit must be 'mi' or 'km'")
        elif distance_unit == 'mi':
            if output_distance_unit == 'km':
                return distance * 1.60934
            elif output_distance_unit == 'mi':
                return distance
            else:
                raise ValueError("output_distance_unit must be 'mi' or 'km'")
        else:
            raise ValueError(f'Invalid distance unit: {distance_unit}')
        
    # if output distance and time not specified, use 
    # the distance and time units as the output units
    if output_distance_unit == '':
        output_distance_unit = distance_unit
        
    if output_time_unit == '':
        output_time_unit = time_unit
        
    if distance_unit != output_distance_unit:
        distance = _convert_distance(distance, distance_unit, output_distance_unit)
        
    if time_unit != output_time_unit:
        time = _convert_time(time, time_unit, output_time_unit)
        
    return distance / time


def time_difference(d1: str, d2: str, unit: str = 'hours') -> float:
    """
    Given two strings in the format matching the format in 
    Apple Watch data: YYYY-MM-DD HH:MM:SS -XXXX, return
    a decimal number representing the time difference in 
    `unit` between the two datetimes.
    
    >>> time_difference('1900-01-01 00:00:00 -0500', '1901-01-01 00:00:00 -0500')
    8760.0
    
    >>> time_difference('1900-01-01 00:00:00 -0500', '1901-01-02 00:00:00 -0500')
    8784.0
    
    >>> time_difference('1900-01-01 00:00:00 -0500', '1901-01-01 00:00:00 -0400')
    8759.0

    Args:
        d1 (str): The first datetime string.
        d2 (str): The second datetime string.
        unit (str, optional): The unit of time difference. Defaults to 'hours'.
            Valid units are:
                - 'seconds'
                - 'minutes'
                - 'hours'
                - 'days'
                - 'weeks'
                - 'years'

    Returns:
        float: The time difference between the two datetimes
            in the specified unit.
    """
    d1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S %z')
    d2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S %z')
    
    absolute_difference_in_seconds = abs((d2 - d1).total_seconds())
    
    if unit == 'seconds':
        return absolute_difference_in_seconds
    elif unit == 'minutes':
        return absolute_difference_in_seconds / 60
    elif unit == 'hours':
        return absolute_difference_in_seconds / 3600
    elif unit == 'days':
        return absolute_difference_in_seconds / 86400
    elif unit == 'weeks':
        return absolute_difference_in_seconds / 604800
    elif unit == 'years':
        return absolute_difference_in_seconds / 31556926
    else:
        raise ValueError(f'Invalid unit: {unit}. Possible units are: seconds, minutes, hours, days, weeks, years.')
    

class WatchData:
    def __init__(self, path: str):
        self._path = Path(path)
    
    def __str__(self):
        return f'Watch data from: {self._path}'
    
    
    def plot_speed_by_run(self):
        """
        Produce a bar plot showing the speed of the run by day.
        """

        def _filter_runs(element: lxml.etree._Element) -> bool:
            """
            Filter to filter run data.
            """
            if element.get('workoutActivityType') == 'HKWorkoutActivityTypeRunning':
                return True
            
        runs = self.filter_elements(_filter_runs)
        
        tracker = defaultdict(float)
        results = dict()
        results['date'] = []
        results['speed'] = []
        
        # for each run, calculate the speed in km/hr
        # for now, just append the first run for any given date
        for run in runs:
            time_in_hours = time_difference(run.attrib['startDate'], run.attrib['endDate'])
            date_key = datetime.datetime.strptime(run.attrib['creationDate'], '%Y-%m-%d %H:%M:%S %z').date().strftime('%Y-%m-%d')
            if not tracker.get(date_key):
                tracker[date_key] = 1
                results['date'].append(date_key)
                results['speed'].append(calculate_speed(float(run.attrib['totalDistance']), time_in_hours, distance_unit = run.attrib['totalDistanceUnit']))
                                       
        df = pd.DataFrame(data=results)
        fig = px.bar(df, x='date', y='speed', log_y=True)
        fig.show()
        
    
    def filter_elements(self, filt: Callable) -> list[lxml.etree._Element]:
        """
        `filter_elements` accepts a function (or "filter") and applies 
        the filter to parse the accepted elements from the XML.
        
        A filter is any function that accepts a `lxml.etree._Element` and
        returns either `True` or `False`. Elements that return `True` are
        kept and returned as a list. Elements that return `False` are not.

        Args:
            filt (Callable): Any function that accepts a `lxml.etree._Element` and
                returns either `True` or `False`. Elements that return `True` are
                kept and returned as a list. Elements that return `False` are not.
    
        Returns:
            list[lxml.etree._Element]: A list of filtered elements.
        """
        results = []
        tree = lxml.etree.iterparse(str(self._path / 'export.xml'))
        for _, element in tree:
            if filt(element):
                results.append(element)
            else:
                element.clear()
        
        return results


if __name__ == '__main__':
    import doctest
    doctest.testmod()
