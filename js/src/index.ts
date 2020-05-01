import {querySimplecepAutofillFields} from "./fields-finder";
import {defaultInstallerEvents} from "./handlers";
import {enableHandlersInstall} from "./install-handlers";

/* find all CEP fields in the page and install default defaultHandlers in all of them */
querySimplecepAutofillFields().map((cepFieldData) => {
    enableHandlersInstall(cepFieldData);
    defaultInstallerEvents.forEach((event) => cepFieldData.cepField.dispatchEvent(event));
});
