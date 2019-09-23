import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Icon, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { transcriptionAudioFile, transcriptionNew, transcriptionStatusReset } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";
import urls from 'urls'

class NewTranscription extends Component {

    state = {
        audioFilename: null,
        // formData: null
    }

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        // reset status cause we have a new file
        // var formData = new FormData();
        // formData.append('file', acceptedFiles[0]);
        this.setState({ audioFilename: acceptedFiles[0].name})
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.transcriptionAudioFile(acceptedFiles[0].name)
        this.props.transcriptionNew(formData)
    }

    componentDidMount = () => {
        this.props.transcriptionStatusReset()
    }


    render() {
        const { t, audioFilename, modelName } = this.props;
        let audioFileEl
        if (this.state.audioFilename) {
            audioFileEl = <Segment>{t('transcription.new.usingAudio', { audioFilename: this.state.audioFilename }) } </Segment>
        } else if (audioFilename) {
            audioFileEl = <Segment>{t('transcription.new.usingAudio', { audioFilename })} </Segment>
        }

        let showNext = (modelName && this.state.audioFilename) ? true : false

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

                            {/* disabled={!modelName}  */}

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

                            { audioFileEl }

                            <Divider />

                            <div>

                                {t('transcription.new.format')}
                                {
                                    showNext = true
                                }
                                <Button as={Link} to={urls.gui.transcription.results + '/text'} disabled={!showNext} >
                                    {t('transcription.new.resultsText')}
                                </Button>

                                <Button as={Link} to={urls.gui.transcription.results + '/elan'} disabled={!showNext} >
                                    {t('transcription.new.resultsElan')}
                                </Button>
                            </div>

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
        audioFilename: state.transcription.audioFilename,
        status: state.transcription.status
    }
}
const mapDispatchToProps = dispatch => ({
    transcriptionAudioFile: filename => {
        dispatch(transcriptionAudioFile(filename))
    },
    transcriptionNew: formData => {
        dispatch(transcriptionNew(formData))
    },
    transcriptionStatusReset: () => {
        dispatch(transcriptionStatusReset())
    }

})


export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewTranscription));
