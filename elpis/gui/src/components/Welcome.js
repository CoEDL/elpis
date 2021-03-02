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

			<Grid className="welcome">
				<Grid.Row>
					<Grid.Column >
						<Branding />
					</Grid.Column>
				</Grid.Row>

				<Grid.Row className="welcome-description">
					<Grid.Column>
						<div className="keep-line-breaks">{ t('welcome.description') }</div>
					</Grid.Column>
				</Grid.Row>

				<Grid.Row columns={2} className="train-description">
					<Grid.Column>
						<div className="keep-line-breaks text">{ t('welcome.train_description') }</div>
					</Grid.Column>
					<Grid.Column>
						<div className="train-button">
                        <Link to={urls.gui.engine.index}>
                            {t('welcome.start_train')}
                        </Link>
                        </div>
					</Grid.Column>
				</Grid.Row>

				<Grid.Row columns={2} className="transcription-description">
					<Grid.Column className="">
						<div className="keep-line-breaks text">{ t('welcome.transcribe_description') }</div>
					</Grid.Column>
					<Grid.Column>
						<div className="transcribe-button">
                        <Link to={urls.gui.transcription.choose}>
                            {t('welcome.start_transcribe')}
                        </Link>
                        </div>
					</Grid.Column>
				</Grid.Row>
			</Grid>
		);
	}
}


export default translate('common')(StepWelcome)
