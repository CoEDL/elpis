import React, { Component } from 'react';
import { Button, Image, Segment } from 'semantic-ui-react';
import { Link } from "react-router-dom";
import { translate } from 'react-i18next';
import elpisLogo from './elpis.png'
import { connect } from 'react-redux';
import { configReset } from 'redux/actions/configActions';
import SelectEngine from 'components/Engine/SelectEngine'

class StepBranding extends Component {

    reset = () => {
        this.props.configReset()
        window.location.href = "/engine/"
    }

    render() {
        const { t, dev_mode } = this.props;

        return (
            <Segment clearing as='h1' className="top-nav">
                <Link to="/">
                    <Image floated="left" src={elpisLogo} className="logo" alt="logo" />
                </Link>
                 { dev_mode &&
                 <p>DEV MODE</p>
                 }
                <div className={"right"}>
                    <SelectEngine />
                    <Button basic onClick={this.reset}>{t('common.resetButton')}</Button>
                </div>
            </Segment>
        )
    }
}

const mapStateToProps = state => {
    return {
        dev_mode: state.config.app_config.dev_mode
    }
}

const mapDispatchToProps = dispatch => ({
    configReset: postData => {
        dispatch(configReset(postData))
            .then(response => console.log("reset OK", response))
            .catch(error => console.log("reset failed", error))
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(StepBranding))
