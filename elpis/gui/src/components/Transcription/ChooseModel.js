import React, {Component} from "react";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Button, Divider, Grid, Header, Segment} from "semantic-ui-react";
import {modelLoad, modelList} from "redux/actions/modelActions";
import {datasetLoad} from "redux/actions/datasetActions";
import {engineLoad} from "redux/actions/engineActions";
import {pronDictLoad} from "redux/actions/pronDictActions";
import Branding from "components/Shared/Branding";
import urls from "urls";


class ChooseModel extends Component {

    componentDidMount() {
        this.props._modelList();
    }

    handleSelectModel = (model_name) => {
        const {history, list, _modelLoad} = this.props;

        console.log("load model_name", model_name);

        var selectedModel = list.filter(m => m.name === model_name);
        console.log("selectedModel", selectedModel);
        const modelData = {name: selectedModel[0].name};
        const datasetData = {name: selectedModel[0].dataset_name};
        const engineName = {engine_name: selectedModel[0].engine_name};
        const pronDictData = {name: selectedModel[0].pron_dict_name};

        _modelLoad(modelData, datasetData, engineName, pronDictData);
        history.push(urls.gui.transcription.new);
    }


    render() {
        const {t, list} = this.props;
        console.log("list", list);

        const modelList = list.map((model, index) => {
            return (
                <Button key={index} onClick={() => this.handleSelectModel(model.name)}>
                    {model.name}
                </Button>
            );
        });

        return (
            <div>
                <Branding />
                <Segment>
                <Grid centered>

                <Grid.Row>
                <Grid.Column>
                    <Header as="h1" text="true">
                        {t("transcription.choose_model.title")}
                    </Header>
                    {list.length > 0 &&
                        <>
                            <Divider />
                            <p>{t("transcription.choose_model.use_existing")}</p>
                            <div>
                                {modelList}
                            </div>
                        </>
                    }
                    <Divider />
                    {list.length === 0 &&
                        t("transcription.choose_model.no_models_found")
                    }
                    <Link to={urls.gui.engine.index}>
                        {t("transcription.choose_model.train_new")}
                    </Link>
                </Grid.Column>
                </Grid.Row>
                </Grid>
                </Segment>
            </div>
       );
    }
}

const mapStateToProps = state => {
    return {
        list: state.model.modelList,
        currentEngine: state.engine.engine,
    };
};

const mapDispatchToProps = dispatch => ({
    _modelList: () => {
        dispatch(modelList());
    },
    _modelLoad: (modelData, datasetData, engineName, pronDictData) => {
        dispatch(engineLoad(engineName))
            .then(() => dispatch(modelLoad(modelData)))
            .then(() => dispatch(datasetLoad(datasetData)))
            .then(() => dispatch(pronDictLoad(pronDictData)));
    },
});

export default
    withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        withTranslation("common")(ChooseModel)
    )
);
