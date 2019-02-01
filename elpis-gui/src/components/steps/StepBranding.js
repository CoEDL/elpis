import React, { Component } from 'react';
import { Header } from 'semantic-ui-react';


export default class StepBranding extends Component {

  render () {
    return (
      <Header as='h1'><img src="https://github.com/CoEDL/elpis/raw/master/docs/img/elpis.png" className="logo" alt="logo" /></Header>
    )
  }
}