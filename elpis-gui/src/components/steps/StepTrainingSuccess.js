import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Button, Table, Modal } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import AccordionFluid from '../Semantics Components/AccordionFluid';

export default class StepTrainingSuccess extends Component {

    state = { open: false }

    open = () => this.setState({ open: true })
    close = () => this.setState({ open: false })

    render() {
        const { open } = this.state
        return (
            <div>
                <StepBranding />
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


                                <Modal
                                trigger={<Button>Download a bundle of the model, settings and information about training data</Button>}
                                basic size='small'
                                open={open}
                                onOpen={this.open}
                                onClose={this.close}
                                >
                                        <Header icon='archive' content='Your files and settings are being compiled' />
                                        <Modal.Content>
                                        <p>
                                            Click Save on your browser's download dialog
                                        </p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                        <Button color='green' inverted onClick={this.close}>
                                            <Icon name='checkmark' /> Ok
                                        </Button>
                                        </Modal.Actions>
                                </Modal>

                                <Button as={Link} to="/new-transcription">Use the model to transcribe new audio</Button>
                            </Grid.Column>

                    </Grid>
                </Segment>
            </div>
        );
    }
}