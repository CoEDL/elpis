import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import StepBranding from './StepBranding';
import StepInformer from '../StepInformer';
import { translate } from 'react-i18next';
import { updateNewTranscriptionFile } from '../../redux/actions';
import { connect } from 'react-redux';
import classNames from "classnames";

class StepNewTranscription extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.updateNewTranscriptionFile(formData);
    }

    render() {
        const { t } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer />
                        </Grid.Column>

                        <Grid.Column width={ 10 }>
                            <Header as='h1' text="true">
                                { t('newTranscription.title') }
                            </Header>


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
                                                    <p>{ t('newTranscription.dropFilesHintDragActive') } </p>
                                                ) : (<p>{ t('newTranscription.dropFilesHint') }</p>)
                                            }
                                        </div>
                                    );
                                } }
                            </Dropzone>

                            newTranscriptionFile: {this.props.newTranscriptionFile}


                            <Header as='h1' type="text">{ t('newTranscription.chooseModelHeader') }</Header>
                            <Grid>
                                <Grid.Column>
                                    <List>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>English-Indonesian 1-gram</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>English-Indonesian 3-gram</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>English-Indonesian 5-gram with Indonesian 12s</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>Indoesian 1-gram</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>Everything 3-gram with Indonesian 12s</List.Content>
                                        </List.Item>
                                    </List>
                                </Grid.Column>
                            </Grid>

                            <Divider />

                            <Button type='submit' as={ Link } to="/transcription-results">
                                { t('newTranscription.nextButton') }
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
        newTranscriptionFile: state.model.newTranscriptionFile
    }
}

const mapDispatchToProps = dispatch => ({
    updateNewTranscriptionFile: postData => {
        dispatch(updateNewTranscriptionFile(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(StepNewTranscription));
