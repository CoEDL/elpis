const toyLexicon = `!SIL sil
<UNK> spn
di d I
kaai k a: I
amakaang a m a k a: ŋ
hada h a d a
muila m u I l a
`;

const initState = {
    pronDictList: [],
    name: '',
    dataBundleName: '',
    date: null,
    l2s: '',
    lexicon: '',
    apiWaiting: {status: false, message: 'something'}
}

const pronDict = (state = initState, action) => {
    switch (action.type) {

        case 'TRIGGER_API_WAITING':
            return {
                ...state,
                apiWaiting: {status: true, message: action.message}
            }


        case 'PRON_DICT_LIST':
            console.log("reducer got pron dict list", action.response.data)
            return {
                ...state,
                pronDictList: action.response.data.data
            }

        case 'PRON_DICT_LOAD':
        case 'PRON_DICT_NEW':
            console.log("name", action.response.data.data.name)
            console.log("reducer got pron dict new or load", action.response.data)
            return {
                ...state,
                name: action.response.data.data.config.name,
                dataBundleName: action.response.data.data.config.dataset_name,
                l2s: action.response.data.data.l2s,
                lexicon: 'No lexicon yet'
            }

        case 'PRON_DICT_NAME':
            console.log("reducer got pron dict name", action.response.data)
            return {
                    ...state,
                    name: action.response.data.data.name
                }

        case 'PRON_DICT_L2S':
            console.log("reducer got l2s", action)
            return {
                ...state,
                l2s: action.response.data
            }

        case 'PRON_DICT_LEXICON':
            console.log("reducer got lexicon", action.response.data)
            return {
                ...state,
                lexicon: action.response.data
            }

        default:
            return state;
    }
}

export default pronDict;