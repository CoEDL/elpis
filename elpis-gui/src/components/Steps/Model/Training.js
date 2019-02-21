import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { triggerApiWaiting } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelTraining extends Component {
    componentDidMount = () => {
        this.props.triggerApiWaiting('now training')
    }
    render() {
        const { t, settings, apiWaiting } = this.props;

        // TODO: display as list rather than run-on line
        const settingDescription = [
            t('model.settings.audioLabel') + ' ' + settings.frequency,
            t('model.settings.mfccLabel')  + ' ' + settings.mfcc,
            t('model.settings.ngramLabel') + ' ' + settings.ngram,
            t('model.settings.beamLabel')  + ' ' + settings.beam
        ].join(' ~ ');


        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text='true'>
                                { t('model.training.title') }
                            </Header>

                            <Message icon>
                                <Icon name='circle notched' loading />
                                <Message.Content>
                                    <Message.Header>{ t('model.training.trainingHeader') }</Message.Header>
                                </Message.Content>
                            </Message>

                            <Card fluid>
                                <Card.Content header={ t('model.training.settingsHeader') } />
                                <Card.Content description={ settingDescription } />
                            </Card>

                            <Step.Group size='mini'>
                                <Step active>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('model.training.preparingAcousticHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('model.training.featuresExtractionHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                                <Step>
                                    <Icon name='info' size='tiny' />
                                    <Step.Content>
                                        <Step.Title>{ t('model.training.preparingLanguageDataHeader') }</Step.Title>
                                    </Step.Content>
                                </Step>

                            </Step.Group>

                            <Card fluid>
                                <Card.Content header={ t('model.training.logsHeader') } />
                                <Card.Content description='gory output from Kaldi - but not interactive' />
                            </Card>

                            <Divider />

                            <Button as={ Link } to="/model/training/results">
                                { t('model.training.nextButton') }
                            </Button>

                            <Button as={ Link } to="/model/training/error" icon>
                                <Icon name='warning sign' />
                                { t('model.training.nextButtonError') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>

                {/* temporarily disable with 'false &&' */}
                <Dimmer active={ false && apiWaiting.status }>
                    <Loader size="massive"  content={apiWaiting.message} />
                </Dimmer>

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
export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelTraining));
