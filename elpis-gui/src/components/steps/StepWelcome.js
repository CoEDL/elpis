import React, { Component } from 'react';
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'

export default class StepWelcome extends Component {
    // constructor(props) {
    //     super(props);
    // }
    // render() {
    //     return <div>
    //         <Button onClick={() => this.props.toStepNaming()}>Build Model</Button>
    //     </div>;
    // }

    render() {
        return (
            <div>
                <Grid centered row={6}>    
                    <Grid.Row centered>
                        <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <Segment>
                            <Button>Build New Model</Button>
                            <Button>New Transcription</Button>
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
                            <AccordionFluid title={'Step 1'}/>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <AccordionFluid title={'Step 2'}/>
                    </Grid.Row>
    
                    <Grid.Row centered>
                        <AccordionFluid title={'Step 3'}/>
                    </Grid.Row>
    
                </Grid>
            </div>
        )
      }
}