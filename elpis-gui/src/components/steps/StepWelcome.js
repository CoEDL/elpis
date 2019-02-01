import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepWelcome extends Component {
    render() {
        return (
            <div>
                <Grid centered row={6}>
                    <Grid.Row centered>
                        <Header as='h1'><img src="https://github.com/CoEDL/elpis/raw/master/docs/img/elpis.png" className="logo" alt="logo" /></Header>
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
                                    <Header as='h2'>Instructional Video/Lorum</Header>
                                    <p>
                                        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Pariatur reprehenderit voluptas recusandae iusto deleniti eaque sunt, consectetur, rerum, dicta laboriosam porro molestias optio officiis minus nemo ex qui! Quas, velit.
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