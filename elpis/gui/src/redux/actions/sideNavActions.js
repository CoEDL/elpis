import * as actionTypes from "../actionTypes/appActionTypes";

export const setCurrentStep = url => ({
    type: actionTypes.APP_SET_CURRENT_STEP,
    url,
});
