import React, { Component } from 'react';
import { Header } from 'semantic-ui-react';
import { Link } from "react-router-dom";
import elpisLogo from './elpis.png'

export default class StepBranding extends Component {

    render() {
        return (
            <Header as='h1'>
                <Link to="/">
                    <img src={elpisLogo} className="logo" alt="logo" />
                </Link>
            </Header>
        )
    }
}
