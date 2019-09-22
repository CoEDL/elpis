import urls from 'urls'

// For convenience while developing, set this true
// false will make the menus collapse
const enableAll = true

const initialStepModelState = {
	currentStep: [0, 0],
	steps: [
		{
			title: "Step 1 Recordings",
			path: urls.gui.dataset.index,
			done: false, doing: false, enabled: true,
			substeps: [
				{ done: false, doing: false, enabled: false, title: "Add files", path: urls.gui.dataset.files },
				{ done: false, doing: false, enabled: false, title: "Prepare", path: urls.gui.dataset.prepare }
			]
		},
		{
			title: "Step 2 Pronunciation Dictionary",
			path: urls.gui.pronDict.index,
			done: false, doing: false, enabled: false,
			substeps: [
				{ done: false, doing: false, enabled: false, title: "Letter to sound", path: urls.gui.pronDict.l2s },
				{ done: false, doing: false, enabled: false, title: "Pronunciation", path: urls.gui.pronDict.lexicon }
			]
		},
		{
			title: "Step 3 Training",
			path: urls.gui.model.index,
			done: false, doing: false, enabled: false,
			substeps: [
				{ done: false, doing: false, enabled: false, title: "Settings", path: urls.gui.model.settings },
				{ done: false, doing: false, enabled: false, title: "Training", path: urls.gui.model.train },
				{ done: false, doing: false, enabled: false, title: "Results", path: urls.gui.model.results },
			]
		},
		{
			title: "Step 4 New transcriptions",
			path: urls.gui.transcription.new,
			done: false, doing: false, enabled: false,
			substeps: [
				{ done: false, doing: false, enabled: false, title: "Transcribe", path: urls.gui.transcription.new }
			]
		}
	]
}

const steps = (state = initialStepModelState, action) => {
	let newSteps = []
	let currentIndex = []

	switch (action.type) {

		// Set the 'doing' status by matching URL
		case 'SET_CURRENT_STEP':
			let rememberToEnableTheNextStep = false
			// Track down which is the current substep by matching path to URL
			// Split the url into parts, remove the first / to avoid empty first item in array
			let urls_params = action.url.slice(1, action.url.length).split("/")

			state.steps.forEach((step, i) => {
				// watch out for leading / in step.path. remove it for comparison
				if (urls_params[0] === step.path.slice(1)) {
					currentIndex = [i, null]
				}
				step.substeps.forEach((substep, j) => {
					if (action.url === substep.path) {
						currentIndex = [i, j]
					}
				})
			})

			newSteps = state.steps.map((step, i) => {
				// reset all
				step.done = false
				step.doing = false
				step.enabled = false

				let isPastStep = (i < currentIndex[0]) ? true : false
				let isCurrentStep = (i === currentIndex[0]) ? true : false
				let isFutureStep = (i > currentIndex[0]) ? true : false

				step.substeps.map((substep, j) => {

					// reset all
					substep.done = false
					substep.doing = false
					substep.enabled = false

					let isPastSubStep = (j < currentIndex[1]) ? true : false
					let isCurrentSubStep = (j === currentIndex[1]) ? true : false
					let isNextSubStep = (j === currentIndex[1] + 1) ? true : false
					let isLastSubStep = (j === step.substeps.length - 1) ? true : false
					// let isFutureSubStep  = (j > currentIndex[1]) ? true : false

					// previous
					if (isPastStep || (isCurrentStep && isPastSubStep)) {
						step.done = true
						substep.done = true
						step.enabled = true
						substep.enabled = true
					}
					// this one
					if (isCurrentStep) {
						step.doing = true
						step.enabled = true
					}
					// this one
					if (isCurrentStep && isCurrentSubStep) {
						substep.doing = true
						substep.enabled = true
					}
					// next one
					if (isCurrentStep && isNextSubStep) {
						substep.enabled = true
					}
					// also enable first substeps in next step if we are on the last substep in a step
					if (isCurrentStep && isCurrentSubStep && isLastSubStep) {
						rememberToEnableTheNextStep = true
					}
					// future steps
					if (isFutureStep) {
						step.enabled = false
					}

					// For developer convenience...
					if (enableAll) substep.enabled = true

					return substep
				})

				// For further developer convenience...
				if (enableAll) step.enabled = true

				return step
			})

			if (rememberToEnableTheNextStep && newSteps[currentIndex[0] + 1]) {
				newSteps[currentIndex[0] + 1].enabled = true
				newSteps[currentIndex[0] + 1].substeps[0].enabled = true
			}

			return { steps: newSteps }

		default:
			return state
	}
}
export default steps;
