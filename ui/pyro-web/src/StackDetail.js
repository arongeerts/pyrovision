import React, { useState } from "react";
import Card from "react-bootstrap/Card";


function StackDetail(props) {
    const stack = props.stack;
    if (!stack) {
        return <></>
    }
    return <Card >
        <Card.Header>{stack.id}</Card.Header>
        <div style={{textAlign: "left"}}><pre>{JSON.stringify(stack.outputs, null, 2) }</pre></div>
    </Card>
}

export default StackDetail;