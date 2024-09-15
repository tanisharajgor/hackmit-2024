import * as React from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { View } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';


// Screens
import HomeScreen from './screens/Home';
import QuestionScreen from './screens/Interact';
import ProfileScreen from './screens/Vocab';
import PredictionScreen from './screens/Profile'


// Screen names --- MAY BE WORTH CONSIDERING REMOVING INFO TAB (not needed for this)
const homeName = 'Home';
const detailsName = 'Interact';
const infoName = 'Info';
const profileName = 'Vocab';
const predictionName = 'Profile'


const Tab = createBottomTabNavigator();


const MyTheme = {
 ...DefaultTheme,
 colors: {
   ...DefaultTheme.colors,
   background: '#181c38'
 },
};


export default function MainContainer() {
 return (
   <NavigationContainer theme={MyTheme}>
     <Tab.Navigator
       initialRouteName={homeName}
       screenOptions={({ route }) => ({
         tabBarIcon: ({ focused, color, size }) => {
           let iconName;
           let rn = route.name;


           if (rn === homeName) {
             iconName = focused ? 'home' : 'home-outline';
           } else if (rn === detailsName) {
             iconName = focused ? 'camera' : 'camera-outline';
           } else if (rn === infoName) {
             iconName = focused ? 'search' : 'search-outline';
           } else if (rn === profileName) {
             iconName = focused ? 'book' : 'book-outline';
           } else if (rn === predictionName) {
             iconName = focused ? 'person' : 'person-outline';
           }


           // You can return any component that you like here!
           return <Ionicons name={iconName} size={size} color={color} />;
         },
         tabBarStyle: {
           backgroundColor: '#303452ff',
         },
       })}
       tabBarOptions={{
         activeTintColor: '#ff84a5',
         inactiveTintColor: 'white',
         labelStyle: { paddingBottom: 5, fontSize: 10, color: 'white'},
         style: { padding: 10, height: 70},
       }}>
       <Tab.Screen name={homeName} component={HomeScreen}/>
       <Tab.Screen name={detailsName} component={QuestionScreen} />
       <Tab.Screen name={profileName} component={ProfileScreen} />
       <Tab.Screen name={predictionName} component={PredictionScreen} />
     </Tab.Navigator>
   </NavigationContainer>
 );
}
