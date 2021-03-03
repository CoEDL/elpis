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
            <>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Branding />
                        </Grid.Column>
                    </Grid.Row>

                    <Grid.Row className="welcome-description">
                        <Grid.Column>
                            <div className="keep-line-breaks">{ t('welcome.description') }</div>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <div className="welcome-options">
                    <div className="row">
                        <div className="left-col train-button">
                            <Link to={urls.gui.engine.index}>
                                {t('welcome.start_train')}
                            </Link>
                        </div>
                        <div className="right-col keep-line-breaks text">{ t('welcome.train_description') }</div>
                    </div>
                    <div className="row">
                        <div className="left-col transcribe-button">
                            <Link to={urls.gui.transcription.choose}>
                                {t('welcome.start_transcribe')}
                            </Link>
                        </div>
                        <div className="right-col keep-line-breaks text">{ t('welcome.transcribe_description') }</div>
                    </div>
                </div>
            </>
		);
	}
}


export default translate('common')(StepWelcome)
