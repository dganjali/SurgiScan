import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';

import DashboardScreen from './src/screens/DashboardScreen';
import EmergencyScreen from './src/screens/EmergencyScreen';
import LogsScreen from './src/screens/LogsScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <StatusBar style="auto" />
        <Stack.Navigator 
          initialRouteName="Dashboard"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#1e3a8a',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Dashboard" 
            component={DashboardScreen}
            options={{ title: 'Code Blue System' }}
          />
          <Stack.Screen 
            name="Emergency" 
            component={EmergencyScreen}
            options={{ title: 'Emergency Active' }}
          />
          <Stack.Screen 
            name="Logs" 
            component={LogsScreen}
            options={{ title: 'Event Logs' }}
          />
          <Stack.Screen 
            name="Settings" 
            component={SettingsScreen}
            options={{ title: 'Settings' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
} 