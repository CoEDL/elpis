import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { transcriptionNew } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class NewTranscription extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.transcriptionNew(formData);
    }

    render() {
        const { t } = this.props;
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

                            newTranscriptionFile: {this.props.newTranscriptionFile}


                            <Header as='h1' type="text">{ t('transcription.new.chooseModelHeader') }</Header>
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
                                            <List.Content>Indonesian 1-gram</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='square outline' />
                                            <List.Content>Everything 3-gram with Indonesian 12s</List.Content>
                                        </List.Item>
                                    </List>
                                </Grid.Column>
                            </Grid>

                            <Divider />

                            <Button as={ Link } to="/transcription/results">
                                { t('transcription.new.nextButton') }
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
    transcriptionNew: postData => {
        dispatch(transcriptionNew(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewTranscription));
