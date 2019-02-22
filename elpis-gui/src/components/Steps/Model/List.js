import React, { Component } from 'react';
import { Grid, Header, List, Segment, Icon, Button, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelList } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelList extends Component {
    componentDidMount() {
        const { modelList } = this.props
        modelList()
    }

    render() {
        const { t, list } = this.props;

        const listEl = list.length > 0 ? (
            <Table celled collapsing>
                <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Name</Table.HeaderCell>
                    <Table.HeaderCell>WER</Table.HeaderCell>
                    <Table.HeaderCell>DEL</Table.HeaderCell>
                    <Table.HeaderCell>INS</Table.HeaderCell>
                    <Table.HeaderCell>SUB</Table.HeaderCell>
                </Table.Row>
                </Table.Header>
                <Table.Body>
            {
                list.map( model => {
                    return (
                    <Table.Row key={ model.name }>
                        <Table.Cell>{ model.name }</Table.Cell>
                        <Table.Cell>{ model.results.wer }</Table.Cell>
                        <Table.Cell>{ model.results.del }</Table.Cell>
                        <Table.Cell>{ model.results.ins }</Table.Cell>
                        <Table.Cell>{ model.results.sub }</Table.Cell>
                    </Table.Row>
                )})
            }
            </Table.Body>
            </Table>
    ) : <p>{ t('model.list.noneMessage') }</p>

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1'>
                                { t('model.list.title') }
                            </Header>

                            { listEl }

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.model.modelList
    }
}

const mapDispatchToProps = dispatch => ({
    modelList: () => {
        dispatch(modelList())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelList))
