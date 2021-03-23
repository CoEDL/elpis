import { applyMiddleware, createStore, combineReducers } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";
import config from "./reducers/configReducer";
import dataset from "./reducers/datasetReducer";
import engine from "./reducers/engineReducer";
import model from "./reducers/modelReducer";
import pronDict from "./reducers/pronDictReducer";
import sideNav from "./reducers/sideNavReducer";
import transcription from "./reducers/transcriptionReducer";
import thunk from "redux-thunk";

const appReducer = combineReducers({
    config,
    dataset,
    engine,
    model,
    pronDict,
    sideNav,
    transcription,
});

// hard reset
const rootReducer = (state, action) => {
    if (action.type == "CONFIG_RESET") {
        state = undefined;
    }
    return appReducer(state, action);
};


const store = createStore(rootReducer,
    composeWithDevTools(applyMiddleware(thunk))
);
export default store;
