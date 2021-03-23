/* eslint-disable max-len */
import * as actionTypes from "../actionTypes/appActionTypes";
import urls from "urls";

// For convenience while developing, set this true
// false will make the menus collapse
const enableAll = true;

// Define a total ordering on the steps.
const stepOrderDefinition = [
	"engine",
	"recordings",
	"pronunciation",
	"train",
	"transcribe",
];

export function stepToOrder(stepName) {
	return stepOrderDefinition.findIndex(v => v === stepName);
}

// Get the name of the next step according to the stepOrderDefinition variable.
function getNextStepName(stepName, engine) {
	if (stepName === null) return null;

	let stepIndex = stepToOrder(stepName);

	// if current step is not in the list
	if (stepIndex === -1) {
		throw "stepName: " + stepName + " is not in the stepOrderDefinition list.";
	}

	// if there is no next step
	if (stepIndex === stepOrderDefinition.length - 1) {
		return null;
	}

	let nextStepName = stepOrderDefinition[stepIndex + 1];

	// if non-kaldi engine, then skip 'pronunciation'
	if (engine !== "kaldi" && nextStepName === "pronunciation") {
		nextStepName = getNextStepName(nextStepName);
	}

	return nextStepName;
}

const initialStepModelState = {
	engine: null,
	lastURL: null,
	steps: {
		recordings: {
			substeps: [
				{done: false, doing: false, enabled: false, title: "navigation.recordings.title", path: urls.gui.dataset.index},
				{done: false, doing: false, enabled: false, title: "navigation.recordings.files", path: urls.gui.dataset.files},
				{done: false, doing: false, enabled: false, title: "navigation.recordings.wordlist", path: urls.gui.dataset.prepare},
			],
			engine_specific: null,
		},
		pronunciation: {
			substeps: [
				{done: false, doing: false, enabled: false, title: "navigation.pronunciation.title", path: urls.gui.pronDict.index},
				{done: false, doing: false, enabled: false, title: "navigation.pronunciation.letterToSound", path: urls.gui.pronDict.l2s},
				{done: false, doing: false, enabled: false, title: "navigation.pronunciation.dictionary", path: urls.gui.pronDict.lexicon},
			],
			engine_specific: "kaldi",
		},
		train: {
			substeps: [
				{done: false, doing: false, enabled: false, title: "navigation.training.title", path: urls.gui.model.index},
				{done: false, doing: false, enabled: false, title: "navigation.training.settings", path: urls.gui.model.settings},
				{done: false, doing: false, enabled: false, title: "navigation.training.train", path: urls.gui.model.train},
				{done: false, doing: false, enabled: false, title: "navigation.training.results", path: urls.gui.model.results},
			],
			engine_specific: null,
		},
		transcribe: {
			substeps: [
				{done: false, doing: false, enabled: false, title: "navigation.transcriptions.title", path: urls.gui.transcription.new},
			],
			engine_specific: null,
		},
	},
};

const sideNav = (state = initialStepModelState, action) => {
	switch (action.type) {
		case actionTypes.ENGINE_LOAD_SUCCESS: {
			let engine = action.response.data.data.engine;

			// TODO dispatch the set current step action after engine load
			// used to fall through the case but that's not allowed now

			return {...state, engine};
		}

		case actionTypes.APP_SET_CURRENT_STEP: {
			let currentSubStepIndex = 0;
			let currentStepName = null;
			// Make a copy of the original steps as to not override the initial steps.
			let originalStepsState = Object.assign({}, initialStepModelState);

			// Used to enable next groups of steps if user is on last substep
			let rememberToEnableTheNextStep = false;

			// Iterate through main steps
			for (let [stepName, step] of Object.entries(originalStepsState.steps)) {
				step.substeps.forEach((substep, i) => {
					// model/new type pages aren't represented in the substeps, so match them to the first in each step
					const searchReg = /\/new|\//ig;
					const path_match = (window.location.pathname.replace(searchReg,"") === substep.path.replace(searchReg,"")) ? 1 : 0;

					if (path_match){
						// Found the current step!
						currentStepName = stepName;
						currentSubStepIndex = i;
					}
				});
			}

			let rebuiltSteps = {};

			Object.entries(originalStepsState.steps).forEach(([stepName, step]) => {
				// Determine this steps situation.
				let isPastStep = stepToOrder(stepName) < stepToOrder(currentStepName);
				let isCurrentStep = stepToOrder(stepName) === stepToOrder(currentStepName);
				let isFutureStep = stepToOrder(stepName) > stepToOrder(currentStepName);

				// Determine whether step is to be kept based on selected engine.
				if (step.engine_specific !== null && step.engine_specific !== state.engine) {
					// The engine has been specified and this step does not belong to this engine.
					return; // Skip construction step.
				}

				step.substeps.forEach((substep, i) => {
					// reset all
					substep.done = false;
					substep.doing = false;
					substep.enabled = false;

					// Determine the substep situation
					let isPastSubStep = i < currentSubStepIndex;
					let isCurrentSubStep = i === currentSubStepIndex;
					let isNextSubStep = i === currentSubStepIndex + 1;
					let isLastSubStep = i === currentSubStepIndex - 1;

					// previous
					if (isPastStep || (isCurrentStep && isPastSubStep)) {
						step.done = true;
						substep.done = true;
						step.enabled = true;
						substep.enabled = true;
					}

					// this one
					if (isCurrentStep) {
						step.doing = true;
						step.enabled = true;
					}

					// this one
					if (isCurrentStep && isCurrentSubStep) {
						substep.doing = true;
						substep.enabled = true;
					}

					// next one
					if (isCurrentStep && isNextSubStep) {
						substep.enabled = true;
					}

					// also enable first substeps in next step if we are on the last substep in a step
					if (isCurrentStep && isCurrentSubStep && isLastSubStep) {
						rememberToEnableTheNextStep = true;
					}

					// future steps
					if (isFutureStep) {
						step.enabled = false;
					}

					// For developer convenience...
					if (enableAll) substep.enabled = true;
				});

				// add step to the rebuilt steps
				rebuiltSteps[stepName] = step;
			});


			let nextStepName = getNextStepName(currentStepName, state.engine);

			if (rememberToEnableTheNextStep && nextStepName) {
				rebuiltSteps[nextStepName].substeps[0].enabled = true;
			}

			return {...state, steps: rebuiltSteps, lastURL: action.url};
		}
		default:
			return {...state};
	}
};
export default sideNav;
