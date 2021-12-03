import * as actionTypes from "../actionTypes/transcriptionActionTypes";

const initState = {
    filename: null,
    status: "ready",
    stage_status: null,
    type: null,
    text: null,
    elan: null,
    confidence: null,
};
const transcription = (state = initState, action) => {
    switch (action.type) {
        case actionTypes.TRANSCRIPTION_NEW_SUCCESS:
            var {originalFilename} = action.response.data.data;

            return {...initState, filename: originalFilename};

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_STARTED:
            return {
                ...state,
                type: "text",
                status: "transcribing",
            };

        case actionTypes.TRANSCRIPTION_STATUS_SUCCESS:
            var {status, stage_status, type} = action.response.data.data;

            return {...state, status, stage_status, type};

        case actionTypes.TRANSCRIPTION_GET_TEXT_SUCCESS:
            return {...state, text: action.response.data.data.text};

        case actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS:
            return {...state, elan: action.response.data.data.elan};

        case actionTypes.TRANSCRIPTION_GET_CONFIDENCE_SUCCESS:
            var {confidence} = action.response.data.data;

            return {...state, confidence: confidence};

        default:
            return {...state};
    }
};

export default transcription;
