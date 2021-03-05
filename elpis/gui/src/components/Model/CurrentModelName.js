import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import SelectEngineDropdown from 'components/Engine/SelectEngineDropdown'
import urls from 'urls'

class CurrentModelName extends Component {

    render() {
        const { t, currentEngine, engineHumanNames, modelList, datasetName, pronDictName, name, match } = this.props

        const onDashboard = (match.url === urls.gui.model.index) ? true : false
        const engineHumanName = currentEngine ? engineHumanNames[currentEngine] : ''
        const dictName = pronDictName ? pronDictName : t('model.common.pronDictNotRequired')

        return (
            <>
                {name &&
                <Message color='olive'>
                    { t('engine.common.currentEngineLabel') + engineHumanName }
                    <br />
                    { t('model.common.currentModelLabel') + name }
                    <br />
                    {currentEngine && currentEngine == 'kaldi' &&
                        <>
                            {t('pronDict.common.currentPronDictLabel') + dictName}
                            <br />
                        </>
                    }
                    {t('dataset.common.currentDatasetLabel') + datasetName }
                </Message>
                }

                {!currentEngine &&
                <Message color='purple'>
                    { t('engine.common.noCurrentEngineLabel') }
                    <SelectEngineDropdown />
                </Message>
                }

                {currentEngine && !name &&
                <Message color='purple'>
                    {onDashboard && modelList.length === 0 &&
                        t('common.makeNewOne')
                    }
                    {onDashboard && modelList.length > 0 &&
                        t('common.selectOneBelow')
                    }
                    {!onDashboard &&
                        <>
                            <p>{ t('model.common.currentModelLabel') }</p>
                            <Link to={urls.gui.model.index}>
                                { t('common.chooseOrNewLabel') }
                            </Link>
                        </>
                    }
                </Message>
                }
            </>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        modelList: state.model.modelList,
        datasetName: state.model.datasetName,
        pronDictName: state.model.pronDictName,
        currentEngine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names
    }
}
export default withRouter(
    connect(mapStateToProps)(
        translate('common')(CurrentModelName)
    )
)