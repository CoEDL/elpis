import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Divider, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { modelPronunciation } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelPronunciationDictionary extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        this.props.modelPronunciation(formData);
    }

    render() {
        const { t, pronunciation } = this.props;

        const pron = pronunciation ? (
            <Segment>
                <pre>
                    {pronunciation}
                </pre>
            </Segment>

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
                            <Header as='h1'>
                                { t('model.pronDict.title') }
                            </Header>

                            <p>
                                { t('model.pronDict.description') }
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
                                                    <p>{ t('model.pronDict.dropFilesHintDragActive') } </p>
                                                ) : (<p>{ t('model.pronDict.dropFilesHint') }</p>)
                                            }
                                        </div>
                                    );
                                } }
                            </Dropzone>

                            { pron }

                            <Divider />

                            <Button type='submit' as={ Link } to="/model/lexicon">
                                { t('model.pronDict.nextButton') }
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
        pronunciation: state.model.pronunciation,
    }
}

const mapDispatchToProps = dispatch => ({
    modelPronunciation: postData => {
        dispatch(modelPronunciation(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelPronunciationDictionary));
