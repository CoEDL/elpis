import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { List, Icon, Accordion } from 'semantic-ui-react';
import Indicator from '../components/Indicator';

/**
 * Instructions for building the steps navigation menu when the user wants to build a model.
 */
export const NewModelInstructions = [
    {
        name: "Step 1",
        path: "/naming",
        icon: "wrench",
        substeps: [
            { name: "Build a new model", path: "/naming"},
            { name: "Add data", path: "/add-data"},
            { name: "Data prepatation", path: "/data-preparation"},
            { name: "Pronunciation dictionary", path: "/build-pronunciation-dictionary"},
        ]
    },
    {
        name: "Step 2",
        path: "/model-settings",
        icon: "lemon",
        substeps: [
            { name: "Model settings", path: "/model-settings"},
            { name: "Training model", path: "/training-model"},
            { name: "Trained Model Success", path: "/training-success"},
        ]
    },
    {
        name: "Step 3",
        path: "/new-transcription",
        icon: "microphone",
        substeps: [
            { name: "Choose model", path: "/new-transcription"},
            { name: "Input data", path: "/input-data"},
            { name: "Transcribe", path: "/transcribe"},
        ]
    }
];


class StepInformer extends Component {
    constructor(props) {
        super(props);
        const { instructions } = props;
        this.state = {
            // Only the first step is open at the beginning.
            openSteps: Array(instructions.length).fill(false).map((_, i) => i === 0 ).slice(),
        };

    }

    toggleStep(i) {
        let openSteps = this.state.openSteps.slice();
        openSteps[i] = !openSteps[i];
        this.setState({ openSteps: openSteps});
    }

    render() {
        const { instructions, location } = this.props;
        const done = "green";
        const doing = "blue";
        const todo = "#ccc";

        // index of the current step overall
        let stepPaths = [];
        instructions.forEach(step => {
            stepPaths = stepPaths.concat(step.substeps.map(substep => substep.path));
        });
        let target_idx = stepPaths.findIndex(step => step === location.pathname);

        // Build the components from the instruction and step (location/route) the process is up to.
        let mainSteps = [];
        instructions.forEach((step, i) => {
            let subSteps = [];
            step.substeps.forEach( (substep, j) => {
                let idx = stepPaths.findIndex(step => step === substep.path);

                // Build the indicator component
                let indicator = (<Indicator
                    // Determine the colour status of the step.
                    color={idx < target_idx ? done : (idx === target_idx ? doing : todo)}
                    // if this is the first substep in the step, then cap it.
                    cap={j===0}
                    // if this is the last substep in the step, then cup it.
                    cup={j===step.substeps.length-1}
                />);

                // Build the list item
                if (location.pathname === substep.path) {
                    subSteps.push(
                        <List.Item key={j} style={{position: "relative"}}>
                            {indicator}
                            {/*
                                paddingLeft to move the text out of the indicators way.
                                Also, since this is the current step, the padding is less
                                to tell the user this step is different to the others (current).
                             */}
                            <div style={{paddingLeft: "1.4em"}}>{substep.name}</div>
                        </List.Item>
                    );
                } else {
                    subSteps.push(
                        <List.Item
                            key={j}
                            as={Link}
                            to={substep.path}
                            style={{position: "relative"}}
                        >{indicator}<div style={{paddingLeft: "1.8em"}}>{substep.name}</div></List.Item>
                    );
                }
            });

            // Build the main step component
            mainSteps.push(
                <div key={i}>
                    {/* TODO: make active more user friendly */}
                    <Accordion.Title active>
                        <div>
                            <Icon name={step.icon} style={{display:'inline'}}/>
                            <div style={{display:'inline'}}>{step.name}</div>
                            <Icon name='dropdown' />
                        </div>
                    </Accordion.Title>
                    {/* TODO: make active more user friendly */}
                    <Accordion.Content active>
                        <List>{subSteps}</List>
                    </Accordion.Content>
                </div>
            );
        });

        return (
            <Accordion styled>
                {mainSteps}
            </Accordion>
        );
    }
}

export default withRouter(props => <StepInformer {...props}/>);