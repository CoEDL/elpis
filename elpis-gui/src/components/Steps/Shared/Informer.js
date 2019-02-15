import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { List, Accordion } from 'semantic-ui-react';
import { connect } from 'react-redux'
import classNames from 'classnames'
import { setCurrentStep } from 'redux/actions'
import Indicator from 'components/Steps/Shared/Indicator';
import './Informer.css'


class StepInformer extends Component {

	handleStepSelect = (step, i, j) => {
		const { history } = this.props
		// Go to new page
		history.push(step.path)
	}

	componentDidMount = () => {
		// identify which step is currently being done
		const { match, setCurrentStep } = this.props
		console.log("match.url", match.url)
		// let urlParams = match.url.split('/')
		// console.log(urlParams)
		// urlParams = urlParams.filter(function(x){
		// 	return (x !== (undefined || null || ''));
		// });

		setCurrentStep(match.url)
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

						const done  = "#E0C6EE";
						const doing = "#D3A0F0";
						const todo  = "#ccc";

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
		steps: state.steps.steps,
		ownProps: ownProps
	}
}

const mapDispatchToProps = dispatch => ({
	setCurrentStep: (urlParams) => {
		dispatch(setCurrentStep(urlParams))
	}
})


export default withRouter(
	connect(
		mapStateToProps,
		mapDispatchToProps
	)(StepInformer)
)
