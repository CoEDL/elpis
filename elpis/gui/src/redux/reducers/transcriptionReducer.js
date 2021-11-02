import * as actionTypes from "../actionTypes/transcriptionActionTypes";

const initState = {
    filename: null,
    status: "ready",
    stage_status: null,
    type: null,
    text: null,
    elan: null,
    confidence: null,
    audio_filename: null,
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
            var {audio_filename, text} = action.response.data.data;

            return {...state, audio_filename, text};

        case actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS:
            // The response here is the file data, not wrapped in a JSON data/status format
            return {...state, elan: action.response.data};

        case actionTypes.TRANSCRIPTION_GET_CONFIDENCE_SUCCESS:
            var {confidence} = action.response.data.data;

            return {...state, confidence: confidence};

        default:
            return {...state};
    }
};

export default transcription;
