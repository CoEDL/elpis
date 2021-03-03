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

        let selectEngine = engine_name => {
            let postData = { engine_name };
            _engineLoad(postData, this.props.history);
        }

        let options = list.map((name, i) => ({key: name, text: name, value: name}));

        let cards = list.map((name, i) => {
            let engine_name, engine_description
            switch (name) {
                case 'kaldi':
                    engine_name = t('engine.common.kaldi_name')
                    engine_description = t('engine.common.kaldi_description')
                    break
                case 'espnet':
                    engine_name = t('engine.common.espnet_name')
                    engine_description = t('engine.common.espnet_description')
                    break
            }
            return (
                <Grid.Row key={name}>
                    <Grid.Column width={3} className="engine-name">
                        <div className="choose-engine-button">
                            <Button onClick={() => selectEngine(name)}>{engine_name}</Button>
                        </div>
                    </Grid.Column>
                    <Grid.Column width={12} className="engine-description">
                        <p>{engine_description}</p>
                    </Grid.Column>
                </Grid.Row>
            )
        });


        return (
            <>
                {list.length === 0 &&
                    <p>{t('engine.select.waitingForEngineList')}</p>
                }

			    <Grid columns={2} className="choose-engine">
                            {cards}
                </Grid>

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
    _engineLoad: (postData, history) => {
        dispatch(engineLoad(postData))
        .then(response => {
            history.push(urls.gui.dataset.index)
           })
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
