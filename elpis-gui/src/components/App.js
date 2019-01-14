import React, { Component } from 'react';
import logo from '../logo.svg';
import './App.css';
import ExampleButton from './Example';
import PageContainer from './PageContainer'
import WelcomePage from './WelcomePage'

class App extends Component {
  render() {
    return (
      <div className="App">
        {/* <ExampleButton />
        <PageContainer body="This is the page body." /> */}
        <WelcomePage />
      </div>
    );
  }
}

export default App;
