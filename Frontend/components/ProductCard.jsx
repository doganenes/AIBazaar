import React from 'react'
import {Card} from 'react-bootstrap'

function ProductCard() {
  return (
    <div>
        <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src='public/project.png' style={{width:"200px"}}/>
      <Card.Body>
        <Card.Title>Card Title</Card.Title>
        <Card.Text>
          This is a simple card component using Bootstrap and React.
        </Card.Text>
      </Card.Body>
    </Card>
    </div>
  )
}

export default ProductCard