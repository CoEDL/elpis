import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Icon, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { transcriptionNew } from 'redux/actions/transcriptionActions';
import { transcriptionAudioFile, transcriptionStatusReset } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";
import urls from 'urls'

class NewTranscription extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.transcriptionNew(formData)
    }

    componentDidMount = () => {
        this.props.transcriptionStatusReset()
    }

    render() {
        const { t, filename, modelName } = this.props;

        // preven the buttnos from being clicked if we haven't got
        // an active model, or file to transcribe
        let enableButtons = (modelName && filename) ? true : false

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

                                <Button as={Link} to={urls.gui.transcription.results + '/text'} disabled={!enableButtons} >
                                    {t('transcription.new.resultsText')}
                                </Button>

                                <Button as={Link} to={urls.gui.transcription.results + '/elan'} disabled={!enableButtons} >
                                    {t('transcription.new.resultsElan')}
                                </Button>
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
        modelName: state.model.name,
        filename: state.transcription.filename,
        status: state.transcription.status
    }
}
const mapDispatchToProps = dispatch => ({
    transcriptionNew: formData => {
        dispatch(transcriptionNew(formData))
    },
    transcriptionStatusReset: () => {
        dispatch(transcriptionStatusReset())
    }

})


export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewTranscription));
