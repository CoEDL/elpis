import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, Placeholder } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';

class StepWelcome extends Component {

	render() {
		const { t } = this.props

		return (

			<Grid>
				<Grid.Row centered>
					<Grid.Column >
						<Branding />
					</Grid.Column>
				</Grid.Row>

				<Grid.Row>
					<Grid.Column>

						<Segment>
							<Button as={ Link } to="/data-bundles">
								{ t('welcome.dataBundlesButton') }
							</Button>
							<Button as={ Link } to="/models">
								{ t('welcome.modelsButton') }
							</Button>
						</Segment>

						<Segment>
							<Button as={ Link } to="/data-bundle/new">
								{ t('welcome.newDataBundleButton') }
							</Button>
							<Button as={ Link } to="/model/new">
								{ t('welcome.newModelButton') }
							</Button>
						</Segment>

						<Segment>
							<Button as={ Link } to="/transcription/new">
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


export default translate('common')(StepWelcome);
