export const apiURL = process.env.REACT_APP_API_URL

export const getStacks = () => {
    return fetch(apiURL + "/stacks").then(resp => resp.json())
}

export const getStack = (identifier) => {
    return fetch(apiURL + "/stacks/" + identifier).then(resp => resp.json())
}