import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import FileUpload from '../FileuploadComponents/FileUpload';
import { translate } from 'react-i18next';
import { connect } from 'react-redux';

class StepAddData extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {

        const { t, audioFiles, transcriptionFiles, additionalTextFiles } = this.props;
        const audioFileList = audioFiles.map(file => (
            <List.Item key={file}>
                <List.Content>{file}</List.Content>
            </List.Item>
        ))
        const transcriptionFilesList = transcriptionFiles.map(file => (
            <List.Item key={file}>
                <List.Content>{file}</List.Content>
            </List.Item>
        ))
        const additionalTextFilesList = additionalTextFiles.map(file => (
            <List.Item key={file}>
                <List.Content>{file}</List.Content>
            </List.Item>
        ))

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
                                <FileUpload />
                            </Segment>

                            <Header as='h1'>
                                { t('addData.filesHeader') }
                            </Header>
                            <Grid>
                                <Grid.Column width={ 5 }>
                                    <List>
                                        { audioFileList }
                                    </List>
                                </Grid.Column>

                                <Grid.Column width={ 5 }>
                                    <List>
                                        { transcriptionFilesList }
                                    </List>
                                </Grid.Column>
                            </Grid>

                            <Grid container>
                                <Button type='submit' as={ Link } to="/data-preparation">
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
        additionalTextFiles: state.model.additionalTextFiles
    }
}

export default connect(mapStateToProps)(translate('common')(StepAddData));
