import React, { Component } from 'react';
import { Grid, Header, List, Segment, Icon, Button } from 'semantic-ui-react';
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
        const { t, modelNames } = this.props;

        const list = modelNames ? (
            <ul>
                {modelNames.map( name => <li key={name}>{name}</li>)}
            </ul>
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

                            { list }

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        modelNames: state.model.modelNames
    }
}

const mapDispatchToProps = dispatch => ({
    modelList: () => {
        dispatch(modelList())
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelList))
