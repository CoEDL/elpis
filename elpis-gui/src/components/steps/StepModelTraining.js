import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer from '../StepInformer';
import { translate } from 'react-i18next';
import { connect } from 'react-redux';
import { triggerApiWaiting } from '../../redux/actions';

class StepModelTraining extends Component {
    componentDidMount = () => {
        // this.props.triggerApiWaiting('now training')
    }
    render() {
        const { t, settings, apiWaiting } = this.props;

        // TODO: display as list rather than run-on line
        const settingDescription = [
            t('modelSettings.audioLabel') + ' ' + settings.frequency,
            t('modelSettings.mfccLabel')  + ' ' + settings.mfcc,
            t('modelSettings.nGramLabel') + ' ' + settings.ngram,
            t('modelSettings.beamLabel')  + ' ' + settings.beam
        ].join(' ~ ');


        return (
            <div>
                <Dimmer active={apiWaiting.status}>
                    <Loader size="massive"  content={apiWaiting.message} />
                </Dimmer>

                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 5 }>
                            <StepInformer />
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
        settings: state.model.settings,
        apiWaiting: state.model.apiWaiting
    }
}
const mapDispatchToProps = dispatch => ({
    triggerApiWaiting: message => {
        dispatch(triggerApiWaiting(message))
    }
})
export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(StepModelTraining));
