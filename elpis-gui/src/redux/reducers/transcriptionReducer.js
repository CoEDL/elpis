import * as actionTypes from '../actionTypes/transcriptionActionTypes';

const initState = {
    filename: null,
    status: 'ready',
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

        // after uploading the file
        case 'TRANSCRIPTION_PREPARE':
            return {
                ...state,
                status: action.response.data.data,
            }

        case 'TRANSCRIPTION_STATUS':
            return {
                ...state,
                status: action.response.data.data
            }

        case 'TRANSCRIPTION_STATUS_RESET':
            return {
                ...state,
                status: 'ready',
                text: null,
                elan: null
            }


        case 'TRANSCRIPTION_GET_TEXT':
            return {
                ...state,
                text: action.response.data
            }

        case 'TRANSCRIPTION_GET_ELAN':
            return {
                ...state,
                elan: action.response.data
            }

        default:
            return state;
    }
}

export default transcription;