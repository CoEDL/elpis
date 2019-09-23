import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Card, Divider, Grid, Header, Icon, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import downloadjs from 'downloadjs'
import { transcriptionStatus  } from 'redux/actions/transcriptionActions';
import { transcriptionTranscribe, transcriptionTranscribeAlign, transcriptionGetText, transcriptionGetElan } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";

class NewTranscriptionResults extends Component {

    statusInterval = null

    componentDidMount = () => {
        const { transcriptionTranscribe, transcriptionTranscribeAlign } = this.props;

        // trigger a status check every so often
        this.statusInterval = setInterval(this.handleTranscriptionStatus, 1000)

        // make a plain text or aligned transcription depending on the URL param
        const format = this.props.match.params.format
        if (format == "text") transcriptionTranscribe()
        if (format == "elan") transcriptionTranscribeAlign()
    }

    handleTranscriptionStatus = () => {
        const { status, transcriptionStatus } = this.props;
        const format = this.props.match.params.format

        // check status from API
        transcriptionStatus()

        if (status==='transcribed') {
            this.props.clearInterval(this.statusInterval)
            if (format == "text") this.props.transcriptionGetText()
            if (format == "elan") this.props.transcriptionGetElan()
        }
        // TODO handle a status error, but it would be better to handle error at the action level
    }

    handleDownload = () => {
        const { elan, text } = this.props
        const format = this.props.match.params.format
        if (format == "text") downloadjs(text, 'text.txt', 'text/txt');
        if (format == "elan") downloadjs(elan, 'elan.eaf', 'text/xml');
    }

    render() {
        const { t, audioFilename, elan, text, status } = this.props;
        const format = this.props.match.params.format

        const loadingIcon = (status === 'transcribing') ? (
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
                                { t('transcription.results.title') }
                            </Header>

                            <CurrentModelName />

                            <Segment>
                                {t('transcription.results.usingAudio', { audioFilename: audioFilename})}
                            </Segment>

                            <Message icon>
                                { loadingIcon }
                                <Message.Content>
                                    <Message.Header>{ status }</Message.Header>
                                </Message.Content>
                            </Message>


                            {format == "text" && text && status == 'transcribed' &&
                            <Segment>
                                {text.split(' ').slice(1).join(' ')}
                            </Segment>
                            }

                            <Button disabled={status !== 'transcribed'} onClick={this.handleDownload}>
                                {t('transcription.results.downloadButton')}
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
        name: state.model.name,
        status: state.transcription.status,
        audioFilename: state.transcription.audioFilename,
        text: state.transcription.text,
        elan: state.transcription.elan
    }
}

const mapDispatchToProps = dispatch => ({
    transcriptionStatus: () => {
        dispatch(transcriptionStatus())
    },
    transcriptionTranscribe: () => {
        dispatch(transcriptionTranscribe())
    },
    transcriptionTranscribeAlign: () => {
        dispatch(transcriptionTranscribeAlign())
    },
    transcriptionGetText: () => {
        dispatch(transcriptionGetText())
    },
    transcriptionGetElan: () => {
        dispatch(transcriptionGetElan())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(
    translate('common')(
        ReactTimeout(NewTranscriptionResults)))
