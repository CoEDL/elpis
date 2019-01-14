import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, List, Button} from 'semantic-ui-react';

export default class StepDataPreperation extends Component {
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
                                    <Header as='h1' text textAlign='center'>  <Icon name='train' />Data prepatation success, Overview of training corpus</Header>
                                    <p>Banner Message: text has been cleaned and normalised OK</p>   
                                    <p>Describe what has just happened for the novice user to better understand</p>   
    
                                    
                                   <Grid>
                                        <Grid.Column width={5}>
                                        <Header as='h1' text> Wordlist</Header>
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
                                        <Header as='h1' text> Frequency</Header>
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
                                    
                                    
                                    <Button type='submit' onClick={()=> {this.props.toStepBuildDictionary()}}>Next:build letter to sound</Button>
                                </Grid.Column>
                           
                        </Grid>  
                    </Segment>
                    <Button onClick={()=>{this.props.goBack()}}>Back</Button>
                </div>
        );
    }
}