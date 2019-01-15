import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'

export default class StepWelcome extends Component {
    render() {
        return (
            <div>
                <Grid centered row={6}>    
                    <Grid.Row centered>
                        <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <Segment>
                            <Button as={Link} to="/naming">Build New Model</Button>
                            <Button as={Link} to="/new-transcription">New Transcription</Button>
                        </Segment>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <Segment> 
                            <Container text>
                                <Header as='h2'>Instructional Video/Lorum</Header>
                                <p>
                                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Pariatur reprehenderit voluptas recusandae iusto deleniti eaque sunt, consectetur, rerum, dicta laboriosam porro molestias optio officiis minus nemo ex qui! Quas, velit.
                                </p>
                            </Container>
                        </Segment>
                    </Grid.Row>
    
                    <Grid.Row centered>
                            <AccordionFluid title={'Step 1'} active/>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <AccordionFluid title={'Step 2'}/>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <AccordionFluid title={'Step 3'}/>
                    </Grid.Row>
    
                </Grid>
            </div>
        );
      }
}