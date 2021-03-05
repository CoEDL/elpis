import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Divider, Header, Container, Segment, Placeholder } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import Branding from 'components/Shared/Branding';
import urls from 'urls'

class StepWelcome extends Component {

	render() {
		const { t, list } = this.props
		return (
            <div>
                <Branding />
                <Segment className="welcome-options">
                <Grid centered>
                    <Grid.Row>
                        <Grid.Column className="keep-line-breaks">
                            { t('welcome.description') }
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <Divider/>

                    <div className="row">
                        <div className="left-col train-button">
                            <Button as={Link} to={urls.gui.engine.index}>
                                {t('welcome.start_train')}
                            </Button>
                        </div>
                        <div className="right-col keep-line-breaks text">{ t('welcome.train_description') }</div>
                    </div>
                    <div className="row">
                        <div className="left-col transcribe-button">
                            <Button as={Link} to={urls.gui.transcription.choose}>
                                {t('welcome.start_transcribe')}
                            </Button>
                        </div>
                        <div className="right-col keep-line-breaks text">{ t('welcome.transcribe_description') }</div>
                    </div>
                </Segment>
            </div>
		);
	}
}


export default translate('common')(StepWelcome)
