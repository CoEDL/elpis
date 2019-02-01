import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { List, Icon, Accordion, Step } from 'semantic-ui-react';
import Indicator from '../components/Indicator';
import { connect } from 'react-redux'
import { setStepDoing, setCurrentStepDone, enableNextStep } from '../redux/actions'
import classNames from 'classnames'
import './StepInformer.css'

/**
 * Steps navigation menu
 */

// change to use redux state instead
export const NewModelInstructions = [];


class StepInformer extends Component {

    handleStepSelect = (step, i, j) => {
        const { setCurrentStepDone, enableNextStep, history } = this.props

        // Temporarily set 'enabled' property of the next step
        // This should be set by main page buttons
        // in response to tasks being completed, not by nav
        enableNextStep(step)

        // Set done status for the active step
        // This should be set by main page buttons
        // in response to tasks being completed, not by nav
        setCurrentStepDone()

        // Go to new page
        history.push(step.path)
    }

    componentDidMount = () => {
        // identify which step is currently being done
        const { match, setStepDoing } = this.props
        const params = match.url.split('/')
        setStepDoing(params)
    }


    render() {
        const { steps } = this.props

        return (
            <Accordion styled>
                {
                    // for each step (pass down the index too,
                    // we'll use that when we call the action to update redux state)
                    steps.map((step, i) => {

                        // step classes - use 'disabled' rather than 'enabled' cause it might have magic power
                        const stepClassNames = classNames({
                            stepDone: step.done,
                            stepDoing: step.doing,
                            disabled: !step.enabled
                        })

                        const done = "yellow";
                        const doing = "yellowgreen";
                        const todo = "#ccc";

                        return (
                            <div key={ step.title }>
                                <Accordion.Title className={ stepClassNames } active={ step.enabled || step.doing } onClick={ () => this.handleStepSelect(step, i, 0) }>
                                    { step.title }
                                </Accordion.Title>
                                <Accordion.Content active={ step.enabled || step.doing }>
                                    <List className="stepList">
                                        {
                                            // for each substep (pass in the step index and the substep index)
                                            // we'll use these to target the selected substep in redux
                                            step.substeps.map((substep, j) => {
                                                const color = (substep.doing) ? doing : (substep.done) ? done : todo
                                                // Build the indicator component
                                                let indicator = (<Indicator
                                                    // Determine the colour status of the step.
                                                    color={ color }
                                                    // if this is the first substep in the step, then cap it.
                                                    cap={ j === 0 }
                                                    // if this is the last substep in the step, then cup it.
                                                    cup={ j === step.substeps.length - 1 }
                                                />);


                                                // substep classes
                                                const substepClassNames = classNames({
                                                    substepDone: substep.done,
                                                    substepDoing: substep.doing,
                                                    disabled: !substep.enabled
                                                })

                                                return (
                                                    <List.Item className={ substepClassNames }
                                                        onClick={ () => this.handleStepSelect(substep, i, j) }
                                                        key={ substep.title }>

                                                        { indicator }

                                                        <div style={ { paddingLeft: "1.4em" } }>{ substep.title }</div>

                                                    </List.Item>
                                                )
                                            }
                                            )
                                        }
                                    </List>
                                </Accordion.Content>
                            </div>
                        )
                    })
                }
            </Accordion>
        )
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        steps: state.stepReducer.steps,
        ownProps: ownProps
    }
}

const mapDispatchToProps = dispatch => ({
    setStepDoing: urlParams => {
        dispatch(setStepDoing(urlParams))
    },
    setCurrentStepDone: () => {
        dispatch(setCurrentStepDone())
    },
    enableNextStep: (step) => {
        dispatch(enableNextStep(step))
    }
})


export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(StepInformer)
)
