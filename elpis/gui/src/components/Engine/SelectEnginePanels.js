import React, { Component } from 'react';
import { withRouter } from "react-router-dom";
import { Card, Grid, Segment, Header, Button, Dropdown, Divider } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { engineLoad } from 'redux/actions/engineActions';
import { setCurrentStep } from 'redux/actions/sideNavActions'
import urls from 'urls';


class SelectEnginePanels extends Component {

    render() {

        let { t, currentEngine, list, _engineLoad, history } = this.props;

        let handleChange = (_event, data) => {
            let engine_name = data.value;
            let postData = { engine_name };
            _engineLoad(postData);
        };

        let selectEngine = engine_name => {
            console.log("select engine", engine_name)
            let postData = { engine_name };
            _engineLoad(postData);
            history.push(urls.gui.dataset.index)
        }

        let options = list.map((name, i) => ({key: name, text: name, value: name}));

        let cards = list.map((name, i) => {
            console.log("name", name)
            let engine_description
            switch (name) {
                case 'kaldi':
                    engine_description = t('engine.common.kaldi_description')
                    break
                case 'espnet':
                    engine_description = t('engine.common.espnet_description')
                    break
            }

            return (

                <div className="engine-type-button" key={name} onClick={() => selectEngine(name)}>
                    {engine_description}
                </div>
            )
        });


        return (
            <>
                {list.length === 0 &&
                    <p>{t('engine.select.waitingForEngineList')}</p>
                }
                {
                cards
                }

            </>
        )
    }
}

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine,
    }
}

const mapDispatchToProps = dispatch => ({
    _engineLoad: postData => {
        dispatch(engineLoad(postData))
    }
})

export default
    withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(SelectEnginePanels)
    )
)
