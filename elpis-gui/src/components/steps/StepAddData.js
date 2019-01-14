import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';

export default class StepAddData extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>

                <Segment>
                    <Grid centered>
                            <Grid.Column width={6}>
                                <AccordionFluid title={'Step 1'}/>
                                <AccordionFluid title={'Step 2'}/>
                                <AccordionFluid title={'Step 3'}/>
                            </Grid.Column>

                            <Grid.Column width={10}>
                                <Header as='h1' text> <Icon name='book' />Add Data</Header>
                                <p>Some description and information about file formats, naming requirements etc.</p>   

                                <Segment placeholder>
                                    <Header icon>
                                    <Icon name='file audio outline' />
                                    Drag and drop audio and transcription files here
                                    </Header>
                                    <Button primary>Add Document</Button>
                                </Segment>

                                <Header as='h1' text> Transcription and Audio Files</Header>
                               <Grid>
                                    <Grid.Column width={5}>
                                        <List>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File1.eaf</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File2.eaf</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File3.eaf</List.Content>
                                            </List.Item>
                                        </List>
                                    </Grid.Column>

                                    <Grid.Column width={5}> 
                                    <List>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File1.wav</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File2.wav</List.Content>
                                            </List.Item>
                                            <List.Item>
                                                <List.Icon name='check square'/>
                                                <List.Content>File3.wav</List.Content>
                                            </List.Item>
                                        </List>
                                    </Grid.Column>
                                </Grid>
                                
                                <Button type='submit' onClick={()=> {this.props.toStepDataPreparation()}}>Next:process this data</Button>
                            </Grid.Column>
                       
                    </Grid>  
                </Segment>
                <Button onClick={()=>{this.props.goBack()}}>Back</Button>
            </div>
        );
    }
}