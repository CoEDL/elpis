// import { applyMiddleware, createStore } from 'redux'
// import { composeWithDevTools } from 'redux-devtools-extension'
// import { persistStore, persistReducer } from 'redux-persist'
// import storage from 'redux-persist/lib/storage' // defaults to localStorage for web and AsyncStorage for react-native
// import thunk from 'redux-thunk'
// import rootReducer from './reducer'

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

// const store = createStore(rootReducer, 
//     window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
// );
// export default store;