import React, { Component } from 'react';
import { Button, Grid, Header, Segment, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { dataBundleList, dataBundleLoad } from 'redux/actions';
import arraySort from 'array-sort'
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import CurrentDataBundleName from "./CurrentDataBundleName";

class DataBundleDashboard extends Component {

    state = {
        column: null,
        reverse: false
    }

    componentDidMount() {
        this.props.dataBundleList()
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

    handleLoad = name => {
        const { dataBundleLoad } = this.props
        const postData = { name: name }
        dataBundleLoad(postData)
    }

    render() {
        const { t, name, list } = this.props;
        console.log("this.props.list", list)
        console.log("this.props.name", name)
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
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                {
                    list.map( dataBundleName => {
                        const className = (dataBundleName === name) ? 'current-data-bundle' : ''
                        return (
                            <Table.Row key={ dataBundleName } className={ className }>
                                <Table.Cell>
                                    <Button fluid onClick={ () => this.handleLoad(dataBundleName) }>{ dataBundleName }</Button>
                                </Table.Cell>
                            </Table.Row>
                        )
                    })
                }
                </Table.Body>
            </Table>
        ) : <p>{ t('dataBundle.dashboard.noneMessage') }</p>

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
                                { t('dataBundle.dashboard.title') }
                            </Header>

                            <CurrentDataBundleName />

                            <Segment>
                                { listEl }
                            </Segment>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.dataBundle.dataBundleList,
        name: state.dataBundle.name
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundleList: () => {
        dispatch(dataBundleList())
    },
    dataBundleLoad: postData => {
        dispatch(dataBundleLoad(postData))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(DataBundleDashboard))
