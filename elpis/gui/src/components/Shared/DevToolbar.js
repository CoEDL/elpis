import React  from "react";
import SelectEngineDropdown from "components/Engine/SelectEngineDropdown";

const DevToolbar = props => {
    return props.dev_mode ? (
        <div className="dev-toolbar">
            <SelectEngineDropdown />
        </div>
    ) : (
        <></>
    );
};

export default (DevToolbar);
