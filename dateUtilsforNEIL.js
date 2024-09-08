
export const formatDateForStorage = (date) => {
    return date.toISOString().split('T')[0]; // Format to YYYY-MM-DD
  };
  

  export const parseDateFromStorage = (dateString) => {
    return new Date(dateString);
  };
  

  export const getLocalDate = (date) => {
    const offset = date.getTimezoneOffset() * 60000; // Offset in milliseconds
    return new Date(date.getTime() - offset);
  };
  

  export const formatTimeString = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  

  //SettingScreen.js:

//   import { 
//     formatDateForStorage, 
//     parseDateFromStorage, 
//     getLocalDate, 
//     formatTimeString 
//   } from './dateUtils';

//   const loadSchedule = async () => {
//     const schedule = await AsyncStorage.getItem(selectedDay);
//     const parsedSchedule = schedule ? JSON.parse(schedule) : { sleepTime: null, wakeUpTime: null, busyTimes: [] };

//     // Use utility functions for date handling
//     setSleepTime(parsedSchedule.sleepTime ? getLocalDate(new Date(parsedSchedule.sleepTime)) : null);
//     setWakeUpTime(parsedSchedule.wakeUpTime ? getLocalDate(new Date(parsedSchedule.wakeUpTime)) : null);
//     setBusyTimes(parsedSchedule.busyTimes || []);
//   };

//   const saveSchedule = async (newSchedule) => {
//     const formattedSchedule = {
//       sleepTime: newSchedule.sleepTime ? formatDateForStorage(newSchedule.sleepTime) : null,
//       wakeUpTime: newSchedule.wakeUpTime ? formatDateForStorage(newSchedule.wakeUpTime) : null,
//       busyTimes: newSchedule.busyTimes || []
//     };
//     await AsyncStorage.setItem(selectedDay, JSON.stringify(formattedSchedule));
//   };

//   const finalizeTimeSelection = () => {
//     setShowTimePicker(false);

//     if (currentEditingField === 'sleep') {
//       setSleepTime(getLocalDate(timePickerValue));
//       saveSchedule({ sleepTime: getLocalDate(timePickerValue), wakeUpTime, busyTimes });
//     } else if (currentEditingField === 'wakeUp') {
//       setWakeUpTime(getLocalDate(timePickerValue));
//       saveSchedule({ sleepTime, wakeUpTime: getLocalDate(timePickerValue), busyTimes });
//     } else if (currentEditingField === 'busyStart') {
//       setNewBusyStartTime(getLocalDate(timePickerValue));
//     } else if (currentEditingField === 'busyEnd') {
//       setNewBusyEndTime(getLocalDate(timePickerValue));
//     }

//     setCurrentEditingField(null);
//   };

//   const handleAddBusyTime = () => {
//     if (newBusyStartTime && newBusyEndTime) {
//       const newBusyTime = `${formatTimeString(newBusyStartTime)} - ${formatTimeString(newBusyEndTime)}`;
//       const updatedBusyTimes = [...busyTimes, newBusyTime];
//       setBusyTimes(updatedBusyTimes);
//       setNewBusyStartTime(null);
//       setNewBusyEndTime(null);
//       saveSchedule({ sleepTime, wakeUpTime, busyTimes: updatedBusyTimes });
//     } else {
//       alert('Please select both start and end times for the busy time.');
//     }
//   };

//   const handleRemoveBusyTime = (time) => {
//     const updatedBusyTimes = busyTimes.filter(t => t !== time);
//     setBusyTimes(updatedBusyTimes);
//     saveSchedule({ sleepTime, wakeUpTime, busyTimes: updatedBusyTimes });
//   };




//In Calendar Screen.js:

//   import { 
//     formatDateForStorage, 
//     parseDateFromStorage, 
//     getLocalDate, 
//     formatTimeString 
//   } from './dateUtils';

// const loadGoals = async (date) => {
//     // Format date for storage retrieval
//     const formattedDate = formatDateForStorage(new Date(date));
//     const goals = await AsyncStorage.getItem(formattedDate);
//     setDailyGoals(goals ? JSON.parse(goals) : []);

//     setMarkedDates({
//       [formattedDate]: {
//         selected: true,
//         marked: true,
//         selectedColor: '#00adf5',
//       },
//     });
//   };

//   const deleteGoal = async (goalId) => {
//     const updatedGoals = dailyGoals.filter(goal => goal.id !== goalId);
//     setDailyGoals(updatedGoals);

//     if (selectedDate) {
//       const formattedDate = formatDateForStorage(new Date(selectedDate));
//       await AsyncStorage.setItem(formattedDate, JSON.stringify(updatedGoals));
//     }
//   };

//   const resetGoals = async () => {
//     if (selectedDate) {
//       const formattedDate = formatDateForStorage(new Date(selectedDate));
//       await AsyncStorage.removeItem(formattedDate);
//       setDailyGoals([]);
//     }
//   };

//   const renderItem = ({ item }) => {
//     const startTime = item.startTime ? parseDateFromStorage(item.startTime) : null;
//     const endTime = item.endTime ? parseDateFromStorage(item.endTime) : null;





//GoalSelectionScreen.js:

// import { formatDateForStorage, parseDateFromStorage, getLocalDate, formatTimeString } from './dateUtils';

// const GoalSelectionScreen = ({ route, navigation }) => {
//     const { date } = route.params || { date: getLocalDate() };


//     const loadDaySchedule = async () => {
//         const localDate = new Date(date);
//         const dayOfWeek = localDate.toLocaleString('en-us', { weekday: 'short' });
//         const schedule = await AsyncStorage.getItem(dayOfWeek);
//         const parsedSchedule = schedule ? JSON.parse(schedule) : { sleepTime: null, wakeUpTime: null, busyTimes: [] };
//         setSleepTime(parsedSchedule.sleepTime ? parseDateFromStorage(parsedSchedule.sleepTime) : null);
//         setWakeUpTime(parsedSchedule.wakeUpTime ? parseDateFromStorage(parsedSchedule.wakeUpTime) : null);
//         setBusyTimes(parsedSchedule.busyTimes || []);
//       };
    
//       const loadScheduledGoals = async () => {
//         const formattedDate = formatDateForStorage(new Date(date));
//         const existingGoals = await AsyncStorage.getItem(formattedDate);
//         if (existingGoals) {
//           setScheduledGoals(JSON.parse(existingGoals));
//         }
//       };
    
//       const addGoal = () => {
//         if (!goalText || !duration) {
//           Alert.alert('Error', 'Please enter both a goal and duration.');
//           return;
//         }
    
//         const goal = {
//           id: Date.now().toString(),
//           name: goalText.trim(),
//           duration: parseInt(duration, 10),
//           dimension: 'Custom',
//           startTime: null,
//           endTime: null,
//         };
    
//         const availableSlot = findAvailableTimeSlot(goal.duration);
//         if (!availableSlot) {
//           Alert.alert('Error', 'No available time slot for this task.');
//           return;
//         }
    
//         goal.startTime = availableSlot.startTime;
//         goal.endTime = new Date(availableSlot.startTime.getTime() + goal.duration * 60000);
    
//         setSelectedGoals(prevGoals => [...prevGoals, goal]);
//         setGoalText('');
//         setDuration('');
//       };
    
//       const findAvailableTimeSlot = (duration) => {
//         if (!wakeUpTime || !sleepTime) {
//           Alert.alert('Error', 'Please make sure both sleep and wake-up times are set.');
//           return null;
//         }
    
//         const startOfDay = new Date(wakeUpTime.getTime());
//         const endOfDay = new Date(sleepTime.getTime());
    
//         // Merge all busy times including sleep, scheduled tasks, and currently selected goals
//         const allBusyTimes = [
//           ...busyTimes.map(bt => ({
//             startTime: parseDateFromStorage(bt.startTime),
//             endTime: parseDateFromStorage(bt.endTime),
//           })),
//           ...scheduledGoals.map(goal => ({
//             startTime: parseDateFromStorage(goal.startTime),
//             endTime: parseDateFromStorage(goal.endTime),
//           })),
//           ...selectedGoals.map(goal => ({
//             startTime: parseDateFromStorage(goal.startTime),
//             endTime: parseDateFromStorage(goal.endTime),
//           })),
//           {
//             startTime: endOfDay,
//             endTime: new Date(endOfDay.getTime() + 8 * 60 * 60 * 1000), // Assuming 8 hours of sleep
//           },
//         ];
    
//         // Sort busy times by start time
//         allBusyTimes.sort((a, b) => a.startTime - b.startTime);
    
//         // Split the day into 15-minute time blocks
//         const timeBlock = 15 * 60 * 1000; // 15 minutes in milliseconds
//         let blockStart = startOfDay;
    
//         while (blockStart < endOfDay) {
//           const blockEnd = new Date(blockStart.getTime() + duration * 60000);
    
//           // Check if this time block is free
//           const isFree = allBusyTimes.every(bt => blockEnd <= bt.startTime || blockStart >= bt.endTime);
    
//           if (isFree) {
//             return { startTime: blockStart, endTime: blockEnd };
//           }
    
//           // Move to the next time block
//           blockStart = new Date(blockStart.getTime() + timeBlock);
//         }
    
//         return null; // No available time slot found
//       };
    
//       const removeGoal = (goalId) => {
//         setSelectedGoals(prevGoals => prevGoals.filter(goal => goal.id !== goalId));
//       };
    
//       const saveGoals = async () => {
//         const formattedDate = formatDateForStorage(new Date(date));
//         const existingGoals = await AsyncStorage.getItem(formattedDate);
//         const updatedGoals = existingGoals ? JSON.parse(existingGoals) : [];
    
//         const finalGoals = [...updatedGoals, ...selectedGoals];
//         await AsyncStorage.setItem(formattedDate, JSON.stringify(finalGoals));