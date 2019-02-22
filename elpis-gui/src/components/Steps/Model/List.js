import React, { Component } from 'react';
import { Grid, Header, List, Segment, Icon, Button, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelList } from 'redux/actions';
import _ from 'lodash'
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelList extends Component {

    // TODO: clean this up, make it work better with data from redux state

    state = {
        column: null,
        data: [],
        direction: null,
    }

    componentDidMount() {
        const { modelList } = this.props
        modelList()
    }

    handleSort = (clickedColumn, data) => () => {
        const { column,  direction } = this.state

        if (column !== clickedColumn) {
          this.setState({
            column: clickedColumn,
            // data: _.sortBy(data, [clickedColumn]),
            direction: 'ascending',
          })
          return
        }

        if (data) {
            this.setState({
                data: data.reverse(),
                direction: direction === 'ascending' ? 'descending' : 'ascending',
            })
        }
    }

    render() {
        const { t, list } = this.props;
        const { column, direction } = this.state

        console.log("list", list)

        const listEl = list.length > 0 ? (
            <Table sortable celled fixed unstackable>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell
                        sorted={column === 'name' ? direction : null}
                        onClick={this.handleSort('name', list)}
                        >
                        Name
                        </Table.HeaderCell>
                        <Table.HeaderCell
                        sorted={column === 'wer' ? direction : null}
                        onClick={this.handleSort('wer', list.results)}
                        >
                        WER
                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {list.map(model => (
                        <Table.Row key={model.name}>
                        <Table.Cell>{model.name}</Table.Cell>
                        <Table.Cell>{model.results.wer}</Table.Cell>
                        </Table.Row>
                    ))}
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
