import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Checkbox, Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { replaceFiles, triggerApiWaiting } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import FileUpload from './FileUpload';

class DataBundleAddFiles extends Component {

    handleFilesReplaceToggle = () => {
        this.props.replaceFiles()
    }

    handleNextButton = () => {
        this.props.triggerApiWaiting('data preparation')
        this.props.history.push('/data-bundle/preparation')
    }

    render() {

        const { t, audioFiles, transcriptionFiles, additionalTextFiles, replace } = this.props;

        const audioFileList = audioFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const transcriptionFilesList = transcriptionFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const additionalTextFilesList = additionalTextFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))

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
                                { t('dataBundle.addFiles.title') }
                            </Header>

                            <p>
                                { t('dataBundle.addFiles.description') }
                            </p>

                            <Segment>
                                <Checkbox
                                    toggle
                                    onChange={ this.handleFilesReplaceToggle }
                                    defaultChecked={ replace }
                                    label={ t('dataBundle.addFiles.filesReplaceLabel') }
                                />
                            </Segment>

                            <Segment>
                                <FileUpload />
                            </Segment>

                            <Header as='h1'>
                                { t('dataBundle.addFiles.filesHeader') }
                            </Header>

                            <Grid columns={ 3 }>
                                <Grid.Column>
                                    <List>
                                        { audioFileList }
                                    </List>
                                </Grid.Column>

                                <Grid.Column>
                                    <List>
                                        { transcriptionFilesList }
                                    </List>
                                </Grid.Column>

                                <Grid.Column>
                                    <List>
                                        { additionalTextFilesList }
                                    </List>
                                </Grid.Column>
                            </Grid>

                            <Grid container>
                                <Button type='submit' onClick={ this.handleNextButton }>
                                    { t('dataBundle.addFiles.nextButton') }
                                </Button>
                                <Button type='submit' as={ Link } to="/data-bundle/preparation/error" icon>
                                    <Icon name='warning sign' />
                                    { t('dataBundle.addFiles.nextButtonError') }
                                </Button>
                            </Grid>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}


const mapStateToProps = state => {
    return {
        audioFiles: state.dataBundle.audioFiles,
        transcriptionFiles: state.dataBundle.transcriptionFiles,
        additionalTextFiles: state.dataBundle.additionalTextFiles,
        replace: state.dataBundle.replaceFiles
    }
}

const mapDispatchToProps = dispatch => ({
    replaceFiles: () => {
        dispatch(replaceFiles());
    },
    triggerApiWaiting: message => {
        dispatch(triggerApiWaiting(message));
    }
})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(DataBundleAddFiles)
    )
);
