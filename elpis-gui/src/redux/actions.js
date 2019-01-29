export const changeFoo = foo => {
  return { type: 'CHANGE_FOO', foo }
}
export const incrementSomething = () => {
  return { type: 'INCREMENT_SOMETHING' }
}
export const updateMyName = myName => {
  return { type: 'UPDATE_MY_NAME', myName }
}