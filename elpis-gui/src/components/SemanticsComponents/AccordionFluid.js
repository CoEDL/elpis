import React, { Component } from 'react'
import { Accordion, Icon } from 'semantic-ui-react'

export default class AccordionExampleFluid extends Component {
  state = { activeIndex: null }

  handleClick = (e, titleProps) => {
    const { index } = titleProps
    const { activeIndex } = this.state
    const newIndex = activeIndex === index ? -1 : index

    this.setState({ activeIndex: newIndex })
  }

  render() {
    const { activeIndex } = this.state

    return (
      <Accordion styled>
        <Accordion.Title active={activeIndex === 0} index={0} onClick={this.handleClick}>
          <Icon name='dropdown' />
          {this.props.title}
        </Accordion.Title>
        <Accordion.Content active={activeIndex === 0}>
          <p>
            A dog is a type of domesticated animal. Known for its loyalty and faithfulness, it can
            be found as a welcome guest in many households across the world.
          </p>
        </Accordion.Content>
      </Accordion>
    )
  }
}