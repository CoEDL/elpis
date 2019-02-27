import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Card, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import downloadjs from 'downloadjs'
import { transcriptionElan } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentModelName from "components/Steps/Model/CurrentModelName";

class NewTranscriptionResults extends Component {

    handleElanBuild = () => {
        const { transcriptionElan } = this.props
        transcriptionElan()
    }

    handleElanDownload = () => {
        const { elan } = this.props
        downloadjs(elan, 'elan.eaf', 'text/xml');

    }

    render() {
        const { t, elan, name, audioFile } = this.props;
        console.log("elan", elan)
        console.log("audioFile", audioFile)

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>

                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1' text='true'>
                                { t('transcription.results.title') }
                            </Header>

                            <CurrentModelName name={ name } />

                            <p>{ t('transcription.results.usingAudio') } { audioFile } </p>

                            <Card fluid>
                                <Card.Content header={ t('transcription.results.errorLogHeader') } />
                                <Card.Content description='Were there any errors? Just output the log, nothing fancy' />
                            </Card>

                            <Card fluid>
                                <Card.Content header={ t('transcription.results.resultsHeader') } />
                                <Card.Content description='Blah Blah Blah Blah Blah' />
                            </Card>

                            <Divider />

                            <Button onClick={ this.handleElanBuild }>
                                Build Elan
                            </Button>

                            <Button onClick={ this.handleElanDownload }>
                                Download Elan
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
        name: state.model.name,
        elan: state.transcription.elan,
        audioFile: state.transcription.audioFile
    }
}

const mapDispatchToProps = dispatch => ({
    transcriptionElan: () => {
        dispatch(transcriptionElan())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(NewTranscriptionResults))
