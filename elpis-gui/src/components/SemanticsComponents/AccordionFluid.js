import React, { Component } from 'react'
import { Accordion, Icon } from 'semantic-ui-react'

export default class AccordionExampleFluid extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeIndex: (props.active!==undefined && props.active!==false) ? 0 : -1,
    }
  }

  handleClick = (e, titleProps) => {
    const { index } = titleProps
    const { activeIndex } = this.state
    const newIndex = activeIndex === index ? -1 : index

    this.setState({ activeIndex: newIndex })
  }

  render() {
    const { activeIndex } = this.state
    const { iconName } = this.props;
    console.log( this.state.activeIndex);
    
    return (
      <Accordion styled>
        <Accordion.Title active={activeIndex === 0} index={0} onClick={this.handleClick}>
          <Icon name={iconName} />
          {this.props.title}
          <Icon name='dropdown' />
        </Accordion.Title>
        <Accordion.Content active={activeIndex === 0}>
          {this.props.children}
        </Accordion.Content>
      </Accordion>
    )
  }
}