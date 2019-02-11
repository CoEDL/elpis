import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Divider, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer from '../StepInformer';
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';
import { updateModelPronunciationFile } from '../../redux/actions';
import { connect } from 'react-redux';
import classNames from "classnames";

class StepBuildPronunciationDictionary extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.updateModelPronunciationFile(formData);
    }

    render() {
        const { t, pronunciationFile } = this.props;

        const pronFile = pronunciationFile ?
            pronunciationFile + ' uploaded OK'
            : null

        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer />
                        </Grid.Column>
                        <Grid.Column width={ 10 }>
                            <Header as='h1'>
                                { t('buildPron.title') }
                            </Header>

                            <p>
                                { t('buildPron.description') }
                            </p>

                            <Divider />

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
                                                    <p>{ t('buildPron.dropFilesHintDragActive') } </p>
                                                ) : (<p>{ t('buildPron.dropFilesHint') }</p>)
                                            }
                                        </div>
                                    );
                                } }
                            </Dropzone>

                            <p>
                                { pronFile }
                            </p>

                            <Divider />

                            <Button type='submit' as={ Link } to="/model-settings">
                                { t('buildPron.nextButton') }
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
        pronunciationFile: state.model.pronunciationFile,
    }
}

const mapDispatchToProps = dispatch => ({
    updateModelPronunciationFile: postData => {
        dispatch(updateModelPronunciationFile(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(StepBuildPronunciationDictionary));
