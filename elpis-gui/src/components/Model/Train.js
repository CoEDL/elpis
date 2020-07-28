import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import { modelTrain, modelStatus } from 'redux/actions/modelActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import CurrentModelName from "./CurrentModelName";
import urls from 'urls'

class ModelTrain extends Component {

    statusInterval = null

    componentDidMount = () => {
    }

    handleModelTrain = () => {
        this.props.modelTrain()
        this.statusInterval = this.props.setInterval(this.handleModelStatus, 1000)
    }

    handleModelStatus = () => {
        const { status, modelStatus } = this.props;
        modelStatus()
        if (status=='trained') this.props.clearInterval(this.statusInterval)
    }


    onScroll = () => {
    }
    follow = () => {
    }

    render() {
        const { t, name, settings, status, stage_status } = this.props;

        const loadingIcon = (status === 'training') ? (
            <Icon name='circle notched' loading  />
        ) : null

        const trainingButton = (status === 'ready') ? (
            <Button onClick={this.handleModelTrain} disabled={!name}>
                { t('model.train.trainButton') }
            </Button>
        ) : null

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
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

                            <Message icon>
                                { loadingIcon }
                                <Message.Content>
                                    <Message.Header>{ status }</Message.Header>
                                    {stage_status &&
                                        Object.keys(stage_status).map((stage, i) => {
                                            let name = stage_status[stage]["name"]
                                            let status = stage_status[stage]["status"]
                                            let message = stage_status[stage]["message"]
                                        return (
                                            <p key={stage} className="stage">
                                                <span className="name">{name}</span>
                                                <span className="divider">{status && <>|</>}</span>
                                                <span className="status">{status}</span>
                                                <span className="divider">{message && <>|</>}</span>
                                                <span className="message">{message}</span>
                                            </p>
                                        )}
                                    )}
                                </Message.Content>
                            </Message>
                                <Segment>
                                    {trainingButton}
                                </Segment>


                        </Grid.Column>
                    </Grid>
                </Segment>

            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        settings: state.model.settings,
        status: state.model.status,
        stage_status: state.model.stage_status
    }
}
const mapDispatchToProps = dispatch => ({
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
