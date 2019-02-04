import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepModelTraining extends Component {
    render() {
        const { t } = this.props;

        // TODO: display as list rather than runon line
        const settingDescription = [
            t('model-settings.audio-label') + 'XXX',
            t('model-settings.mfcc-label') + 'XXX',
            t('model-settings.n-gram-label') + 'XXX',
            t('model-settings.beam-label') + 'XXX'
        ].join(' ~ ');

        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 5 }>
                            <StepInformer instructions={ NewModelInstructions } />
                        </Grid.Column>

                        <Grid.Column width={ 11 }>
                            <Header as='h1' text='true'>
                                { t('trainingModel.title') }
                            </Header>

                            <Message icon>
                                <Icon name='circle notched' loading />
                                <Message.Content>
                                    <Message.Header>{ t('trainingModel.trainingHeader') }</Message.Header>
                                </Message.Content>
                            </Message>

                            <Card>
                                <Card.Content header={ t('trainingModel.settingsHeader') } />
                                <Card.Content description={ settingDescription } />
                            </Card>

                            <Step.Group size='mini'>
                                <Step>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.preparingAcousticHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step active>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.featuresExtractionHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step disabled>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.preparingLanguageDataHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                            </Step.Group>

                            <Card>
                                <Card.Content header={ t('trainingModel.logsHeader') } />
                                <Card.Content description='gory output from Kaldi - but not interactive' />
                            </Card>

                            <Button as={ Link } to="/training-success">
                                { t('trainingModel.nextButton') }
                            </Button>

                            <Button as={ Link } to="/training-error" icon>
                                <Icon name='warning sign' />
                                { t('trainingModel.nextButtonError') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepModelTraining)
