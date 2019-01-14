import React, { Component } from 'react';
import logo from '../logo.svg';
import './App.css';
import ExampleButton from './Example';
import PageContainer from './PageContainer'

class App extends Component {
  render() {
    return (
      <div className="App">
        <ExampleButton />
        <PageContainer body="This is the page body." />
      </div>
    );
  }
}

export default App;
