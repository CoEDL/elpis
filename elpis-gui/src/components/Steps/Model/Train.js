import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import { triggerApiWaiting, modelTrain, modelStatus } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelTrain extends Component {
    state = {
        dots: 0
    }

    componentDidMount = () => {
        this.props.triggerApiWaiting('now training')
    }
    handleModelTrain = () => {
        console.log('train')
        this.props.modelTrain()
        this.props.setInterval(this.handleModelStatus, 2000)
    }
    handleModelStatus = () => {
        console.log('status')
        this.props.modelStatus()
    }

    render() {
        const { t, settings, apiWaiting, status } = this.props;

        console.log('status', status)

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
                                { t('model.train.title') }
                            </Header>

                            <Card fluid>
                                <Card.Content header={ t('model.train.settingsHeader') } />
                                <Card.Content description={ t('model.settings.ngramLabel') + ' ' + settings.ngram } />
                            </Card>

                            <Segment>
                                <Button onClick={this.handleModelTrain}>
                                    { t('model.train.trainButton') }
                                </Button>
                                <Button onClick={this.handleModelStatus}>
                                    { t('model.train.statusButton') }
                                </Button>
                            </Segment>


                            <Message icon>
                                <Icon name='circle notched' loading />
                                <Message.Content>
                                    <Message.Header>{ status }</Message.Header>
                                </Message.Content>
                            </Message>

                            <Card fluid>
                                <Card.Content header={ t('model.train.logsHeader') } />
                                <Card.Content description={ t('model.train.logsDescription') } />
                            </Card>


                            <Divider />

                            <Button as={ Link } to="/model/train/results">
                                { t('model.train.nextButton') }
                            </Button>

                            <Button as={ Link } to="/model/train/error" icon>
                                <Icon name='warning sign' />
                                { t('model.train.nextButtonError') }
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
        apiWaiting: state.model.apiWaiting,
        status: state.model.status
    }
}
const mapDispatchToProps = dispatch => ({
    triggerApiWaiting: message => {
        dispatch(triggerApiWaiting(message))
    },
    modelTrain: () => {
        dispatch(modelTrain())
    },
    modelStatus: () => {
        dispatch(modelStatus())
    },


})
export default connect(
    mapStateToProps,
    mapDispatchToProps)(
    translate('common')(
    ReactTimeout(ModelTrain)));
