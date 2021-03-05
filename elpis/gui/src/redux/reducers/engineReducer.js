import * as actionTypes from '../actionTypes/appActionTypes';
import urls from 'urls'

const initialEngineState = {
    engine: null,
    engine_list: [],
    engine_human_names: {"kaldi": "word", "espnet":"phoneme"}
}
const engine = (state = initialEngineState, action) => {
	switch (action.type) {
		case actionTypes.ENGINE_LOAD_STARTED:
		case actionTypes.ENGINE_LOAD_FAILURE:
		case actionTypes.ENGINE_LIST_STARTED:
		case actionTypes.ENGINE_LIST_FAILURE:
			return {...state}

		case actionTypes.ENGINE_LIST_SUCCESS:
			let engine_list = action.response.data.data.engine_list;
			console.log("engine_list", engine_list)
			return { ...state, engine_list };

		case actionTypes.ENGINE_LOAD_SUCCESS:
			let engine = action.response.data.data.engine;
			return { ...state, engine };

		default:
			return { ...state }
	}

}
export default engine;