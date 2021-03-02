import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Grid, Button, Header, Container, Segment } from 'semantic-ui-react';
import { modelLoad, modelList } from 'redux/actions/modelActions';
import { datasetLoad } from 'redux/actions/datasetActions';
import { pronDictLoad } from 'redux/actions/pronDictActions';
import urls from 'urls'


class ChooseTranscriptionModel extends Component {

    componentDidMount() {
        this.props._modelList()
    }

    handleSelectModel = (model_name) => {
        const { list, _modelLoad } = this.props

        console.log("load model_name", model_name)

        // get the matching ds and pd values
        var selectedModel = list.filter(m => m.name==model_name)
        // argh, this is weird, but reusing code from Model Dashboard
        const modelData = { name: selectedModel[0].name }
        const datasetData = { name: selectedModel[0].dataset_name }
        const pronDictData = { name: selectedModel[0].pron_dict_name }
        _modelLoad(modelData, datasetData, pronDictData)
    }


    render() {
        const { t, currentEngine, list } = this.props
        console.log("list", list)

        const modelList = list.map((model, index) => {
            return (
                <Button key={index} onClick={() => this.handleSelectModel(model.name)}>
                    {model.name}
                </Button>
            )
        })

        return (
            <pre>
                Choose a model:
                    <Segment>
                        import ( coming soon )
                    </Segment>
                    <Segment>
                        use existing
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
    _modelList: () => {
        dispatch(modelList())
    },
    _modelLoad: (modelData, datasetData, pronDictData) => {
        dispatch(modelLoad(modelData))
            .then(response => dispatch(datasetLoad(datasetData)))
            .then(response => dispatch(pronDictLoad(pronDictData)))
    }

})

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(ChooseTranscriptionModel)
    )
