import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepNewTranscription extends Component {
    render() {
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                            <Grid.Column width={6}>
                                <StepInformer instructions={NewModelInstructions} />
                            </Grid.Column>

                            <Grid.Column width={10}>
                                <Header as='h1' > <Icon name='computer' />Transcribe some audio with an exisiting model</Header>

                                <Segment placeholder>
                                    <Header icon>
                                    <Icon name='file audio outline' />
                                    Drag and drop audio and transcription files here
                                    </Header>
                                    <Button primary>Add Document</Button>
                                </Segment>

                                <Header as='h1' > Choose a model</Header>
                               <Grid>
                                    <Grid.Column>
                                        <List>
                                            <List.Item>
                                                <List.Icon name='square outline'/>
                                                <List.Content>English-Indonesian 1-gram</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='square outline'/>
                                                <List.Content>English-Indonesian 3-gram</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='square outline'/>
                                                <List.Content>English-Indonesian 5-gram with Indonesian 12s</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='square outline'/>
                                                <List.Content>Indoesian 1-gram</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='square outline'/>
                                                <List.Content>Everything 3-gram with Indonesian 12s</List.Content>
                                            </List.Item>
                                        </List>
                                    </Grid.Column>
                                </Grid>

                                <Button type='submit' as={Link} to="/transcription-results">Go</Button>
                            </Grid.Column>

                    </Grid>
                </Segment>
            </div>
        );
    }
}