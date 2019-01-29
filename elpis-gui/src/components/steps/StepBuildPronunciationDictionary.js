import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button } from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepBuildPronunciationDictionary extends Component {
    render() {
        return (
            <div>
                    <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={6}>
                                    <StepInformer instructions={NewModelInstructions} />
                                </Grid.Column>
                                <Grid.Column width={10}>
                                    <Header as='h1' text textAlign='center'>  <Icon name='train' />Build the pronunciation dictionary</Header>
                                    <Grid>
                                        <Grid.Column width={2}>
                                            <List size='big'>
                                                <List.Item>
                                                    <List.Content>a<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>b<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>t<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>k<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>g<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>ng<List.Icon name='check square outline' /></List.Content>
                                                </List.Item>
                                            </List>
                                        </Grid.Column>
                                        <Grid.Column width={8}> 
                                            <div>
                                                <Segment vertical>Te eum doming eirmod, nominati pertinacia argumentum ad his.</Segment>
                                                <Segment vertical>Pellentesque habitant morbi tristique senectus.</Segment>
                                                <Segment vertical>Eu quo homero blandit intellegebat. Incorrupte consequuntur mei id.</Segment>
                                            </div>
                                        </Grid.Column>
                                    </Grid>
                                    <Button type='submit' as={Link} to="/model-settings">Next: model settings</Button>
                                </Grid.Column>
                        </Grid>  
                    </Segment>
                </div>
        );
    }
}