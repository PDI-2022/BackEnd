const baseURL = "http://localhost:5000/api/v1/";

const authenticateUrl = baseURL+"authenticate";
const loginUrl = baseURL+"login"
const forgetPasswordUrl = baseURL+"forgot-password"

function setUserPagePerPage(page,itensPerPage)
{
    return baseURL+`users?offset=${page}&limit=${itensPerPage}`;
}
function setUserId(userId){
    return baseURL+`users/${userId}`;
}
const createUserUrl = baseURL+"users"

const createModelUrl = baseURL+"models";
function setModelId(modelId){
    return baseURL+`models/${modelId}`
}
function setModelPagePerPage(page,itensPerPage)
{
    return baseURL+`models?offset=${page}&limit=${itensPerPage}`
}

let seedsPaginateUrl = baseURL+"process/pagination";
const getEmbriaoCSVUrl = baseURL+"process/embriao"

const processUrl = baseURL+"process"

