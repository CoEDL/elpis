import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, Placeholder } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import { translate } from 'react-i18next';
import { newModel } from '../../redux/actions';
import { connect } from 'react-redux';

class StepWelcome extends Component {

	handleNewModel = () => {
		this.props.newModel();
		this.props.history.push('/naming')
	}

	render() {
		const { t } = this.props

		return (

			<Grid>
				<Grid.Row centered>
					<Grid.Column >
						<StepBranding />
					</Grid.Column>
				</Grid.Row>

				<Grid.Row>
					<Grid.Column>
						<Segment>
							<Button onClick={ this.handleNewModel }>
								{ t('welcome.newModelButton') }
							</Button>
							<Button as={ Link } to="/new-transcription">
								{ t('welcome.newTranscriptionButton') }
							</Button>
						</Segment>

						<Segment>
							<Header as='h2'>Instructional Video</Header>
							<p>{ t('welcome.intro', { passInSomething: "memememe" }) }</p>
						</Segment>

						<Segment>
							<p>{ t('welcome.stepPlaceholder') }</p>
							<Placeholder>
								<Placeholder.Header>
									<Placeholder.Line />
									<Placeholder.Line />
								</Placeholder.Header>
								<Placeholder.Paragraph>
									<Placeholder.Line />
									<Placeholder.Line />
									<Placeholder.Line />
								</Placeholder.Paragraph>
							</Placeholder>
						</Segment>

					</Grid.Column>
				</Grid.Row>
			</Grid>
		);
	}
}


const mapDispatchToProps = dispatch => ({
	newModel: () => {
		dispatch(newModel());
	}
})

export default withRouter(
	connect(
		null,
		mapDispatchToProps
	)(
		translate('common')(StepWelcome)
	)
);
