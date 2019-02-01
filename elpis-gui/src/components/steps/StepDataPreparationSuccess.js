import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button} from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepDataPreperation extends Component {
    render() {
        return (
                <div>
                    <Header as='h1'><img src="https://github.com/CoEDL/elpis/raw/master/docs/img/elpis.png" className="logo" alt="logo" /></Header>
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={6}>
                                    <StepInformer instructions={NewModelInstructions} />
                                </Grid.Column>
                                <Grid.Column width={10}>
                                    <Header as='h1'><Icon name='train' />Data preparation success</Header>
                                    <h2>Overview of training corpus</h2>
                                    <p>Banner Message: text has been cleaned and normalised OK</p>
                                    <p>Describe what has just happened for the novice user to better understand</p>
                                   <Grid>
                                        <Grid.Column width={5}>
                                        <Header as='h1' > Wordlist</Header>
                                            <List>
                                                <List.Item>
                                                    <List.Content>a</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>alphabet</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>Am</List.Content>
                                                </List.Item>
                                            </List>
                                        </Grid.Column>
                                        <Grid.Column width={5}>
                                            <Header as='h1' > Frequency</Header>
                                            <List>
                                                <List.Item>
                                                    <List.Content>21</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>77</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>84</List.Content>
                                                </List.Item>
                                            </List>
                                        </Grid.Column>
                                    </Grid>
                                    <Button type='submit' as={Link} to="/build-pronunciation-dictionary">Next: build letter to sound</Button>
                                </Grid.Column>
                        </Grid>
                    </Segment>
                </div>
        );
    }
}