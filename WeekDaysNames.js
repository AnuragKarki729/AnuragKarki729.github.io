import React from 'react';
import { Text } from 'react-native';
import { weekDayNames } from '../dateutils';
const WeekDaysNames = React.memo(({ style }) => {
    const dayNames = weekDayNames(6);
    return dayNames.map((day, index) => (<Text 
    allowFontScaling={false} 
    key={index} 
    style={style} 
    numberOfLines={1} 
    accessibilityLabel={''}>
      {day}
    </Text>));
});
export default WeekDaysNames;
