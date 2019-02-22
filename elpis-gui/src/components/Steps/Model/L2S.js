import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Divider, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { modelL2S } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelL2S extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        const { modelL2S } = this.props
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        modelL2S(formData);
    }

    render() {
        const { t, l2s } = this.props;
        console.log("l2s", l2s)
        const pron = l2s ? (
            <Segment>
                <pre>
                    {l2s}
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
        l2s: state.model.l2s,
    }
}

const mapDispatchToProps = dispatch => ({
    modelL2S: postData => {
        dispatch(modelL2S(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelL2S));
