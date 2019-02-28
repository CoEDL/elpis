import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Card, Divider, Grid, Header, Icon, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import downloadjs from 'downloadjs'
import { transcriptionElan, transcriptionStatus } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";

class NewTranscriptionResults extends Component {

    componentDidMount = () => {
        this.statusInterval = this.props.setInterval(this.handleTranscriptionStatus, 5000)
    }

    handleTranscriptionStatus = () => {
        const { status, transcriptionStatus } = this.props;
        console.log("status")
        transcriptionStatus()
        if (status==='transcribed') this.props.clearInterval(this.statusInterval)
    }

    handleElanBuild = () => {
        const { transcriptionElan } = this.props
        transcriptionElan()
    }

    handleElanDownload = () => {
        const { elan } = this.props
        downloadjs(elan, 'elan.eaf', 'text/xml');

    }

    render() {
        const { t, elan, audioFile, status } = this.props;

        console.log("elan", elan)
        console.log("audioFile", audioFile)
        console.log('status', status)

        const loadingIcon = (status === 'training') ? (
            <Icon name='circle notched' loading  />
        ) : null

        const elanButtons = (status==='transcribed') ? (
            <Segment>
                <Button onClick={ this.handleElanBuild }>
                { t('transcription.results.buildElanButton') }
                </Button>

                <Button onClick={ this.handleElanDownload }>
                { t('transcription.results.downloadElanButton') }
                </Button>
            </Segment>
        ) : (
            <Segment>
                { t('transcription.results.downloadButtonsNotReadyYet') }
            </Segment>
        )

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
                                { t('transcription.results.title') }
                            </Header>

                            <CurrentModelName />

                            <p>{ t('transcription.results.usingAudio') } { audioFile } </p>

                            <Message icon>
                                { loadingIcon }
                                <Message.Content>
                                    <Message.Header>{ status }</Message.Header>
                                </Message.Content>
                            </Message>

{/*
                            <Card fluid>
                                <Card.Content header={ t('transcription.results.errorLogHeader') } />
                                <Card.Content description='Were there any errors? Just output the log, nothing fancy' />
                            </Card>

                            <Card fluid>
                                <Card.Content header={ t('transcription.results.resultsHeader') } />
                                <Card.Content description='Blah Blah Blah Blah Blah' />
                            </Card>
 */}


{elanButtons}

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
        elan: state.transcription.elan,
        audioFile: state.transcription.audioFile,
        status: state.transcription.status
    }
}

const mapDispatchToProps = dispatch => ({
    transcriptionElan: () => {
        dispatch(transcriptionElan())
    },
    transcriptionStatus: () => {
        dispatch(transcriptionStatus())
    },
})

export default connect(mapStateToProps, mapDispatchToProps)(
    translate('common')(
        ReactTimeout(NewTranscriptionResults)))
