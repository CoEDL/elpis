# The State Tree

All information important to the process of transcription is stored in the state tree. The structure of the tree seperated data by the steps in the process.

Once information in put into the state tree, it can be considered non-volitile and will persists after a power cycles. The backend and frontend store slightly different properties in their state trees, however, there are some common properties shown below.

The common top-level state tree:
```
state: {
    dataset: ...,
    pronDict: ...,
    model: ...,
    transcription: ...
}
```

