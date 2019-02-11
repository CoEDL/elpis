import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Card, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer from '../StepInformer';
import { translate } from 'react-i18next';

class StepTrainingError extends Component {
    render() {
        const { t } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 5 }>
                            <StepInformer />
                        </Grid.Column>

                        <Grid.Column width={ 11 }>
                            <Header as='h1' text='true'>
                                <Icon name='warning' />
                                { t('trainingModelError.title') }
                            </Header>
                            <p>We ran into a problem when training the model</p>
                            <p>Please click the button below to connect you to a tech person on slack</p>
                            <p>An error file detailing the log showing below will be sent as an attachment to the technical team on slack</p>

                            <Card>
                                <Card.Content header={ t('trainingModelError.errorLogHeader') } />
                                <Card.Content description='Error logs spited out while training model' />
                            </Card>

                            <Button href="https:slack.com/" target="_blank">
                                { t('trainingModelError.contactButton') }
                            </Button>

                            <Button as={ Link } to="/model-settings" >
                                { t('trainingModelError.backButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepTrainingError)
