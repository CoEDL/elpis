import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Dropdown, Form, Grid, Header, Icon, List, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { withTranslation } from 'react-i18next';
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
import { modelLoad, modelList } from 'redux/actions/modelActions';
import { datasetLoad } from 'redux/actions/datasetActions';
import { pronDictLoad } from 'redux/actions/pronDictActions';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import CurrentModelName from "../Model/CurrentModelName";
import urls from 'urls'

class NewTranscription extends Component {

    statusInterval = null

    componentDidMount() {
        this.props.modelList()
    }

    triggerStatusCheck = () => {
        this.statusInterval = setInterval(this.doStatusCheck, 1000)
    }

    doStatusCheck = () => {
        const { status } = this.props;
        this.props.transcriptionStatus()
        if (status == 'transcribed') {
            clearInterval(this.statusInterval)
        }
    }

    handleTranscribe = () => {
        // pass in the status check function
        // so we can fire it in .then after the dispatch is done
        this.props.transcriptionTranscribe(this.triggerStatusCheck)
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

    handleSelectModel = (e, { value }) => {
        const { list, modelLoad } = this.props
        // get the matching ds and pd values
        var selectedModel = list.filter(m => m.name==value)
        // argh, this is weird, but reusing code from Model Dashboard
        const modelData = { name: selectedModel[0].name }
        const datasetData = { name: selectedModel[0].dataset_name }
        const pronDictData = { name: selectedModel[0].pron_dict_name }
        modelLoad(modelData, datasetData, pronDictData)
    }

    render = () => {
        const { t, currentEngine, filename, list, status, stage_status, text, modelName } = this.props;

        //Only show trained models
        const listTrained = list.filter(model => model.status === 'trained')
        const listOptions = listTrained.map(model => ({
            "key": model.name,
            "value": model.name,
            "text": model.name
        }))

        // prevent the buttons from being clicked if we haven't got an active model, or file to transcribe
        let enableTranscription = (modelName && filename &&
            (status == 'ready' || status == 'transcribed' )) ? true : false

        const loadingIcon = (status == 'transcribing') ? (
            <Icon name='circle notched' size="big" loading />
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
                            <Header as='h1' text="true">
                                { t('transcription.new.title') }
                            </Header>

                            {modelName &&
                            <CurrentModelName/>
                            }

                            <Segment>
                                {listOptions &&
                                    <Form.Field>
                                    <label className="pad-right">{t('transcription.new.selectModelLabel')}</label>
                                        <Dropdown
                                            placeholder={t('common.choose')}
                                            selection
                                            name="model_name"
                                            options={listOptions}
                                            defaultValue={modelName ? modelName : ''}
                                            onChange={this.handleSelectModel} />
                                    </Form.Field>
                                }
                            </Segment>

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
                                            <Button>{t('transcription.new.uploadButton')}</Button>
                                        </div>
                                    );
                                } }
                            </Dropzone>

                            {filename &&
                                <Segment>{t('transcription.new.usingAudio', { filename })} </Segment>
                            }

                            <Segment>
                                <Button onClick={this.handleTranscribe} disabled={!enableTranscription} >
                                    {t('transcription.new.transcribe')}
                                </Button>
                            </Segment>

                            <Message icon>
                                { loadingIcon }
                                <Message.Content>
                                    <Message.Header>{t('status.' + status)}</Message.Header>
                                    {stage_status &&
                                    <div className="stages">
                                        {Object.keys(stage_status).map((stage, i) => {
                                                let name = stage_status[stage]["name"]
                                                let status = stage_status[stage]["status"]
                                                let message = stage_status[stage]["message"]
                                                return (
                                                    <p key={stage} className="stage">
                                                        <span className="name">{t('transcription.engines.' + currentEngine + '.stages.' + name)}</span>
                                                        <span className="divider">{status && <>|</>}</span>
                                                        <span className="status">{t('status.' + status)}</span>
                                                        <span className="divider">{message && <>|</>}</span>
                                                        <span className="message">{message}</span>
                                                    </p>
                                                )
                                            }
                                        )}
                                    </div>
                                    }
                                </Message.Content>
                            </Message>

                            {status=='transcribed' &&
                                <Segment>
                                    <p>{text}</p>

                                    <p className="label pad-right">{t('transcription.results.downloadLabel')}</p>
                                    <Button onClick={this.handleDownloadText}>
                                        {t('transcription.results.downloadTextButton')}
                                    </Button>
                                    <Button onClick={this.handleDownloadElan}>
                                        {t('transcription.results.downloadElanButton')}
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
        list: state.model.modelList,
        modelName: state.model.name,
        filename: state.transcription.filename,
        status: state.transcription.status,
        stage_status: state.transcription.stage_status,
        text: state.transcription.text,
        elan: state.transcription.elan,
        currentEngine: state.engine.engine
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
                // So we can safely request the text and elan files here
                dispatch(transcriptionGetText())
                dispatch(transcriptionGetElan())
            })
    },
    transcriptionStatus: () => {
        dispatch(transcriptionStatus())
            .then(response => console.log(response))
    },
    transcriptionGetText: () => {
        dispatch(transcriptionGetText())
    },
    transcriptionGetElan: () => {
        dispatch(transcriptionGetElan())
    },
    modelList: () => {
        dispatch(modelList())
    },
    modelLoad: (modelData, datasetData, pronDictData) => {
        dispatch(modelLoad(modelData))
            .then(response => dispatch(datasetLoad(datasetData)))
            .then(response => dispatch(pronDictLoad(pronDictData)))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(NewTranscription)
);
