import {CepEvents, HandlerParams} from "../types";

/*
  This handler is responsible for locking the CEP data fields, making them
  readonly while the CEP data is fetch.

  So users won't be frustrated if they fill the fields with their own data
  and then it's overwritten by the autofill feature.
 */

export const cepFieldsLockerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepFieldsLocker",
        installer: cepFieldsLockerInstaller,
    },
});

function cepFieldsLockerInstaller({getDataFields, quickAddEventListener}: HandlerParams) {
    let lockedFields: Array<{field: HTMLElement; oldValue: string}> = [];

    function restoreFields() {
        lockedFields.forEach(({field, oldValue}) => {
            if (oldValue === "") {
                field.removeAttribute("readonly");
            } else {
                field.setAttribute("readonly", oldValue);
            }
        });
        lockedFields = [];
    }

    const removeCepFetchStartListener = quickAddEventListener(CepEvents.CepFetchStart, () => {
        const fields = getDataFields();

        fields.forEach(({type, els}) => {
            els.forEach((field) => {
                if (formFieldsTags.includes(field.tagName)) {
                    lockedFields.push({
                        field,
                        oldValue: field.getAttribute("readonly") || "",
                    });
                    field.setAttribute("readonly", "readonly");
                }
            });
        });
    });

    const removeCepFetchErrorListener = quickAddEventListener(
        CepEvents.CepFetchError,
        restoreFields
    );
    const removeCepFieldsAutofilledListener = quickAddEventListener(
        CepEvents.CepFieldsAutofilled,
        restoreFields
    );

    return () => {
        removeCepFetchStartListener();
        removeCepFetchErrorListener();
        removeCepFieldsAutofilledListener();
    };
}

const formFieldsTags = ["INPUT", "SELECT", "TEXTAREA"];
