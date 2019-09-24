import { applyMiddleware, createStore, combineReducers } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import sideNav from './reducers/sideNavReducer';
import dataset from './reducers/datasetReducer';
import pronDict from './reducers/pronDictReducer';
import model from './reducers/modelReducer';
import transcription from './reducers/transcriptionReducer';
import thunk from 'redux-thunk';

const appReducer = combineReducers({
    sideNav,
    dataset,
    pronDict,
    model,
    transcription
});

// hard reset
const rootReducer = (state, action) => {
    if (action.type == 'CONFIG_RESET') {
        state = undefined
    }
    return appReducer(state, action)
}


const store = createStore(rootReducer,
    composeWithDevTools(applyMiddleware(thunk))
);
export default store;