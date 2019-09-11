import { applyMiddleware, createStore, combineReducers } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import dataset from './datasetReducer';
import pronDict from './pronDictReducer';
import model from './modelReducer';
import transcription from './transcriptionReducer';
import steps from './stepReducer';
import thunk from 'redux-thunk';

const rootReducer = combineReducers({
    dataset,
    pronDict,
    model,
    transcription,
    steps
});

const store = createStore(rootReducer,
    composeWithDevTools(applyMiddleware(thunk))
);
export default store;