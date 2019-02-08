import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Checkbox, Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import FileUpload from '../FileuploadComponents/FileUpload';
import { translate } from 'react-i18next';
import { connect } from 'react-redux';
import { setFilesOverwrite } from '../../redux/actions';
import { triggerApiWaiting } from '../../redux/actions';

class StepAddData extends Component {

    handleFilesOverwriteToggle = () => {
        this.props.setFilesOverwrite()
    }

    handleNextButton = () => {
        this.props.triggerApiWaiting('data preparation')
        this.props.history.push('/data-preparation')
    }

    render() {

        const { t, audioFiles, transcriptionFiles, additionalTextFiles, filesOverwrite } = this.props;
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

        console.log('filesOverwrite', filesOverwrite)

        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer instructions={ NewModelInstructions } />
                        </Grid.Column>

                        <Grid.Column width={ 10 }>
                            <Header as='h1'>
                                { t('addData.title') }
                            </Header>

                            <p>
                                { t('addData.description') }
                            </p>

                            <Segment>
                                <Checkbox
                                    toggle
                                    onChange={this.handleFilesOverwriteToggle}
                                    defaultChecked={filesOverwrite}
                                    label={t('addData.filesOverwriteLabel') }
                                    />
                            </Segment>

                            <Segment>
                                <FileUpload />
                            </Segment>

                            <Header as='h1'>
                                { t('addData.filesHeader') }
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
                                <Button type='submit' onClick={this.handleNextButton}>
                                    { t('addData.nextButton') }
                                </Button>
                                <Button type='submit' as={ Link } to="/data-preparation-error" icon>
                                    <Icon name='warning sign' />
                                    { t('addData.nextButtonError') }
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
        audioFiles: state.model.audioFiles,
        transcriptionFiles: state.model.transcriptionFiles,
        additionalTextFiles: state.model.additionalTextFiles,
        filesOverwrite: state.model.filesOverwrite
    }
}

const mapDispatchToProps = dispatch => ({
    setFilesOverwrite: () => {
        dispatch(setFilesOverwrite());
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
        translate('common')(StepAddData)
    )
);
