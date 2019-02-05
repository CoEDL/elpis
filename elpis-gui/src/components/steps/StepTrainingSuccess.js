import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Button, Table, Modal } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import AccordionFluid from '../SemanticsComponents/AccordionFluid';
import { translate } from 'react-i18next';

class StepTrainingSuccess extends Component {

    state = { open: false }

    open = () => this.setState({ open: true })
    close = () => this.setState({ open: false })

    render() {
        const { open } = this.state
        const { t } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 5 }>
                            <StepInformer instructions={ NewModelInstructions } />
                        </Grid.Column>

                        <Grid.Column width={ 11 }>
                            <Header as='h1' text='true'>
                                { t('trainingModelSuccess.title') }
                            </Header>

                            <Table celled padded>
                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid title={ 'English-Indonesian 1-gram  WER:6 INS:2 SUB:1 DEL:3' } />
                                        </Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid active title={ 'The one that just finished  WER:12 INS:3 SUB:X DEL:X' } />
                                        </Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid title={ 'English-Indonesian 3-gram  WER:X INS:X SUB:X DEL:X' } />
                                        </Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid title={ 'English-Indonesian 5-gram with Indonesian 12s  WER:X INS:X SUB:X DEL:X' } />
                                        </Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid title={ 'Indonesian 1-gram  WER:X INS:X SUB:X DEL:X' } />
                                        </Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>
                                            <AccordionFluid title={ 'Everything 3-gram with Indonesian 12s WER:X INS:X SUB:X DEL:X' } />
                                        </Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            </Table>

                            <Divider />

                            <Modal
                                trigger={ <Button>{ t('trainingModelSuccess.downloadButton') }</Button> }
                                basic size='small'
                                open={ open }
                                onOpen={ this.open }
                                onClose={ this.close }
                            >
                                <Header icon='archive' content={ t('trainingModelSuccess.downloadModalHeader') } />
                                <Modal.Content>
                                    <p>
                                        { t('trainingModelSuccess.downloadModalContent') }
                                    </p>
                                </Modal.Content>
                                <Modal.Actions>
                                    <Button color='green' inverted onClick={ this.close }>
                                        <Icon name='checkmark' />
                                        { t('trainingModelSuccess.downloadOkButton') }
                                    </Button>
                                </Modal.Actions>
                            </Modal>

                            <Divider />

                            <Button as={ Link } to="/new-transcription">
                                { t('trainingModelSuccess.newTranscribeButton') }
                            </Button>
                        </Grid.Column>

                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepTrainingSuccess)
