import * as actionTypes from '../actionTypes/transcriptionActionTypes';

const initState = {
    filename: null,
    status: 'ready',
    type: null,
    text: null,
    elan: null
}

const transcription = (state = initState, action) => {

    switch (action.type) {

        case actionTypes.TRANSCRIPTION_NEW_SUCCESS:
            var { originalFilename } = action.response.data.data
            return { ...initState, filename: originalFilename }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_STARTED:
            return {
                ...state,
                type: 'text',
                status: 'transcribing'
            }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_STARTED:
            return {
                ...state,
                type: 'elan',
                status: 'transcribing'
            }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_SUCCESS:
            var { status, type } = action.response.data.data
            return { ...state, status, type }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_SUCCESS:
            var { status, type } = action.response.data.data
            return { ...state, status, type }

        case actionTypes.TRANSCRIPTION_STATUS_SUCCESS:
            var { status, type } = action.response.data.data
            return { ...state, status, type }

        case actionTypes.TRANSCRIPTION_GET_TEXT_SUCCESS:
            // TODO: do this on the backend
            var text = action.response.data
            text = text.split(' ').slice(1).join(' ')
            return { ...state, text }

        case actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS:
            return {
                ...state,
                elan: action.response.data
            }

            default:
            return state;
    }
}

export default transcription;