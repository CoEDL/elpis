import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepWelcome extends Component {
    render() {
        return (
            <div>
                <Grid centered row={6}>
                    <Grid.Row centered>
                        <StepBranding />
                    </Grid.Row>

                    <Grid.Row centered>

                        <Segment>
                            <Button as={Link} to="/naming">Build New Model</Button>
                            <Button as={Link} to="/new-transcription">New Transcription</Button>
                        </Segment>
                    </Grid.Row>

                    <Grid.Row centered>

                            <Container >
                                <Segment>
                                    <Header as='h2'>Instructional Video</Header>
                                    <p>
                                        Friendly welcome message :-)
                                    </p>
                                </Segment>
                            </Container>

                    </Grid.Row>

                    <Grid.Row centered>
                        <StepInformer instructions={NewModelInstructions} />
                    </Grid.Row>

                </Grid>
            </div>
        );
      }
}