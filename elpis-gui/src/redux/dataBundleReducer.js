import {getFileExtension} from 'helpers'

const initState = {
    name: "",
    dataBundleList: [],
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    settings: {
        tier: 'Phrase'
    },
    wordlist: {
        amakaang: 2,
        di: 2,
        hada: 2,
        kaai: 2,
        muila: 2
    }
}


const dataBundle = (state = initState, action) => {
    switch (action.type) {

        case 'DATA_BUNDLE_LIST':
        console.log("reducer got data bundle list", action.response.data.data)
            return {
                ...state,
                dataBundleList: action.response.data.data
            }

        case 'DATA_BUNDLE_LOAD':
        case 'DATA_BUNDLE_NEW':
            console.log("reducer got data bundle new or load", action.response.data)
            return {
                ...state,
                name: action.response.data.data.name
            }

        case 'DATA_BUNDLE_NAME':
            return {
                ...state,
                name: action.response.data.data.name
            }

        case 'DATA_BUNDLE_FILES':
            // action.data is an array of filenames
            // parse this, split into separate lists
            let audioFiles = action.response.data.filter(file => getFileExtension(file) === 'wav')
            let transcriptionFiles = action.response.data.filter(file => getFileExtension(file) === 'eaf')
            let additionalTextFiles = action.response.data.filter(file => getFileExtension(file) === 'txt')

            audioFiles.sort()
            transcriptionFiles.sort()
            additionalTextFiles.sort()

            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];
            return {
                ...state,
                audioFiles,
                transcriptionFiles,
                additionalTextFiles
            }

        case 'DATA_BUNDLE_SETTINGS':
            // watch out for response.data.data ...
            return {
                ...state,
                settings: {...state.settings, tier: action.response.data.data.tier}
            }

        case 'DATA_BUNDLE_PREPARE':
            console.log("wordlist", action.response.data)
            return {
                ...state,
                wordlist: action.response.data
            }

        default:
            return state;
    }
}

export default dataBundle;