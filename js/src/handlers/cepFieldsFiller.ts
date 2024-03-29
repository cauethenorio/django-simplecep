import {CepEvents, HandlerParams} from "../types";

export const cepFieldsFillerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepFieldsFiller",
        installer: cepFieldsFillerInstaller,
    },
});

function cepFieldsFillerInstaller({
    getDataFields,
    quickAddEventListener,
    quickDispatchEvent,
}: HandlerParams) {
    return quickAddEventListener(CepEvents.CepFetchSuccess, (cepData: CepDataType) => {
        const fields = getDataFields();
        fields.forEach(({type, els}) => {
            const val = cepData[type];
            if (val != null) {
                els.forEach((e) => {
                    if (e instanceof HTMLInputElement) {
                        e.value = val;
                    }
                });
            }
        });
        quickDispatchEvent(CepEvents.CepFieldsAutofilled, {fields, cepData});
    });
}
