const initialStepModelState = {
    steps: [
        {
            title: "Step 1 Data Preparation",
            path: "/naming",
            icon: "wrench",
            done: false, doing: false, enabled: true,
            substeps: [
                { done: true, doing: false, enabled: true, title: "Name the model", path: "/naming" },
                { done: true, doing: false, enabled: true, title: "Add data", path: "/add-data" },
                { done: true, doing: true, enabled: true, title: "Data preparation", path: "/data-preparation" },
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
                { done: false, doing: false, enabled: false, title: "Input data", path: "/input-data" },
                { done: false, doing: false, enabled: false, title: "Transcribe", path: "/transcribe" },
            ]
        }
    ]
}

const stepReducer = (state = initialStepModelState, action) => {
    let newSteps = []

    switch (action.type) {

        // set the 'doing' status by matching URL
        case 'SET_STEP_DOING':
            newSteps = state.steps.map((step, i) => {
                step.doing = false
                step.substeps.map((substep, j) => {
                    substep.doing = false
                    if (action.urlParams.includes(substep.path.replace(/^\/|\/$/g, ''))) {
                        step.doing = true
                        substep.doing = true
                    }
                    return substep
                })
                return step
            })
            return { steps: newSteps }


        case 'SET_CURRENT_STEP_DONE':
            newSteps = state.steps.map((step, i) => {
                step.substeps.map((substep, j) => {
                    if (substep.doing) {
                        substep.done = true
                    }
                    return substep
                })
                return step
            })
            return { steps: newSteps }

        case 'ENABLE_NEXT_STEP':
            let rememberToEnableTheNextStep = false
            let enabledStepIndex = null

            newSteps = state.steps.map((step, i) => {
                step.substeps.map((substep, j) => {
                    if (substep === action.step) {
                        // Set the enabled status of the next substep after the one we are going to
                        // But if its the last substep in a group,
                        // store the index of the current step
                        // and update the next step after we are done
                        if (j+1 < step.substeps.length) {
                            step.substeps[j + 1].enabled = true
                        }
                        else if (i+1 < state.steps.length) {
                            rememberToEnableTheNextStep = true
                            enabledStepIndex = i+1
                        }
                    }
                    return substep
                })
                return step
            })
            // If we need to enable the next step...
            if (rememberToEnableTheNextStep) {
                newSteps[enabledStepIndex].enabled = true
                newSteps[enabledStepIndex].substeps[0].enabled = true
            }
            return { steps: newSteps }

        default:
            return state
    }
}
export default stepReducer;
