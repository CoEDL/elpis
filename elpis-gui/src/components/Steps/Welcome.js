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
{/*
						<Segment>
							<Button as={ Link } to="/data-bundle/new">
								{ t('welcome.newDataBundleButton') }
							</Button>
							<Button as={ Link } to="/model/new">
								{ t('welcome.newModelButton') }
							</Button>
						</Segment>

						<Segment>
							<Button as={ Link } to="/data-bundles">
								{ t('welcome.dataBundlesButton') }
							</Button>
							<Button as={ Link } to="/models">
								{ t('welcome.modelsButton') }
							</Button>
						</Segment>

						<Segment>
							<Button as={ Link } to="/transcription/new">
								{ t('welcome.newTranscriptionButton') }
							</Button>
						</Segment>
*/}

						<Segment>

							<p>
								Elpis is a speech recognition tool, which you can use to transcribe audio.
								It works in three parts:
							</p>
							<p>
								Step 1) Collect some files <br />
								Step 2) Training <br />
								Step 3) Use it to tanscribe new audio
							</p>

						</Segment>

						<Segment>
							<p>
								Start by <Link to="/data-bundle/new">making a new data bundle</Link> or <Link to="/data-bundles/">or use an existing one</Link>.
							</p>
						</Segment>

					</Grid.Column>
				</Grid.Row>
			</Grid>
		);
	}
}


export default translate('common')(StepWelcome);
