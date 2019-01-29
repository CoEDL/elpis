import React, { Component } from 'react';
import { Link } from "react-router-dom";
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { Grid, Header, Segment, Icon, Button, Table } from 'semantic-ui-react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid';

export default class StepTrainingSuccess extends Component {
    render() {
        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>

                <Segment>
                    <Grid centered>
                            <Grid.Column width={5}>
                                <StepInformer instructions={NewModelInstructions} />
                            </Grid.Column>

                            <Grid.Column width={11}>
                                <Header as='h1' text='true'> <Icon name='graduation cap' /> Trained Model Success </Header>
                            
                                <Table celled padded>
                                    <Table.Body>
                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'English-Indonesian 1-gram  WER:6 INS:2 SUB:1 DEL:3'}/>
                                            </Table.Cell>
                                        </Table.Row>

                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'The one that just finished  WER:12 INS:3 SUB:X DEL:X'}/>
                                            </Table.Cell>
                                        </Table.Row>

                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'English-Indonesian 3-gram  WER:X INS:X SUB:X DEL:X'}/>
                                            </Table.Cell>
                                        </Table.Row>

                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'English-Indonesian 5-gram with Indonesian 12s  WER:X INS:X SUB:X DEL:X'}/>
                                            </Table.Cell>
                                        </Table.Row>

                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'Indonesian 1-gram  WER:X INS:X SUB:X DEL:X'}/>
                                            </Table.Cell>
                                        </Table.Row>

                                        <Table.Row>
                                            <Table.Cell>
                                                <AccordionFluid title={'Everything 3-gram with Indonesian 12s WER:X INS:X SUB:X DEL:X'}/>
                                            </Table.Cell>
                                        </Table.Row>
                                    </Table.Body>
                                </Table>

                                <Button onClick={()=>{}}>Download a bundle of the model, settings and information about training data</Button>
                                <Button as={Link} to="/new-transcription">Use the model to transcribe new audio</Button>
                            </Grid.Column>
                       
                    </Grid>  
                </Segment>
            </div>
        );
    }
}