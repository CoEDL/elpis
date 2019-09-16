import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Divider, Grid, Header, Message, Segment } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { pronDictL2S } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentPronDictName from "./CurrentPronDictName";
import urls from 'urls'

class PronDictL2S extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        const { pronDictL2S } = this.props
        var formData = new FormData();
        formData.append('file', acceptedFiles[0]);
        pronDictL2S(formData);
    }

    render() {
        const { t, l2s } = this.props;
        console.log("l2s", l2s)
        const pron = l2s ? (
            <Segment>
                <pre>
                    { l2s }
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
                                { t('pronDict.l2s.title') }
                            </Header>

                            <CurrentPronDictName />

                            <Message content={ t('pronDict.l2s.description') } />

                            { ! pron &&
                                <Segment>
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
                                                            <p>{ t('pronDict.l2s.dropFilesHintDragActive') } </p>
                                                        ) : (<p>{ t('pronDict.l2s.dropFilesHint') }</p>)
                                                    }
                                                    <Button>{t('pronDict.l2s.uploadButton')}</Button>
                                                </div>
                                            );
                                        } }
                                    </Dropzone>
                                </Segment>
                            }

                            {pron &&
                                <Segment>
                                    { pron }
                                </Segment>
                            }

                            <Button as={Link} to={urls.gui.pronDict.lexicon}>
                                {t('common.nextButton')}
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
        l2s: state.pronDict.l2s,
        name: state.pronDict.name,
    }
}

const mapDispatchToProps = dispatch => ({
    pronDictL2S: postData => {
        dispatch(pronDictL2S(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(PronDictL2S));
