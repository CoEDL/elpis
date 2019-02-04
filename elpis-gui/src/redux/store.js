// import { applyMiddleware, createStore } from 'redux'
// import { persistStore, persistReducer } from 'redux-persist'
// import storage from 'redux-persist/lib/storage' // defaults to localStorage for web and AsyncStorage for react-native
// import thunk from 'redux-thunk'
// import {
//     apiReducer,
//     stepReducer,
// } from './reducer'

// // const persistConfig = {
// //   key: 'root',
// //   storage,
// // }

// // const persistedReducer = persistReducer(persistConfig, rootReducer)
// // export const store = createStore(
// //   persistedReducer,
// //   composeWithDevTools(applyMiddleware(thunk))
// // )
// // export const persistor = persistStore(store)


import { applyMiddleware, createStore, combineReducers } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import model from './apiModelReducer';
import steps from './stepReducer';
import thunk from 'redux-thunk';

const rootReducer = combineReducers({
    model,
    steps,
});

const store = createStore(rootReducer,
    composeWithDevTools(applyMiddleware(thunk))
);
export default store;