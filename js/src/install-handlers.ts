import {
    InstallHandlerCustomEvent,
    UninstallHandlerCustomEvent,
    HandlerParams,
    CepEvents,
    AutofillFieldDataType,
} from "./types";

import {createQuickEventsFuncsFor} from "./quick-events";

const createDataFieldsGetter = (
    dataFields: AutofillFieldDataType["dataFields"]
): HandlerParams["getDataFields"] => () =>
    dataFields.map(({type, selector}) => ({
        type,
        els: Array.prototype.slice
            .call(document.querySelectorAll(selector))
            .filter((node: HTMLElement | null) => node != null),
    }));

function getHandlerInstallerParameters(fieldData: AutofillFieldDataType) {
    /* create an object with useful data to be sent as param to handler installers */
    const {baseCepURL, dataFields} = fieldData;
    const getCepURL: HandlerParams["getCepURL"] = (cep: string): string =>
        baseCepURL.replace("00000000", cep);
    const getDataFields = createDataFieldsGetter(dataFields);

    const {quickAddEventListener, quickDispatchEvent} = createQuickEventsFuncsFor(
        fieldData.cepField
    );

    /* when you install a CEP field handler, these are the parameters your
    installer function will receive */
    return {
        getCepURL,
        getDataFields,
        fieldData,
        quickDispatchEvent,
        quickAddEventListener,
    };
}

export function enableHandlersInstall(fieldData: AutofillFieldDataType) {
    // object with all installed handlers as key
    // and a func to uninstall them as value
    let installedHandlers: {[handlerName: string]: () => undefined} = {};
    const {cepField} = fieldData;

    cepField.addEventListener(CepEvents.InstallHandler, ((event: InstallHandlerCustomEvent) => {
        const {installer, handlerName} = event.detail;

        /* it there's already a handler registered with that name, unregister it.
        So it's easier for the user to replace any handler */
        if (installedHandlers[handlerName] != null) {
            const previousHandlerUninstall = installedHandlers[handlerName];
            previousHandlerUninstall();
            console.log(`Handler '${handlerName}' removed to be replaced.`);
        }

        const handlerInstallerParams = getHandlerInstallerParameters(fieldData);
        installedHandlers[handlerName] = installer(handlerInstallerParams);
        console.log(`Handler '${handlerName}' installed.`);
    }) as EventListener);

    cepField.addEventListener(CepEvents.removeHandler, ((event: UninstallHandlerCustomEvent) => {
        const {handlerName} = event.detail;
        installedHandlers[handlerName]();
        console.log(`Handler '${handlerName}' removed.`);
    }) as EventListener);
}
