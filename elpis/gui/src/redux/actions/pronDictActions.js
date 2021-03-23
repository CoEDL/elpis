import axios from 'axios';
import urls from 'urls';

import * as actionTypes from '../actionTypes/pronDictActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host;


/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

export function pronDictNew(postData) {
    const url = baseUrl + urls.api.pronDict.new;
    var responseData;
    return async dispatch => {
        dispatch(pronDictNewStarted());
        await axios.post(url, postData)
            .then( response => {
                responseData = response.data;
                dispatch(pronDictNewSuccess(response));
            })
            .catch( error => {
                dispatch(pronDictNewFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictNewStarted = () => ({
    type: actionTypes.PRON_DICT_NEW_STARTED
});
const pronDictNewSuccess = response => ({
    type: actionTypes.PRON_DICT_NEW_SUCCESS,
    response: { ...response }
});
const pronDictNewFailure = error => ({
    type: actionTypes.PRON_DICT_NEW_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */

export function pronDictLoad(postData) {
    const url = baseUrl + urls.api.pronDict.load;
    var responseData;
    return async dispatch => {
        dispatch(pronDictLoadStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(pronDictLoadSuccess(response));
            })
            .catch(error => {
                dispatch(pronDictLoadFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictLoadStarted = () => ({
    type: actionTypes.PRON_DICT_LOAD_STARTED
});
const pronDictLoadSuccess = response => ({
    type: actionTypes.PRON_DICT_LOAD_SUCCESS,
    response: { ...response }
});
const pronDictLoadFailure = error => ({
    type: actionTypes.PRON_DICT_LOAD_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  LIST * * * * * * * * * * *  */

export function pronDictList() {
    const url = baseUrl + urls.api.pronDict.list;
    var responseData;
    return async dispatch => {
        dispatch(pronDictListStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(pronDictListSuccess(response));
            })
            .catch(error => {
                dispatch(pronDictListFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictListStarted = () => ({
    type: actionTypes.PRON_DICT_LIST_STARTED
});
const pronDictListSuccess = response => ({
    type: actionTypes.PRON_DICT_LIST_SUCCESS,
    response: { ...response }
});
const pronDictListFailure = error => ({
    type: actionTypes.PRON_DICT_LIST_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  L2S * * * * * * * * * * *  */

export function pronDictL2S(postData) {
    const url = baseUrl + urls.api.pronDict.l2s;
    const config = { headers: { 'content-type': 'multipart/form-data' } };
    var responseData;
    return async dispatch => {
        dispatch(pronDictL2SStarted());
        await axios.post(url, postData, config)
            .then(response => {
                responseData = response.data;
                dispatch(pronDictL2SSuccess(response));
            })
            .catch(error => {
                dispatch(pronDictL2SFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictL2SStarted = () => ({
    type: actionTypes.PRON_DICT_L2S_STARTED
});
const pronDictL2SSuccess = response => ({
    type: actionTypes.PRON_DICT_L2S_SUCCESS,
    response: { ...response }
});
const pronDictL2SFailure = error => ({
    type: actionTypes.PRON_DICT_L2S_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  BUILD LEXICON * * * * * * * * * * *  */

export function pronDictBuildLexicon() {
    const url = baseUrl + urls.api.pronDict.generateLexicon;
    var responseData;
    return async dispatch => {
        dispatch(pronDictBuildLexiconStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(pronDictBuildLexiconSuccess(response));
            })
            .catch(error => {
                dispatch(pronDictBuildLexiconFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictBuildLexiconStarted = () => ({
    type: actionTypes.PRON_DICT_BUILD_LEXICON_STARTED
});
const pronDictBuildLexiconSuccess = response => ({
    type: actionTypes.PRON_DICT_BUILD_LEXICON_SUCCESS,
    response: { ...response }
});
const pronDictBuildLexiconFailure = error => ({
    type: actionTypes.PRON_DICT_BUILD_LEXICON_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  SAVE LEXICON * * * * * * * * * * *  */

export function pronDictSaveLexicon(postData) {
    const url = baseUrl + urls.api.pronDict.saveLexicon;
    var responseData;
    return async dispatch => {
        dispatch(pronDictSaveLexiconStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(pronDictSaveLexiconSuccess(response));
            })
            .catch(error => {
                dispatch(pronDictSaveLexiconFailure(error));
                throw error;
            });
        return responseData;
    };
}

const pronDictSaveLexiconStarted = () => ({
    type: actionTypes.PRON_DICT_SAVE_LEXICON_STARTED
});
const pronDictSaveLexiconSuccess = response => ({
    type: actionTypes.PRON_DICT_SAVE_LEXICON_SUCCESS,
    response: { ...response }
});
const pronDictSaveLexiconFailure = error => ({
    type: actionTypes.PRON_DICT_SAVE_LEXICON_FAILURE,
    response: { error }
});


/* * * * * * * * * * * *  UPDATE LEXICON * * * * * * * * * * *  */

export const pronDictUpdateLexicon = data => ({
    type: actionTypes.PRON_DICT_UPDATE_LEXICON,
    data
});
