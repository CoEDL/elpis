import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, Placeholder } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import Branding from 'components/Shared/Branding';
import urls from 'urls'

class StepWelcome extends Component {

	render() {
		const { t, list } = this.props
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

							<p>
								Elpis is a speech recognition tool, which you can use to transcribe audio.
								It works in four parts:
							</p>
							<p>
								Step 1) Add some language recordings and their transcriptions that you already have <br />
								Step 2) Creating a pronunciation dictionary <br />
								Step 3) Training the speech recognition "models" <br />
								Step 4) Use it to tanscribe new audio
							</p>

						</Segment>

						<Segment>
							<p>
								Start by <Link to={urls.gui.dataset.new}>making a new group of recordings</Link> or <Link to={urls.gui.dataset.index}>or use one you have started before</Link>.
							</p>
						</Segment>

					</Grid.Column>
				</Grid.Row>
			</Grid>
		);
	}
}


export default translate('common')(StepWelcome)
