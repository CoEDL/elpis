import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepNewTranscription extends Component {
    render() {
        const { t } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer instructions={ NewModelInstructions } />
                        </Grid.Column>

                        <Grid.Column width={ 10 }>
                            <Header as='h1' text="true">
                                { t('newTranscription.title') }
                            </Header>

                            <Segment placeholder>
                                <Header icon>
                                    <Icon name='file audio outline' />
                                    { t('newTranscription.dropHint') }
                                </Header>
                                <Button primary>{ t('newTranscription.addAudioButton') }</Button>
                            </Segment>

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
export default translate('common')(StepNewTranscription)
