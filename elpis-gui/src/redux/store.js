import { applyMiddleware, createStore, combineReducers } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import dataset from './datasetReducer';
import pronDict from './pronDictReducer';
import model from './modelReducer';
import transcription from './transcriptionReducer';
import steps from './stepReducer';
import thunk from 'redux-thunk';

const appReducer = combineReducers({
    dataset,
    pronDict,
    model,
    transcription,
    steps
});


const rootReducer = (state, action) => {
    if (action.type == 'CONFIG_RESET') {
        console.log("doing reset")
        state = undefined
    }
    return appReducer(state, action)
}


const store = createStore(rootReducer,
    composeWithDevTools(applyMiddleware(thunk))
);
export default store;