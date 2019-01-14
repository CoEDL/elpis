import React from 'react';
import { Container } from 'semantic-ui-react';
import './PageContainer.css';

export default function PageContainer (props) {
  return <Container className="page-contianer">{props.body}</Container>;
}