import React, { useState } from "react";
import ListGroup from 'react-bootstrap/ListGroup';
import { getStacks } from "./api";
import { Spinner } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";


function StackList(props) {
    const [hasFetched, setFetched] = useState(false);
    const [stacks, setStacks] = useState([]);

    const refresh = () => {
        getStacks().then(data => {
            setStacks(data);
            setFetched(true)
        })
    }
    if (!hasFetched) {
        refresh()
        return <div style={{padding: 20}}><Spinner animation="border" variant="primary" /></div>
    } 
    
    if (stacks.length !== 0) {
        return <ListGroup>
            <ListGroup.Item 
                key="list-collection-header" 
                active
                variant={"secondary"} >
                Stacks <FontAwesomeIcon icon={faSyncAlt} onClick={() => setFetched(false)}/>
            </ListGroup.Item>
            {stacks.stacks.map(
                s => <ListGroup.Item 
                    key={s.id} 
                    action 
                    active={props.selected && s.id===props.selected.id}
                    onClick={() => props.selectStack(s)}>
                    {s.id}
                    </ListGroup.Item>
            )}
        </ListGroup>
    } else {
        return <div>No stacks found</div>
    }
}

export default StackList;