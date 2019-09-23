import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { List, Accordion } from 'semantic-ui-react';
import { connect } from 'react-redux'
import classNames from 'classnames'
import { setCurrentStep } from 'redux/actions/appActions'
import './Informer.css'


class StepInformer extends Component {

	handleStepSelect = (step, i, j) => {
		const { history } = this.props
		history.push(step.path)
	}

	componentDidMount = () => {
		const { match, setCurrentStep } = this.props
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

						return (
							<div key={ i }>

								<Accordion.Content active={ step.enabled || step.doing }>
									<List className="stepList">
										{
											// for each substep (pass in the step index and the substep index)
											// we'll use these to target the selected substep in redux
											step.substeps.map((substep, j) => {

												// substep classes
												const substepClassNames = classNames({
													firstSubstep: j === 0,
													substepDone: substep.done,
													substepDoing: substep.doing,
													disabled: !substep.enabled
												})

												return (
													<List.Item className={ substepClassNames }
														onClick={ () => this.handleStepSelect(substep, i, j) }
														key={ substep.title }>

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
		steps: state.app.steps,
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
