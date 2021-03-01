import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Grid, Button, Header, Container, Segment } from 'semantic-ui-react';
import { modelLoad, modelList } from 'redux/actions/modelActions';


class ChooseTranscriptionModel extends Component {

    componentDidMount() {
        this.props.modelList()
    }


    render() {
        const { t, currentEngine, list } = this.props
        console.log("list", list)

        const modelList = list.map((model, index) => (<p key={index}>{model.name}</p>))
        return (
            <pre>
                Choose a model:
                    <Segment>
                        import ( coming soon )
                    </Segment>
                    <Segment>
                        use existing
                        ( list of models )

                        {modelList}

                    </Segment>
                    <Segment>
                        <Link to={urls.gui.engine.index}>train a new model</Link>
                    </Segment>
            </pre>
        )
    }
}

const mapStateToProps = state => {
    return {
        list: state.model.modelList,
        currentEngine: state.engine.engine
    }
}

const mapDispatchToProps = dispatch => ({
    modelList: () => {
        dispatch(modelList())
    },
})

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(ChooseTranscriptionModel)
    )
