import React, { Component } from 'react';
import { Button, Image, Segment } from 'semantic-ui-react';
import { Link } from "react-router-dom";
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
        return (
            <Segment clearing as='h1' className="top-nav">
                <Link to="/">
                    <Image floated="left" src={elpisLogo} className="logo" alt="logo" />
                </Link>
                <div className={"right"}>
                    <SelectEngine />
                    <Button basic onClick={this.reset}>reset</Button>
                </div>
            </Segment>
        )
    }
}

const mapDispatchToProps = dispatch => ({
    configReset: postData => {
        dispatch(configReset(postData))
            .then(response => console.log("reset OK", response))
            .catch(error => console.log("reset failed", error))
    }
})

export default connect(null, mapDispatchToProps)(StepBranding)
