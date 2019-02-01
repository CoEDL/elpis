// For convenience while developing, set this true
// false will make the menus collapse
const enableAll = true

const initialStepModelState = {
    currentStep: [0, 0],
    steps: [
        {
            title: "Step 1 Data Preparation",
            path: "/naming",
            icon: "wrench",
            done: false, doing: false, enabled: true,
            substeps: [
                { done: false, doing: false, enabled: false, title: "Name the model", path: "/naming" },
                { done: false, doing: false, enabled: false, title: "Add data", path: "/add-data" },
                { done: false, doing: false, enabled: false, title: "Data preparation", path: "/data-preparation" },
                { done: false, doing: false, enabled: false, title: "Pronunciation dictionary", path: "/build-pronunciation-dictionary" },
            ]
        },
        {
            title: "Step 2 Model Building",
            path: "/model-settings",
            icon: "lemon",
            done: false, doing: false, enabled: false,
            substeps: [
                { done: false, doing: false, enabled: false, title: "Model settings", path: "/model-settings" },
                { done: false, doing: false, enabled: false, title: "Model Training", path: "/training-model" },
                { done: false, doing: false, enabled: false, title: "Trained Model Success", path: "/training-success" },
            ]
        },
        {
            title: "Step 3 New transcription",
            path: "/new-transcription",
            icon: "microphone",
            done: false, doing: false, enabled: false,
            substeps: [
                { done: false, doing: false, enabled: false, title: "Choose model", path: "/new-transcription" },
                { done: false, doing: false, enabled: false, title: "Transcribe", path: "/transcription-results" },
            ]
        }
    ]
}

const stepReducer = (state = initialStepModelState, action) => {
    let newSteps = []
    let currentIndex = []

    switch (action.type) {

        // Set the 'doing' status by matching URL
        case 'SET_CURRENT_STEP':
            let rememberToEnableTheNextStep = false
            let enabledStepIndex = null
            console.log('.......')
            // Track down which is the current substep by matching path to URL
            state.steps.forEach((step, i) => {
                step.substeps.forEach((substep, j) => {
                    if (action.urlParams.includes(substep.path.replace(/^\/|\/$/g, ''))) {
                        currentIndex = [i, j]
                    }
                })
            })
            console.log('current index', currentIndex)

            newSteps = state.steps.map((step, i) => {

                step.substeps.map((substep, j) => {
                    console.log(i, j, currentIndex[1])
                    // reset all
                    substep.done = false
                    substep.doing = false
                    substep.enabled = false

                    let isPastStep       = (i < currentIndex[0]) ? true : false
                    let isCurrentStep    = (i === currentIndex[0]) ? true : false
                    let isFutureStep     = (i > currentIndex[0]) ? true : false
                    let isPastSubStep    = (j < currentIndex[1]) ? true : false

                    let isCurrentSubStep = (j === currentIndex[1]) ? true : false
                    let isNextSubStep    = (j === currentIndex[1] + 1) ? true : false
                    let isLastSubStep    = (j === step.substeps.length - 1) ? true : false
                    let isFutureSubStep  = (j > currentIndex[1]) ? true : false

                    // previous
                    if (isPastStep || (isCurrentStep && isPastSubStep)) {
                        substep.enabled = true
                        substep.done = true
                    }
                    // this one
                    if (isCurrentStep && isCurrentSubStep) {
                        substep.enabled = true
                        substep.doing = true
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
                    if (enableAll)  substep.enabled = true

                    return substep
                })

                // For further developer convenience...
                if (enableAll) step.enabled = true

                return step
            })

            if (rememberToEnableTheNextStep && newSteps[currentIndex[0]+1]) {
                newSteps[currentIndex[0]+1].enabled = true
                newSteps[currentIndex[0]+1].substeps[0].enabled = true
            }

            return { steps: newSteps }

        default:
            return state
    }
}
export default stepReducer;
