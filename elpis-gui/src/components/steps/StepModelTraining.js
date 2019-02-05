import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';
import { connect } from 'react-redux';

class StepModelTraining extends Component {
    render() {
        const { t, settings } = this.props;

        // TODO: display as list rather than runon line
        const settingDescription = [
            t('modelSettings.audioLabel') + ' ' + settings.frequency,
            t('modelSettings.mfccLabel')  + ' ' + settings.mfcc,
            t('modelSettings.nGramLabel') + ' ' + settings.ngram,
            t('modelSettings.beamLabel')  + ' ' + settings.beam
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

                            <Card fluid>
                                <Card.Content header={ t('trainingModel.settingsHeader') } />
                                <Card.Content description={ settingDescription } />
                            </Card>

                            <Step.Group size='mini'>
                                <Step active>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.preparingAcousticHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.featuresExtractionHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('trainingModel.preparingLanguageDataHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                            </Step.Group>

                            <Card fluid>
                                <Card.Content header={ t('trainingModel.logsHeader') } />
                                <Card.Content description='gory output from Kaldi - but not interactive' />
                            </Card>

                            <Divider />

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

const mapStateToProps = state => {
    return {
        settings: state.model.settings
    }
}
export default connect(mapStateToProps)(translate('common')(StepModelTraining));
