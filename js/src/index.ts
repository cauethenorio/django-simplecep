import {querySimplecepAutofillFields} from "./fields-finder";
import {defaultHandlers} from "./handlers";
import {installHandlers} from "./install-handlers";

/* find all CEP fields in the page and install default defaultHandlers in all of them */
querySimplecepAutofillFields().map(cepFieldData =>
    installHandlers(cepFieldData, defaultHandlers)
);
