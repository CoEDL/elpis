import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button, Grid, Header, Segment, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import arraySort from 'array-sort'
import { dataBundlePrepare } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentDataBundleName from "./CurrentDataBundleName";
import urls from 'urls'

class DataBundlePrepare extends Component {

    state = {
        column: null,
        reverse: false
    }

    componentDidMount() {
        this.props.dataBundlePrepare()
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
            <Table sortable celled fixed unstackable>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell
                            sorted={ column === 'name' ? direction : null }
                            onClick={ this.handleSort('name', list) }
                        >
                            Name
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

        ) : <p>{ t('model.dashboard.noneMessage') }</p>

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>
                        <Grid.Column width={ 12 }>
                            <Header as='h1'>{ t('dataBundle.prepare.title') }</Header>

                            <CurrentDataBundleName />

                            <h2>{ t('dataBundle.prepare.header') }</h2>
                            <p>{ t('dataBundle.prepare.bannerMessage') }</p>

                            {/* <p>{ t('dataBundle.prepare.bannerMessageDetailed') }</p> */}

                            {/* { wordlistTable } */}

                            { listEl }

                            <Button as={ Link } to={urls.gui.model.new}>
                                { t('dataBundle.prepare.nextButton') }
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
        list: state.dataBundle.wordlist
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundlePrepare: () => {
        dispatch(dataBundlePrepare());
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundlePrepare))

