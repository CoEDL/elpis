import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Grid, Header, Segment, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import arraySort from 'array-sort'
import { datasetPrepare } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentDatasetName from "./CurrentDatasetName";
import urls from 'urls'

class DatasetPrepare extends Component {

    state = {
        column: null,
        reverse: false
    }

    componentDidMount() {
        const {name, datasetPrepare} = this.props
        if (name) datasetPrepare()
    }

    handleSort = (clickedColumn, data) => () => {
        const { column } = this.state

        if (column !== clickedColumn) {
            this.setState({
                column: clickedColumn,
                reverse: false,
            })
            arraySort(data, clickedColumn, { reverse: false })
        } else {
            this.setState({
                reverse: ! this.state.reverse
            })
            arraySort(data, clickedColumn, { reverse: ! this.state.reverse })
        }
    }

    render() {
        const { t, list } = this.props
        const { column, direction } = this.state

        const listEl = list.length > 0 ? (
            <>
            <h2>{ t('dataset.prepare.header') }</h2>
            <p>{ t('dataset.prepare.description') }</p>
            <Table sortable celled fixed unstackable>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell
                            sorted={ column === 'name' ? direction : null }
                            onClick={ this.handleSort('name', list) }
                        >
                            Word
                        </Table.HeaderCell>
                        <Table.HeaderCell
                            sorted={ column === 'frequency' ? direction : null }
                            onClick={ this.handleSort('frequency', list) }
                        >
                            Frequency
                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {
                        list.map(word => {
                            return (
                                <Table.Row key={ word.name }>
                                    <Table.Cell>
                                        { word.name }
                                    </Table.Cell>
                                    <Table.Cell>{ word.frequency }</Table.Cell>
                                </Table.Row>
                            )
                        })
                    }
                </Table.Body>
            </Table>
            </>

        ) : null

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>
                        <Grid.Column width={ 12 }>
                            <Header as='h1'>{ t('dataset.prepare.title') }</Header>

                            <CurrentDatasetName />

                            { listEl }

                            <Button as={ Link } to={urls.gui.pronDict.new}>
                                { t('dataset.prepare.nextButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.dataset.wordlist,
        name: state.dataset.name
    }
}

const mapDispatchToProps = dispatch => ({
    datasetPrepare: () => {
        dispatch(datasetPrepare());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DatasetPrepare))

