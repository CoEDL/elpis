import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import { LazyLog, ScrollFollow } from 'react-lazylog/es5';
import { triggerApiWaiting, modelTrain, modelStatus } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "./CurrentModelName";
import urls from 'urls'

class ModelTrain extends Component {

    statusInterval = null

    componentDidMount = () => {
        // this.props.triggerApiWaiting('now training')
    }

    handleModelTrain = () => {
        this.props.modelTrain()
        this.statusInterval = this.props.setInterval(this.handleModelStatus, 5000)
    }

    handleModelStatus = () => {
        const { status, modelStatus } = this.props;
        modelStatus()
        if (status=='trained') this.props.clearInterval(this.statusInterval)
    }


    onScroll = () => {
        console.log("onScroll")
    }
    follow = () => {
        console.log("follow")
    }

    render() {
        const { t, settings, apiWaiting, status } = this.props;

        console.log('status', status)

        const loadingIcon = (status === 'training') ? (
            <Icon name='circle notched' loading  />
        ) : null

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

                            <CurrentModelName />

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
                                { loadingIcon }
                                <Message.Content>
                                    <Message.Header>{ status }</Message.Header>
                                </Message.Content>
                            </Message>

                            <Card fluid>
                                <Card.Content header={ t('model.train.logsHeader') } />
                                <Card.Content description={ t('model.train.logsDescription') } />
                                <div className="kaldi-log">
{/*
                                    <ScrollFollow
                                        startFollowing={true}
                                        render={({ follow, onScroll }) => (
                                        <LazyLog url={urls.api.model.logstream} stream follow={follow} onScroll={onScroll} />
                                        )}
                                    />
*/}
                                </div>
                            </Card>

                            <Divider />

                            <Button as={ Link } to={urls.gui.model.results}>
                                { t('model.train.nextButton') }
                            </Button>
{/*
                            <Button as={ Link } to="/model/train/error">
                                { t('model.train.nextButtonError') }
                            </Button>
*/}
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
        name: state.model.name,
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
export default connect(mapStateToProps, mapDispatchToProps)(
    translate('common')(
    ReactTimeout(ModelTrain)))
