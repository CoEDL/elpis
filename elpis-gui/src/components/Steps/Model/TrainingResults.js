import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Icon, Button, Table, Modal } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelTrainingResults extends Component {

    state = { open: false }

    open = () => this.setState({ open: true })
    close = () => this.setState({ open: false })

    render() {
        const { open } = this.state
        const { t } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text='true'>
                                { t('model.trainingResults.title') }
                            </Header>

                            <p>
                                { t('model.trainingResults.description') }
                            </p>

                            <Table celled padded sortable>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell>sort by Date</Table.HeaderCell>
                                        <Table.HeaderCell>Name</Table.HeaderCell>
                                        <Table.HeaderCell>WER</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>2019 Jan 20</Table.Cell>
                                        <Table.Cell>Abui 1-gram</Table.Cell>
                                        <Table.Cell>WER:6 INS:2 SUB:1 DEL:3</Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>2019 Jan 18</Table.Cell>
                                        <Table.Cell>The one that just finished</Table.Cell>
                                        <Table.Cell>WER:12 INS:3 SUB:X DEL:X</Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>2018 Dec 31</Table.Cell>
                                        <Table.Cell>Abui 3-gram</Table.Cell>
                                        <Table.Cell>WER:X INS:X SUB:X DEL:X</Table.Cell>
                                    </Table.Row>

                                    <Table.Row>
                                        <Table.Cell>2018 Nov 8</Table.Cell>
                                        <Table.Cell>Abui 5-gram</Table.Cell>
                                        <Table.Cell>WER:X INS:X SUB:X DEL:X</Table.Cell>
                                    </Table.Row>

                                </Table.Body>
                            </Table>

                            <Divider />

                            <Modal
                                trigger={ <Button>{ t('model.trainingResults.downloadButton') }</Button> }
                                basic size='small'
                                open={ open }
                                onOpen={ this.open }
                                onClose={ this.close }
                            >
                                <Header icon='archive' content={ t('model.trainingResults.downloadModalHeader') } />
                                <Modal.Content>
                                    <p>
                                        { t('model.trainingResults.downloadModalContent') }
                                    </p>
                                </Modal.Content>
                                <Modal.Actions>
                                    <Button color='green' inverted onClick={ this.close }>
                                        <Icon name='checkmark' />
                                        { t('model.trainingResults.downloadOkButton') }
                                    </Button>
                                </Modal.Actions>
                            </Modal>

                            <Divider />

                            <Button as={ Link } to="/transcription/new">
                                { t('model.trainingResults.newTranscribeButton') }
                            </Button>
                        </Grid.Column>

                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(ModelTrainingResults)
