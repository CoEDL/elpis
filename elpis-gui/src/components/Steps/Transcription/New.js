import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Icon, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import downloadjs from 'downloadjs'
import {
    transcriptionNew,
    transcriptionStatus,
    transcriptionTranscribe,
    transcriptionTranscribeAlign,
    transcriptionGetText,
    transcriptionGetElan } from 'redux/actions/transcriptionActions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";
import urls from 'urls'

class NewTranscription extends Component {

    statusInterval = null

    componentDidMount = () => {}

    triggerStatusCheck = () => {
        console.log("trigger status check")
        this.statusInterval = setInterval(this.doStatusCheck, 1000)
    }

    doStatusCheck = () => {
        const { status, type, transcriptionGetElan } = this.props;

        this.props.transcriptionStatus()

        console.log("render status", status)
        console.log("render type", type)

        // clear the status check
        if (status == 'transcribed') {
            clearInterval(this.statusInterval)

            if (type == 'elan') {
                console.log("fire transcriptionGetElan")
                transcriptionGetElan()
            }
        }

    }


    handleTranscribe = () => {
        // pass in the status check function
        // so we can fire it in .then after the dispatch is done
        this.props.transcriptionTranscribe(this.triggerStatusCheck)
    }

    handleTranscribeAlign = () => {
        // pass in the status check function
        // so we can fire it in .then after the dispatch is done
        this.props.transcriptionTranscribeAlign(this.triggerStatusCheck)
    }


    handleDownloadText = () => {
        downloadjs(this.props.text, 'text.txt', 'text/txt');
    }

    handleDownloadElan = () => {
        downloadjs(this.props.elan, 'elan.eaf', 'text/xml');
    }

    onDrop = (acceptedFiles, rejectedFiles) => {
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.transcriptionNew(formData)
    }


    render = () => {
        const { t, filename, status, type, text, elan, modelName } = this.props;

        // preven the buttnos from being clicked if we haven't got
        // an active model, or file to transcribe
        let enableButtons = (modelName && filename) ? true : false

        const loadingIcon = (status == 'transcribing') ? (
            <Icon name='circle notched' loading />
        ) : (
            <p>ready or done</p>
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
                            <Header as='h1' text="true">
                                { t('transcription.new.title') }
                            </Header>

                            <CurrentModelName />

                            <Dropzone className="dropzone" onDrop={ this.onDrop } getDataTransferItems={ evt => fromEvent(evt) }>
                                { ({ getRootProps, getInputProps, isDragActive }) => {
                                    return (
                                        <div
                                            { ...getRootProps() }
                                            className={ classNames("dropzone", {
                                                "dropzone_active": isDragActive
                                            }) }
                                        >
                                            <input { ...getInputProps() } />

                                            {
                                                isDragActive ? (
                                                    <p>{ t('transcription.new.dropFilesHintDragActive') } </p>
                                                ) : (<p>{ t('transcription.new.dropFilesHint') }</p>)
                                            }
                                        </div>
                                    );
                                } }
                            </Dropzone>

                            {filename &&
                                <Segment>{t('transcription.new.usingAudio', { filename })} </Segment>
                            }

                            <Divider />

                            <Segment>

                                {t('transcription.new.format')}

                                <Button onClick={this.handleTranscribe} disabled={!enableButtons} >
                                    {t('transcription.new.resultsText')}
                                </Button>

                                <Button onClick={this.handleTranscribeAlign} disabled={!enableButtons} >
                                    {t('transcription.new.resultsElan')}
                                </Button>
                            </Segment>

                            <Segment>
                                {loadingIcon} | {status} {type}
                            </Segment>

                            {text &&
                                <Segment>
                                    <p>{text}</p>
                                    <Button onClick={this.handleDownloadText}>
                                        {t('transcription.results.downloadButton')}
                                    </Button>
                                </Segment>
                            }

                            {elan &&
                                <Segment>
                                    <Button onClick={this.handleDownloadElan}>
                                        {t('transcription.results.downloadButton')}
                                    </Button>
                                </Segment>
                            }



                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        modelName: state.model.name,
        filename: state.transcription.filename,
        status: state.transcription.status,
        type: state.transcription.type,
        text: state.transcription.text,
        elan: state.transcription.elan
    }
}
const mapDispatchToProps = dispatch => ({
    transcriptionNew: formData => {
        dispatch(transcriptionNew(formData))
    },
    transcriptionTranscribe: triggerStatusCheck => {
        triggerStatusCheck()
        dispatch(transcriptionTranscribe())
            .then(response =>{
                // This is returned when the transcribe process is done,
                // because this API call is syncronous.
                // So we can safely request the text in this 'then'
                console.log("mapDispatchToProps transcribe", response)
                dispatch(transcriptionGetText())
            })
    },
    transcriptionTranscribeAlign: triggerStatusCheck => {
        dispatch(transcriptionTranscribeAlign())
            .then(response => {
                // This is returned immediately, because this API call runs in the background
                // So we can't request the elan file. Use doStatusCheck above
                console.log("mapDispatchToProps transcribeAlign", response)
                triggerStatusCheck()
            })
    },
    transcriptionStatus: () => {
        console.log("dispatch transcription status")
        dispatch(transcriptionStatus())
            .then(response => {
                console.log("mapDispatchToProps status", response)
            })
    },
    transcriptionGetText: () => {
        dispatch(transcriptionGetText())
    },
    transcriptionGetElan: () => {
        dispatch(transcriptionGetElan())
    },
    dispatchStatus: (status, type) => {
        console.log(status, type)
        dispatch(transcriptionStatus())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewTranscription));
