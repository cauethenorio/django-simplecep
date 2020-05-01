import {CepEvents, HandlerParams} from "../types";

export const cepFieldsAutoFocusInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "focus-next",
        installer: cepFieldsAutoFocusInstaller,
    },
});

function cepFieldsAutoFocusInstaller({quickAddEventListener}: HandlerParams) {
    return quickAddEventListener(CepEvents.CepFieldsAutofilled, ({fields, cepData}) => {
        for (const {type, els} of fields) {
            // search for the first field which returned with no data
            if (cepData[type] == null) {
                for (const el of els) {
                    // search for the first element which is a form field
                    // attached to the field type
                    if (formFieldsTags.indexOf(el.tagName) >= 0) {
                        el.focus();
                        return;
                    }
                }
            }
        }
    });
}

const formFieldsTags = ["INPUT", "SELECT", "TEXTAREA"];
