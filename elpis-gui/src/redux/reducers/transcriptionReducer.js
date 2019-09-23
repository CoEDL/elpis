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
            console.log("reducer got new transcription", action)
            var { originalFilename } = action.payload.data.data
            console.log("originalFilename", originalFilename)
            return { ...initState, filename: originalFilename }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_STARTED:
            console.log("reducer got transcribe started")
            return {
                ...state,
                type: 'text',
                status: 'transcribing'
            }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_STARTED:
            console.log("reducer got transcribe align started")
            return {
                ...state,
                type: 'elan',
                status: 'transcribing'
            }


        case actionTypes.TRANSCRIPTION_TRANSCRIBE_SUCCESS:
            console.log("reducer got transcribe success", action)
            var { status, type } = action.payload.data.data
            return { ...state, status, type }

        case actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_SUCCESS:
            console.log("reducer got transcribe align success", action)
            var { status, type } = action.payload.data.data
            return { ...state, status, type }

        case actionTypes.TRANSCRIPTION_STATUS_SUCCESS:
            console.log("reducer got transcription status", action)
            var { status, type } = action.payload.data.data
            return { ...state, status, type }


        case actionTypes.TRANSCRIPTION_GET_TEXT_SUCCESS:
            console.log("reducer got transcription text", action)
            // TODO: do this on the backend
            var text = action.payload.data
            text = text.split(' ').slice(1).join(' ')
            return { ...state, text }

        case actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS:
            console.log("reducer got transcription elan", action)
            return {
                ...state,
                elan: action.payload.data
            }

        // // after uploading the file
        // case 'TRANSCRIPTION_PREPARE':
        //     return {
        //         ...state,
        //         status: action.response.data.data,
        //     }


        case 'TRANSCRIPTION_STATUS_RESET':
            return { ...initState }


        default:
            return state;
    }
}

export default transcription;