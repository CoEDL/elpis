import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Card, Button } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class NewTranscriptionResults extends Component {
    render() {
        const { t } = this.props;
        // TODO get this from redux?
        const modelName = "English-Indonesian 5-gram with Indonesian 12s"
        const audioName = "some-audio.wav"

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

                            <p>{ t('transcription.results.usingModel', { modelName }) } </p>
                            <p>{ t('transcription.results.usingAudio', { audioName }) } </p>

                            <Card fluid>
                                <Card.Content header={ t('transcription.results.errorLogHeader') } />
                                <Card.Content description='Were there any errors? Just output the log, nothing fancy' />
                            </Card>

                            <Card fluid>
                                <Card.Content header={ t('transcription.results.resultsHeader') } />
                                <Card.Content description='Blah Blah Blah Blah Blah' />
                            </Card>

                            <Divider />

                            <Button as={ Link } to="/">
                                { t('transcription.results.downloadElanButton') }
                            </Button>

                            <Button as={ Link } to="/">
                                { t('transcription.results.downloadPraatButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(NewTranscriptionResults)
